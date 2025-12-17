document.getElementById("runBtn").onclick = async () => {
  const payload = {
    asset: document.getElementById("asset").value,
    timeframe: document.getElementById("timeframe").value,
    market: document.getElementById("market").value,
    min_confidence: 65,
    account: {
      balance: 1000,
      risk: 1,
      mode: "paper"
    }
  };

  document.getElementById("status").innerText = "⏳ Running...";

  const res = await fetch("/api/auto-trading-pro/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await res.json();

  document.getElementById("signalOut").textContent =
    JSON.stringify(data.signal, null, 2);

  document.getElementById("execOut").textContent =
    JSON.stringify(data.execution || data.reason, null, 2);

  document.getElementById("status").innerText = data.status;
};
