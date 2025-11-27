translations = {
    "en": {
        "dashboard": "Dashboard",
        "profile": "Profile",
        "logout": "Logout",
        "settings": "Settings",
        "market_screener": "Market Screener",
        "auto_trading": "Auto Trading",
        "ai_signals": "AI Signals",
        "whale_alerts": "Whale Alerts"
    },

    "ar": {
        "dashboard": "لوحة التحكم",
        "profile": "الملف الشخصي",
        "logout": "تسجيل الخروج",
        "settings": "الإعدادات",
        "market_screener": "سكانر السوق",
        "auto_trading": "التداول الآلي",
        "ai_signals": "إشارات الذكاء الاصطناعي",
        "whale_alerts": "تنبيهات الحيتان"
    }
}


def translate(lang, key):
    if lang not in translations:
        lang = "en"
    return translations[lang].get(key, key)
