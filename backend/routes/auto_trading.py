# backend/auto_trading.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any, List
import time
import logging

logger = logging.getLogger(__name__)


# ------------------------------
# 1) أوضاع التداول الثلاثة
# ------------------------------
class TradingMode(str, Enum):
    SIGNALS_ONLY = "signals_only"      # إشارات فقط (لا تنفيذ أوامر)
    SEMI_AUTO    = "semi_auto"         # إشارات + أمر جاهز يحتاج تأكيد
    FULL_AUTO    = "full_auto"         # تداول آلي كامل


# ------------------------------
# 2) إعدادات الاستراتيجية لكل مستخدم
# ------------------------------
@dataclass
class StrategyConfig:
    user_id: int
    mode: TradingMode
    max_risk_per_trade_pct: float  # نسبة المخاطرة من الرصيد (مثلاً 1 أو 2)
    max_daily_loss_pct: float      # حد أقصى للخسارة اليومية
    max_positions: int             # عدد الصفقات المفتوحة في نفس الوقت
    symbols: List[str]             # العملات / الأسهم / الذهب… المراد تداولها
    exchanges: List[str]           # المنصات المفعلة لهذا المستخدم
    use_smart_analysis: bool       # هل نستخدم التحليل الذكي الموحد؟
    auto_trading_enabled: bool     # تشغيل/إيقاف التداول الآلي


# ------------------------------
# 3) طبقة المنصّة العامة (Interface)
# ------------------------------
class ExchangeClient:
    """
    واجهة عامة لأي منصة (Binance, Bybit, OKX, KuCoin, …)
    كل منصة حقيقية تعمل class يرث من هذا ويطبّق الدوال.
    """

    def __init__(self, api_key: str, api_secret: str, name: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.name = name

    # سعر السوق الحالي
    def get_price(self, symbol: str) -> float:
        raise NotImplementedError

    # رصيد العملة أو الرصيد الأساسي (مثل USDT أو USD)
    def get_balance(self, asset: str) -> float:
        raise NotImplementedError

    # فتح صفقة سوقية (Market)
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        raise NotImplementedError

    # إغلاق صفقة / أمر عكسي
    def close_position(self, symbol: str) -> Dict[str, Any]:
        raise NotImplementedError


# ------------------------------
# 4) مثال: عميل منصة وهمي (Placeholder)
#    تستبدله لاحقا بعميل Binance / Bybit / OKX حقيقي
# ------------------------------
class DummyExchange(ExchangeClient):
    def __init__(self, api_key: str, api_secret: str, name: str = "dummy"):
        super().__init__(api_key, api_secret, name)

    def get_price(self, symbol: str) -> float:
        logger.info(f"[{self.name}] Getting price for {symbol}")
        return 100.0  # قيمة تجريبية

    def get_balance(self, asset: str) -> float:
        logger.info(f"[{self.name}] Getting balance for {asset}")
        return 1000.0  # قيمة تجريبية

    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Placing {side} order on {symbol} qty={quantity}")
        return {
            "status": "filled",
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": self.get_price(symbol),
            "exchange": self.name,
            "time": time.time(),
        }

    def close_position(self, symbol: str) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Closing position on {symbol}")
        return {
            "status": "closed",
            "symbol": symbol,
            "exchange": self.name,
            "time": time.time(),
        }


# ------------------------------
# 5) المحرك الرئيسي للتداول الآلي
# ------------------------------
class AutoTradingEngine:
    """
    المحرك المسؤول عن:
    - إدارة إعدادات الاستراتيجيات لكل مستخدم
    - استقبال نتائج التحليل الذكي (crypto + أسهم + ذهب)
    - حساب حجم الصفقة (Position Size) بحسب المخاطرة
    - اتخاذ قرار: إشارة فقط / شبه آلي / آلي كامل
    - التواصل مع المنصات المتعددة عبر ExchangeClient
    """

    def __init__(self):
        # هنا ممكن تربط لاحقا بقاعدة بيانات بدل القواميس
        self._strategies: Dict[int, StrategyConfig] = {}      # user_id -> StrategyConfig
        self._exchange_clients: Dict[str, ExchangeClient] = {}  # "binance", "bybit", ... -> client instance

    # --------------------------------
    # إدارة المنصات
    # --------------------------------
    def register_exchange_client(self, name: str, client: ExchangeClient):
        """
        مثال:
        engine.register_exchange_client("binance", BinanceClient(api_key, secret))
        """
        self._exchange_clients[name] = client
        logger.info(f"Registered exchange client: {name}")

    # --------------------------------
    # إدارة إعدادات المستخدمين
    # --------------------------------
    def set_user_strategy(self, config: StrategyConfig):
        self._strategies[config.user_id] = config
        logger.info(f"Set strategy for user {config.user_id}: mode={config.mode}")

    def get_user_strategy(self, user_id: int) -> Optional[StrategyConfig]:
        return self._strategies.get(user_id)

    # --------------------------------
    # مساعد: حساب حجم الصفقة
    # --------------------------------
    def _calculate_position_size(
        self,
        exchange: ExchangeClient,
        symbol: str,
        config: StrategyConfig,
        stop_loss_pct: float = 1.0,
        base_asset: str = "USDT",
    ) -> float:
        """
        حساب حجم الصفقة بناء على:
        - رصيد المستخدم
        - نسبة المخاطرة per trade
        - حجم الستوب لوس كنسبة مئوية تقريبية
        """
        balance = exchange.get_balance(base_asset)
        if balance <= 0:
            return 0.0

        # مبلغ المخاطرة في هذه الصفقة
        risk_amount = balance * (config.max_risk_per_trade_pct / 100.0)
        current_price = exchange.get_price(symbol)

        if current_price <= 0 or stop_loss_pct <= 0:
            return 0.0

        # تقريب: مقدار الخسارة لكل وحدة = السعر * (stop_loss_pct / 100)
        loss_per_unit = current_price * (stop_loss_pct / 100.0)
        qty = risk_amount / loss_per_unit
        return round(qty, 6)

    # --------------------------------
    # 6) استقبال إشارة تحليل ذكي وتنفيذ المنطق
    # --------------------------------
    def handle_smart_signal(
        self,
        user_id: int,
        symbol: str,
        direction: str,  # "buy" or "sell"
        confidence: float,  # 0-1
        analysis_summary: str,
        stop_loss_pct: float = 1.5,
        take_profit_pct: float = 3.0,
    ) -> Dict[str, Any]:
        """
        هذه الدالة تُستَدعى من الباكند بعد ما ينتهي التحليل الذكي
        (يشمل العملات + الأسهم + الذهب حسب المشروع).
        """

        config = self.get_user_strategy(user_id)
        if not config:
            return {"error": "strategy_not_configured"}

        if not config.auto_trading_enabled and config.mode != TradingMode.SIGNALS_ONLY:
            # المستخدم أوقف التداول الآلي لكن يسمح بالإشارات فقط
            config.mode = TradingMode.SIGNALS_ONLY

        # نختار أول منصة مفعلة في config.exchanges
        if not config.exchanges:
            return {"error": "no_exchanges_configured"}

        primary_exchange_name = config.exchanges[0]
        exchange = self._exchange_clients.get(primary_exchange_name)
        if not exchange:
            return {"error": f"exchange_client_not_found: {primary_exchange_name}"}

        # بناء نتيجة أساسية
        result = {
            "user_id": user_id,
            "symbol": symbol,
            "direction": direction,
            "confidence": confidence,
            "mode": config.mode.value,
            "analysis_summary": analysis_summary,
            "primary_exchange": primary_exchange_name,
        }

        # 1) وضع الإشارات فقط
        if config.mode == TradingMode.SIGNALS_ONLY:
            result["action"] = "signal_only"
            result["message"] = "تم إنشاء إشارة فقط بدون تنفيذ أمر."
            return result

        # 2) حساب حجم الصفقة
        size = self._calculate_position_size(
            exchange=exchange,
            symbol=symbol,
            config=config,
            stop_loss_pct=stop_loss_pct,
        )

        if size <= 0:
            result["action"] = "no_trade"
            result["message"] = "لا يمكن حساب حجم صفقة مناسب."
            return result

        # 3) وضع شبه آلي: نرجع كل التفاصيل للواجهة وتطلب تأكيد من المستخدم
        if config.mode == TradingMode.SEMI_AUTO:
            result["action"] = "pending_user_confirmation"
            result["proposed_order"] = {
                "symbol": symbol,
                "side": direction,
                "quantity": size,
                "stop_loss_pct": stop_loss_pct,
                "take_profit_pct": take_profit_pct,
            }
            result["message"] = "تم تحضير أمر، في انتظار تأكيد المستخدم."
            return result

        # 4) وضع آلي كامل: تنفيذ مباشر
        if config.mode == TradingMode.FULL_AUTO:
            order = exchange.place_market_order(symbol=symbol, side=direction, quantity=size)
            result["action"] = "order_executed"
            result["order"] = order
            result["stop_loss_pct"] = stop_loss_pct
            result["take_profit_pct"] = take_profit_pct
            result["message"] = "تم تنفيذ صفقة تلقائيًا."
            return result

        # إذا وصلنا هنا، فهناك وضع غير معروف
        result["action"] = "unknown_mode"
        result["message"] = "وضع التداول غير معروف."
        return result
