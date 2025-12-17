document.addEventListener("DOMContentLoaded", () => {
  const runBtn = document.getElementById("runBtn");
  const status = document.getElementById("status");
  const signalOut = document.getElementById("signalOut");
  const execOut = document.getElementById("execOut");

  if (!runBtn) return;

  runBtn.addEventListener("click", async () => {
    status.textContent = "⏳ Running...";
    signalOut.textContent = "";
    execOut.textContent = "";

    const payload = {
      asset: document.getElementById("asset").value,
      timeframe: document.getElementById("timeframe").value,
      market: document.getElementById("market").value,
      min_confidence: 60,
      account: {
        balance: 1000,
        risk: 1,
        mode: document.getElementById("mode").value,
        exchange: document.getElementById("exchange").value,
        order_type: document.getElementById("order_type").value
      }
    };

    try {
      const res = await fetch("/api/auto-trading-pro/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok || data.status === "ERROR") {
        throw new Error(data.message || "Execution failed");
      }

      status.textContent = "✅ Done";
      signalOut.textContent = JSON.stringify(data.signal, null, 2);
      execOut.textContent = JSON.stringify(data.execution, null, 2);

    } catch (e) {
      status.textContent = "❌ Error";
      execOut.textContent = e.message;
    }
  });
});
