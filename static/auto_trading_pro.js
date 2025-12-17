document.addEventListener("DOMContentLoaded", () => {
  const runBtn = document.getElementById("runAutoTradingPro");
  const statusBox = document.getElementById("runStatus");
  const outputBox = document.getElementById("runOutput");

  if (!runBtn) return;

  runBtn.addEventListener("click", async () => {
    statusBox.textContent = "⏳ جاري التنفيذ...";
    statusBox.className = "status loading";
    outputBox.textContent = "";

    const payload = {
      asset: document.getElementById("asset").value,
      timeframe: document.getElementById("timeframe").value,
      market: document.getElementById("market").value,
      halal_strict: document.getElementById("halal_strict")?.checked || false,
      account: {
        balance: parseFloat(document.getElementById("balance").value || 1000),
        risk: parseFloat(document.getElementById("risk").value || 1),
        mode: document.getElementById("mode").value, // paper | live
        exchange: document.getElementById("exchange").value
      }
    };

    try {
      const res = await fetch("/api/auto-trading-pro/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok || data.status === "error") {
        throw new Error(data.message || "Execution failed");
      }

      statusBox.textContent = "✅ تم التنفيذ بنجاح";
      statusBox.className = "status success";

      outputBox.textContent = JSON.stringify(data.result, null, 2);

    } catch (err) {
      statusBox.textContent = "❌ خطأ في التنفيذ";
      statusBox.className = "status error";
      outputBox.textContent = err.message;
    }
  });
});
