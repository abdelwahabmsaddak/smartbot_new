async function loadDashboard() {
  const statusEl = document.getElementById("botStatus");
  const lastUpdateEl = document.getElementById("lastUpdate");
  const tradesOutEl = document.getElementById("tradesOut");

  try {
    statusEl.textContent = "Loading...";
    const res = await fetch("/api/dashboard/live");
    const data = await res.json();

    if (!res.ok || data.status !== "OK") {
      throw new Error(data?.message || "API Error");
    }

    const s = data.stats || {};
    document.getElementById("totalTrades").textContent = s.totalTrades ?? "-";
    document.getElementById("wins").textContent = s.wins ?? "-";
    document.getElementById("losses").textContent = s.losses ?? "-";
    document.getElementById("pnl").textContent = s.pnl ?? "-";

    statusEl.textContent = "Running";
    lastUpdateEl.textContent = "Last update: " + new Date().toLocaleString();

    tradesOutEl.textContent = JSON.stringify(data.trades || [], null, 2);
  } catch (err) {
    statusEl.textContent = "Error";
    lastUpdateEl.textContent = String(err);
    tradesOutEl.textContent = "Failed to load trades.\n" + String(err);
  }
}

loadDashboard();
setInterval(loadDashboard, 5000);
