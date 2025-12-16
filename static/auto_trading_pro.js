function setStatus(text, ok = true) {
  const el = document.getElementById("status");
  el.textContent = text;
  el.style.borderColor = ok ? "#22c55e" : "#ef4444";
  el.style.color = ok ? "#22c55e" : "#ef4444";
}

function pretty(obj) {
  try { return JSON.stringify(obj, null, 2); }
  catch { return String(obj); }
}

document.addEventListener("DOMContentLoaded", () => {
  const runBtn = document.getElementById("runBtn");

  runBtn.addEventListener("click", async () => {
    const asset = document.getElementById("asset").value.trim();
    const market = document.getElementById("market").value;
    const timeframe = document.getElementById("timeframe").value;
    const halal_strict = document.getElementById("halal_strict").checked;
    const min_confidence = Number(document.getElementById("min_confidence").value || 0);

    const balance = Number(document.getElementById("balance").value || 0);
    const risk = Number(document.getElementById("risk").value || 1);
    const mode = document.getElementById("mode").value;
    const exchange = document.getElementById("exchange").value.trim() || "binance";
    const type = document.getElementById("order_type").value;

    const signalOut = document.getElementById("signalOut");
    const execOut = document.getElementById("execOut");

    signalOut.textContent = "--";
    execOut.textContent = "--";

    if (!asset) {
      setStatus("❌ لازم Asset", false);
      return;
    }
    if (balance <= 0) {
      setStatus("❌ Balance لازم يكون > 0", false);
      return;
    }

    setStatus("⏳ Running...", true);
    runBtn.disabled = true;

    const payload = {
      asset,
      timeframe,
      market,
      halal_strict,
      min_confidence,
      account: {
        symbol: asset,
        balance,
        risk,
        mode,
        exchange,
        type
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
        setStatus("❌ Error: " + (data.message || data.error || "Unknown"), false);
        signalOut.textContent = pretty(data);
        return;
      }

      // حالات: OK / SKIPPED
      if (data.status === "SKIPPED") {
        setStatus("⚠️ Skipped: " + (data.reason || "Low confidence"), false);
      } else {
        setStatus("✅ Done", true);
      }

      signalOut.textContent = pretty(data.signal || data);
      execOut.textContent = pretty(data.execution || data);

    } catch (e) {
      setStatus("❌ Network/Server error: " + e.message, false);
    } finally {
      runBtn.disabled = false;
    }
  });
});
