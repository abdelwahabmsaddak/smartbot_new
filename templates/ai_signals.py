<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8" />
    <title>AI Signals</title>
    <link rel="stylesheet" href="/static/style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body>

<div class="container">

    <h2>🤖 إشارات الذكاء الاصطناعي</h2>

    <div class="input-box">
        <label>ادخل الرمز:</label>
        <input type="text" id="symbol" placeholder="مثال: BTCUSDT أو AAPL">
    </div>

    <div class="input-box">
        <label>نوع الإشارة:</label>
        <select id="signal_type">
            <option value="scalping">Scalping</option>
            <option value="swing">Swing</option>
            <option value="long">Long Term</option>
        </select>
    </div>

    <button onclick="loadSignal()">عرض الإشارة 🔍</button>

    <hr>

    <h3>📊 النتيجة:</h3>
    <div id="ai_result" class="box"></div>

    <canvas id="ai_chart" height="120"></canvas>

</div>


<script>
function loadSignal() {
    let symbol = document.getElementById("symbol").value;
    let signal_type = document.getElementById("signal_type").value;

    document.getElementById("ai_result").innerHTML = "⏳ جاري التحليل...";

    fetch("/api/ai_signal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({symbol, signal_type})
    })
    .then(res => res.json())
    .then(data => {

        document.getElementById("ai_result").innerHTML = `
            <p>🔮 <strong>التوقع:</strong> ${data.prediction}</p>
            <p>📈 <strong>نسبة الثقة:</strong> ${data.confidence}%</p>
            <p>📅 <strong>الإطار الزمني:</strong> ${data.timeframe}</p>
        `;

        let ctx = document.getElementById("ai_chart").getContext("2d");
        new Chart(ctx, {
            type: "line",
            data: {
                labels: data.chart.labels,
                datasets: [{
                    label: symbol,
                    data: data.chart.values,
                    borderWidth: 2,
                    borderColor: "blue"
                }]
            }
        });

    });
}
</script>

</body>
</html>
