// theme.js
(function(){
  try{
    const r = document.documentElement;
    const b = document.body;
    const brand  = b?.dataset?.brand  || '#B89B61';
    const brand2 = b?.dataset?.brand2 || '#E7DBBE';
    r.style.setProperty('--brand', brand);
    r.style.setProperty('--brand-2', brand2);
  }catch(_){}
})();
