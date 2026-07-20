var doc = window.parent.document;
var el = doc.querySelector('[data-testid="stMain"]')
    || doc.querySelector('[data-testid="stAppViewContainer"]');
if (el) { el.scrollTo(0, 0); }
window.parent.scrollTo(0, 0);
