(function () {
  const bubble = document.getElementById("cwBubble");
  const panel = document.getElementById("cwPanel");
  const closeBtn = document.getElementById("cwClose");
  const body = document.getElementById("cwBody");
  const form = document.getElementById("cwForm");
  const input = document.getElementById("cwInput");

  function openChat() {
    panel.classList.add("open");
    panel.setAttribute("aria-hidden", "false");
    setTimeout(() => input && input.focus(), 50);
  }

  function closeChat() {
    panel.classList.remove("open");
    panel.setAttribute("aria-hidden", "true");
  }

  function addMsg(text, who) {
    const div = document.createElement("div");
    div.className = "cw-msg " + who;
    div.textContent = text;
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
  }

  async function askBot(q) {
    addMsg(q, "user");
    addMsg("Thinking...", "bot");

    // ✅ لاحقًا نربطها بـ API حقيقية: /api/chat
    // حاليا رد بسيط حتى ما يطيّحش الموقع
    const last = body.querySelectorAll(".cw-msg.bot");
    const thinking = last[last.length - 1];

    try {
      // const res = await fetch("/api/chat", { method:"POST", headers:{ "Content-Type":"application/json" }, body: JSON.stringify({ q }) });
      // const data = await res.json();
      // thinking.textContent = data.answer || "OK";

      thinking.textContent = "✅ Got it. (Next step: connect AI endpoint /api/chat)";
    } catch (e) {
      thinking.textContent = "⚠️ Chat is not connected yet.";
    }
  }

  bubble && bubble.addEventListener("click", openChat);
  closeBtn && closeBtn.addEventListener("click", closeChat);

  body && body.addEventListener("click", (e) => {
    const btn = e.target.closest(".cw-q");
    if (btn) askBot(btn.dataset.q || btn.textContent);
  });

  form && form.addEventListener("submit", (e) => {
    e.preventDefault();
    const q = (input.value || "").trim();
    if (!q) return;
    input.value = "";
    askBot(q);
  });
})();
