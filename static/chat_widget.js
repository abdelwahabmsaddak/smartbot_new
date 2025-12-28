async function askBot(q) {
  addMsg(q, "user");
  addMsg("Thinking...", "bot");

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ q })
  });

  const data = await res.json();
  replaceLastBotMsg(data.answer);
}
