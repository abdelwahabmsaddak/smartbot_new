document.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch("/api/dashboard");
        const data = await res.json();

        document.getElementById("balance").innerText = `$${data.balance}`;
        document.getElementById("openTrades").innerText = data.open_trades;
        document.getElementById("aiStatus").innerText =
            data.ai_status === "active" ? "🟢 Active" : "🔴 Offline";
        document.getElementById("dailyProfit").innerText = `+$${data.daily_profit}`;

        const list = document.getElementById("aiLogs");
        list.innerHTML = "";

        data.ai_logs.forEach(log => {
            const li = document.createElement("li");
            li.textContent = log;
            list.appendChild(li);
        });

      fetch("/api/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    message: "حلل BTC/USDT"
  })
})
.then(res => res.json())
.then(data => {
  console.log(data.reply);
});

        fetch("/api/ai-signals/analyze", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    asset: "XAUUSD",
    timeframe: "4h",
    market: "gold"
  })
})
.then(r => r.json())
.then(d => console.log(d.signal));
        
    } catch (err) {
        console.error("Dashboard API error", err);
    }
});
