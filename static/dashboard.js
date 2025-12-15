document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("balance").innerText = "$12,450";
    document.getElementById("openTrades").innerText = "3";
    document.getElementById("aiStatus").innerText = "🟢 Active";
    document.getElementById("dailyProfit").innerText = "+$320";

    const logs = [
        "📌 BUY BTC/USDT @ 43200",
        "📌 SELL ETH/USDT @ 2450",
        "📌 HOLD GOLD"
    ];

    const list = document.getElementById("aiLogs");
    list.innerHTML = "";
    logs.forEach(log => {
        const li = document.createElement("li");
        li.textContent = log;
        list.appendChild(li);
    });
});
