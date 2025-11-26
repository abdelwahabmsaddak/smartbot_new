"""
AutoTradingPro - محرك التداول الآلي الاحترافي للمشروع SmartBot

ملاحظات مهمّة:
- بشكل افتراضي LIVE_MODE = False  => التداول تجريبي (paper trading) فقط.
- لتفعيل التداول الحقيقي لازم تمرّر live=True وتوفّر API keys صحيحة.
- الاستعمال على مسؤوليتك الخاصة، هذا الكود تعليمي وما فيهوش أي ضمان للربح.

مثال ربط سريع مع الراوت (داخل routes/auto_trading.py):

from backend.auto_trading import AutoTradingPro

bot = AutoTradingPro(
    exchange_name="binance",
    api_key="YOUR_KEY",
    api_secret="YOUR_SECRET",
    symbol="BTC/USDT",
    timeframe="1h"
)

signal, info = bot.run_once()
"""

from __future__ import annotations
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional

import ccxt
import numpy as np
import pandas as pd
import talib
from datetime import datetime


# -------- إعدادات أساسية -------- #

SUPPORTED_EXCHANGES = [
    "binance",
    "bybit",
    "kucoin",
    "okx",
    "gateio",
]


@dataclass
class TradeConfig:
    symbol: str = "BTC/USDT"
    timeframe: str = "1h"
    risk_per_trade: float = 0.01      # 1% من الرأسمال
    max_open_trades: int = 3
    leverage: int = 1
    min_balance: float = 50.0         # أقل رصيد للتداول
    halal_symbols: Optional[List[str]] = None  # قائمة الرموز المسموح بها
    take_profit_pct: float = 0.03     # 3%
    stop_loss_pct: float = 0.01       # 1%


@dataclass
class StrategyResult:
    signal: str               # "buy" / "sell" / "hold"
    ema_fast: float
    ema_slow: float
    rsi: float
    macd: float
    macd_signal: float
    bb_upper: float
    bb_lower: float
    price: float
    smart_score: float        # من 0 إلى 100
    final_reason: str


class AutoTradingPro:
    def __init__(
        self,
        exchange_name: str,
        api_key: str = "",
        api_secret: str = "",
        config: TradeConfig = None,
        live: bool = False,
        sandbox: bool = True,
    ):
        if exchange_name.lower() not in SUPPORTED_EXCHANGES:
            raise ValueError(
                f"Exchange '{exchange_name}' غير مدعومة. اختار واحدة من: {SUPPORTED_EXCHANGES}"
            )

        self.exchange_name = exchange_name.lower()
        self.api_key = api_key
        self.api_secret = api_secret
        self.live = live
        self.sandbox = sandbox

        self.config = config or TradeConfig()

        # لو ما عطيناش قائمة حلال: نستعمل قائمة افتراضية
        if self.config.halal_symbols is None:
            self.config.halal_symbols = [
                "BTC/USDT",
                "ETH/USDT",
                "XAU/USD",   # ذهب
                "XAG/USD",   # فضة
            ]

        self.exchange = self._create_exchange()

    # ---------- تهيئة المنصّة ---------- #
    def _create_exchange(self):
        klass = getattr(ccxt, self.exchange_name)
        params = {
            "apiKey": self.api_key,
            "secret": self.api_secret,
            "enableRateLimit": True,
        }
        exchange = klass(params)

        if hasattr(exchange, "set_sandbox_mode"):
            exchange.set_sandbox_mode(self.sandbox)

        return exchange

    # ---------- جلب البيانات ---------- #
    def fetch_ohlcv(self, limit: int = 200) -> pd.DataFrame:
        """
        يجلب بيانات OHLCV ويحولها إلى DataFrame.
        """
        ohlcv = self.exchange.fetch_ohlcv(
            self.config.symbol,
            timeframe=self.config.timeframe,
            limit=limit,
        )
        df = pd.DataFrame(
            ohlcv,
            columns=["timestamp", "open", "high", "low", "close", "volume"],
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df

    # ---------- المؤشرات و التحليل ---------- #
    def _calculate_indicators(self, df: pd.DataFrame) -> StrategyResult:
        close = df["close"].values.astype(float)

        ema_fast = talib.EMA(close, timeperiod=21)
        ema_slow = talib.EMA(close, timeperiod=55)

        rsi = talib.RSI(close, timeperiod=14)

        macd, macd_signal, _ = talib.MACD(
            close, fastperiod=12, slowperiod=26, signalperiod=9
        )

        bb_upper, bb_middle, bb_lower = talib.BBANDS(
            close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )

        last = -1
        price = float(close[last])
        ema_fast_last = float(ema_fast[last])
        ema_slow_last = float(ema_slow[last])
        rsi_last = float(rsi[last])
        macd_last = float(macd[last])
        macd_signal_last = float(macd_signal[last])
        bb_upper_last = float(bb_upper[last])
        bb_lower_last = float(bb_lower[last])

        # قواعد بسيطة للإشارة
        signal = "hold"
        reason = []

        # ترند صاعد لما EMA السريع فوق البطيء
        if ema_fast_last > ema_slow_last:
            reason.append("اتجاه صاعد EMA")
            if rsi_last < 70 and macd_last > macd_signal_last and price > ema_fast_last:
                signal = "buy"
                reason.append("RSI طبيعي و MACD إيجابي")
        # ترند هابط
        if ema_fast_last < ema_slow_last:
            reason.append("اتجاه هابط EMA")
            if rsi_last > 30 and macd_last < macd_signal_last and price < ema_fast_last:
                signal = "sell"
                reason.append("RSI طبيعي و MACD سلبي")

        # Bollinger: لو السعر قريب من الحد السفلي مع ترند صاعد => تعزيز شراء
        if signal == "buy" and price <= bb_lower_last * 1.01:
            reason.append("السعر عند الحد السفلي للبولنجر (فرصة شراء قوية)")
        # والعكس للبيع
        if signal == "sell" and price >= bb_upper_last * 0.99:
            reason.append("السعر عند الحد العلوي للبولنجر (فرصة بيع قوية)")

        # نحسب smart_score (0 – 100)
        score = 50.0
        if ema_fast_last > ema_slow_last:
            score += 10
        else:
            score -= 10

        if macd_last > macd_signal_last:
            score += 10
        else:
            score -= 10

        if 40 <= rsi_last <= 60:
            score += 10
        elif rsi_last < 30 or rsi_last > 70:
            score -= 10

        # قرب السعر من منتصف البولنجر (أقل تذبذب)
        dist_to_mid = abs(price - (bb_upper_last + bb_lower_last) / 2)
        range_bb = bb_upper_last - bb_lower_last
        if range_bb > 0:
            norm = dist_to_mid / range_bb
            score += max(0, (0.5 - norm)) * 20

        score = max(0.0, min(100.0, score))

        return StrategyResult(
            signal=signal,
            ema_fast=ema_fast_last,
            ema_slow=ema_slow_last,
            rsi=rsi_last,
            macd=macd_last,
            macd_signal=macd_signal_last,
            bb_upper=bb_upper_last,
            bb_lower=bb_lower_last,
            price=price,
            smart_score=score,
            final_reason=" | ".join(reason) if reason else "لا يوجد شرط قوي، انتظار أفضل فرصة",
        )

    # ---------- إدارة رأس المال ---------- #
    def _get_balance(self, quote_currency: str = "USDT") -> float:
        balance = self.exchange.fetch_balance()
        if quote_currency in balance["free"]:
            return float(balance["free"][quote_currency])
        return 0.0

    def _calculate_position_size(self, price: float, balance: float) -> float:
        risk_amount = balance * self.config.risk_per_trade
        if risk_amount <= 0:
            return 0.0
        qty = (risk_amount * self.config.leverage) / price
        return float(qty)

    # ---------- تنفيذ الأوامر (أو محاكاة) ---------- #
    def _create_order(self, side: str, amount: float, price: float) -> Dict:
        """
        لو self.live == False => نرجّع صفقة وهمية (paper trade).
        """
        if amount <= 0:
            return {"status": "error", "message": "amount <= 0"}

        if not self.live:
            return {
                "status": "paper",
                "side": side,
                "amount": amount,
                "price": price,
                "symbol": self.config.symbol,
                "timestamp": datetime.utcnow().isoformat(),
            }

        # *** تداول حقيقي – انتبه ***
        order = self.exchange.create_market_order(
            self.config.symbol,
            side,
            amount,
        )
        return order

    # ---------- فحص “حلال” بسيط ---------- #
    def _is_halal_symbol(self) -> bool:
        return self.config.symbol in (self.config.halal_symbols or [])

    # ---------- تشغيل خطوة واحدة (للـ Dashboard أو الـ API) ---------- #
    def run_once(self) -> Tuple[str, Dict]:
        """
        يرجّع (signal, details_dict) لاستعمالها في dashboard أو Telegram.
        """
        if not self._is_halal_symbol():
            return "hold", {
                "error": "الرمز غير موجود في قائمة الحلال",
                "symbol": self.config.symbol,
            }

        df = self.fetch_ohlcv()
        strategy_result = self._calculate_indicators(df)

        # لو ما فيش شروط واضحة => نرجع hold فقط
        if strategy_result.signal == "hold":
            return "hold", asdict(strategy_result)

        # رصيد بالعملة المقابلة (USDT مثلا)
        quote = self.config.symbol.split("/")[-1]
        balance = self._get_balance(quote_currency=quote)

        if balance < self.config.min_balance:
            info = asdict(strategy_result)
            info["warning"] = "الرصيد أقل من الحد الأدنى للتداول"
            return "hold", info

        qty = self._calculate_position_size(
            price=strategy_result.price, balance=balance
        )

        order = self._create_order(
            side=strategy_result.signal,
            amount=qty,
            price=strategy_result.price,
        )

        info = asdict(strategy_result)
        info["order"] = order

        # نضيف TP / SL نظريين في info (تنجم تستعملهم في منصّات مختلفة)
        if strategy_result.signal == "buy":
            info["take_profit"] = strategy_result.price * (
                1 + self.config.take_profit_pct
            )
            info["stop_loss"] = strategy_result.price * (
                1 - self.config.stop_loss_pct
            )
        elif strategy_result.signal == "sell":
            info["take_profit"] = strategy_result.price * (
                1 - self.config.take_profit_pct
            )
            info["stop_loss"] = strategy_result.price * (
                1 + self.config.stop_loss_pct
            )

        return strategy_result.signal, info

    # ---------- تشغيل مستمر (للـ Cron أو Worker) ---------- #
    def run_loop(self, sleep_seconds: int = 60 * 5):
        """
        حلقة بسيطة: كل فترة تعمل run_once().
        من الأفضل تشغّلها في Worker منفصل عن Flask.
        """
        while True:
            try:
                signal, info = self.run_once()
                print(f"[{datetime.utcnow()}] signal={signal} info={info}")
            except Exception as e:
                print("AutoTradingPro error:", e)
            time.sleep(sleep_seconds)
