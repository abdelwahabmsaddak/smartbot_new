def chat_answer(question, user_id=None, guest=True):
    """
    SmartBot AI Chat logic
    """

    # 1) Detect asset
    asset = detect_asset(question)  # BTC, ETH, GOLD, AAPL ...

    # 2) Base analysis (always)
    base = analyze_asset(asset)

    # 3) Build response
    response = f"**{asset} Outlook**\n"
    response += f"Trend: {base['trend']}\n"

    if guest:
        response += "Summary: Market shows mixed signals.\n"
        response += "\n🔐 Register to unlock full analysis, whale data & risk levels."
    else:
        response += f"Signal: {base['signal']} ({base['confidence']}%)\n"
        response += f"Risk: {base['risk']}\n"
        response += f"Whales: {base['whales']}\n"
        response += "\n👉 Open dashboard for full view."

    return response
