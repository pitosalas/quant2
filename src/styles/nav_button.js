const tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
for (const t of tabs) {
    if (t.textContent.trim() === NAV_TARGET_LABEL) { t.click(); break; }
}
