@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json or {}
    question = data.get("message", "").strip()

    if not question:
        return jsonify({"answer": "❗ Please type a question."})

    user_id = session.get("user_id")
    is_guest = user_id is None

    answer = chat_answer(
        question=question,
        user_id=user_id,
        guest=is_guest
    )

    return jsonify({"answer": answer})
