async function loadDashboard() {
  try {
    const res = await fetch("/api/dashboard/live");
    const data = await res.json();

    if (data.status !== "OK") throw new Error();

    document.getElementById("totalTrades").textContent = data.stats.total_trades;
    document.getElementById("wins").textContent = data.stats.wins;
    document.getElementById("losses").textContent = data.stats.losses;
    document.getElementById("pnl").textContent = data.stats.pnl;

    document.getElementById("tradesOut").textContent =
      JSON.stringify(data.trades, null, 2);

  } catch {
    document.getElementById("tradesOut").textContent = "Error loading data";
  }
}

// تحديث كل 5 ثواني
setInterval(loadDashboard, 5000);
loadDashboard();
