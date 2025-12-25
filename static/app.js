(function () {
  const dict = {
    en: {
      tagline: "AI Market Intelligence",
      nav_home: "Home",
      nav_analysis: "Analyze",
      nav_blog: "Blog",
      nav_whales: "Whales",
      nav_autotrade: "Auto Trade",
      nav_dashboard: "Dashboard",
      nav_about: "About",
      nav_contact: "Contact",
      nav_terms: "Terms",
      nav_pricing: "Pricing",

      cta_analyze: "Analyze",
      hero_badge: "Tech AI • Market Intelligence",
      hero_title: "Analyze crypto, gold & halal stocks — with AI clarity.",
      hero_subtitle: "One clean place to scan markets, track whales, read insights, and plan smarter entries.",
      cta_start: "Start Analysis",
      cta_whales: "Track Whales",

      meta_1k: "Paper-first",
      meta_1v: "Safe testing before live",
      meta_2k: "Halal focus",
      meta_2v: "Filters for compliant assets",
      meta_3k: "Whale tracker",
      meta_3v: "Follow smart money moves",

      panel_title: "Quick Scan",
      panel_chip: "AI Ready",
      stat_1k: "Mode",
      stat_2k: "Signals",
      stat_3k: "Risk",
      stat_4k: "Status",
      status_ready: "Ready",

      tips_title: "Quick Tips",
      tip_1: "Start with BTC/USDT",
      tip_2: "Use Paper mode first",
      tip_3: "Check Dashboard after Run",
      tip_warn: "Live stays locked until security checks.",

      analyze_title: "Analyze anything in seconds",
      analyze_sub: "Crypto • Gold • Halal Stocks — choose market, enter symbol, and open the analysis page.",
      m_crypto: "Crypto",
      m_gold: "Gold",
      m_halal: "Halal Stocks",
      symbol_label: "Symbol",
      symbol_hint: "Examples: BTC/USDT • XAUUSD • AAPL",
      tf_label: "Timeframe",
      tf_hint: "Used for indicators & signal context.",
      halal_label: "Halal filter",
      halal_auto: "Auto",
      halal_strict: "Strict",
      halal_off: "Off",
      halal_hint: "Strict may reduce results but improves compliance.",
      btn_analyze: "Analyze",
      link_screener: "Open Market Screener",
      link_signals: "AI Signals",
      link_dashboard: "Dashboard",

      blog_title: "From the blog",
      blog_sub: "Short, useful insights — no noise.",
      read_more: "Read",
      blog_p1t: "How to use Paper mode properly",
      blog_p1e: "Avoid classic mistakes before going live.",
      blog_p2t: "Halal stock filtering: practical rules",
      blog_p2e: "Simple framework for compliant screening.",
      blog_p3t: "Whale moves: what matters, what doesn’t",
      blog_p3e: "Signals vs. noise in on-chain alerts.",
      btn_all_posts: "View all posts",

      whale_title: "Whale Tracker",
      whale_sub: "Track big transactions & smart money behavior with clean alerts.",
      btn_open_whales: "Open Whale Page",
      btn_whale_alerts: "Whale Alerts",

      footer_note: "Research-first. Paper mode recommended before live trading."
    },

    ar: {
      tagline: "ذكاء سوقي بالـ AI",
      nav_home: "الرئيسية",
      nav_analysis: "تحليل",
      nav_blog: "المدونة",
      nav_whales: "الحيتان",
      nav_autotrade: "تداول آلي",
      nav_dashboard: "لوحة التحكم",
      nav_about: "من نحن",
      nav_contact: "اتصل بنا",
      nav_terms: "الشروط",
      nav_pricing: "الأسعار",

      cta_analyze: "ابدأ التحليل",
      hero_badge: "تقنية AI • ذكاء سوقي",
      hero_title: "حلّل العملات والذهب والأسهم الحلال — بوضوح AI.",
      hero_subtitle: "مكان واحد مرتب: تحليل، تتبّع حيتان، مقالات مفيدة، وخطة دخول أذكى.",
      cta_start: "ابدأ التحليل",
      cta_whales: "تتبّع الحيتان",

      meta_1k: "Paper أولًا",
      meta_1v: "اختبار آمن قبل اللايف",
      meta_2k: "تركيز حلال",
      meta_2v: "فلترة للأصول المتوافقة",
      meta_3k: "حيتان السوق",
      meta_3v: "تابع حركة الأموال الكبيرة",

      panel_title: "نظرة سريعة",
      panel_chip: "جاهز AI",
      stat_1k: "الوضع",
      stat_2k: "الإشارات",
      stat_3k: "المخاطرة",
      stat_4k: "الحالة",
      status_ready: "جاهز",

      tips_title: "نصائح سريعة",
      tip_1: "ابدأ بـ BTC/USDT",
      tip_2: "استعمل Paper أولًا",
      tip_3: "شوف Dashboard بعد Run",
      tip_warn: "اللايف يبقى مقفول حتى يكمّل فحص الأمان.",

      analyze_title: "حلّل أي أصل في ثواني",
      analyze_sub: "عملات • ذهب • أسهم حلال — اختار السوق، اكتب الرمز، وامشي لصفحة التحليل.",
      m_crypto: "عملات",
      m_gold: "ذهب",
      m_halal: "أسهم حلال",
      symbol_label: "الرمز",
      symbol_hint: "أمثلة: BTC/USDT • XAUUSD • AAPL",
      tf_label: "الإطار الزمني",
      tf_hint: "يستعمل للمؤشرات والسياق.",
      halal_label: "فلتر الحلال",
      halal_auto: "تلقائي",
      halal_strict: "صارم",
      halal_off: "إيقاف",
      halal_hint: "الوضع الصارم يقلل النتائج لكنه يزيد الالتزام.",
      btn_analyze: "حلّل الآن",
      link_screener: "فتح ماسح السوق",
      link_signals: "إشارات AI",
      link_dashboard: "لوحة التحكم",

      blog_title: "من المدونة",
      blog_sub: "مقالات قصيرة ومفيدة بلا ضجيج.",
      read_more: "اقرأ",
      blog_p1t: "كيف تستعمل Paper بشكل صحيح",
      blog_p1e: "تجنب أخطاء كلاسيكية قبل اللايف.",
      blog_p2t: "فلترة الأسهم الحلال: قواعد عملية",
      blog_p2e: "إطار بسيط للفرز المتوافق.",
      blog_p3t: "حركة الحيتان: ما يهم وما لا يهم",
      blog_p3e: "فرق الإشارة عن الضجيج في التنبيهات.",
      btn_all_posts: "عرض كل المقالات",

      whale_title: "تتبّع الحيتان",
      whale_sub: "راقب التحويلات الكبيرة وسلوك الأموال الذكية بتنبيهات نظيفة.",
      btn_open_whales: "افتح صفحة الحيتان",
      btn_whale_alerts: "تنبيهات الحيتان",

      footer_note: "الأفضل البحث أولًا. ننصح بـ Paper قبل التداول الحقيقي."
    }
  };

  function setLang(lang) {
    const html = document.documentElement;
    html.lang = lang === "ar" ? "ar" : "en";
    html.dir = lang === "ar" ? "rtl" : "ltr";

    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.getAttribute("data-i18n");
      if (dict[lang] && dict[lang][key]) el.textContent = dict[lang][key];
    });

    // Placeholder tweak
    const sym = document.getElementById("symbol");
    if (sym) {
      sym.placeholder = (lang === "ar")
        ? "BTC/USDT أو XAUUSD أو AAPL"
        : "BTC/USDT, XAUUSD, AAPL";
    }

    localStorage.setItem("lang", lang);

    // Update pill label
    const pills = document.querySelectorAll(".pill");
    pills.forEach(p => p.textContent = lang === "ar" ? "EN" : "AR");
  }

  function toggleLang() {
    const current = localStorage.getItem("lang") || "en";
    setLang(current === "en" ? "ar" : "en");
  }

  // Mobile drawer
  const burgerBtn = document.getElementById("burgerBtn");
  const drawer = document.getElementById("drawer");
  if (burgerBtn && drawer) {
    burgerBtn.addEventListener("click", () => drawer.classList.toggle("show"));
    drawer.addEventListener("click", (e) => {
      if (e.target.classList.contains("drawer__link")) drawer.classList.remove("show");
    });
  }

  // Lang buttons
  const langBtn = document.getElementById("langBtn");
  const langBtn2 = document.getElementById("langBtn2");
  if (langBtn) langBtn.addEventListener("click", toggleLang);
  if (langBtn2) langBtn2.addEventListener("click", toggleLang);

  // Init
  setLang(localStorage.getItem("lang") || "en");
})();
