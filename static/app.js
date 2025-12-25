(() => {
  const btn = document.getElementById('langBtn');
  if(!btn) return;
  btn.onclick = () => {
    const ar = document.documentElement.lang !== 'ar';
    document.documentElement.lang = ar ? 'ar' : 'en';
    document.documentElement.dir = ar ? 'rtl' : 'ltr';
    btn.textContent = ar ? 'EN' : 'AR';
  };
})();
