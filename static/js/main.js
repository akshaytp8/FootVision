/**
 * main.js — LosBlancos Zone
 * Minimal JavaScript — 3 small helpers only.
 */

// 1. Highlight the selected outcome radio button
function initOutcomeRadios() {
  const labels = document.querySelectorAll(".outcome-label");
  labels.forEach(label => {
    const radio = label.querySelector("input[type='radio']");
    if (!radio) return;
    if (radio.checked) label.classList.add("selected");
    radio.addEventListener("change", () => {
      labels.forEach(l => l.classList.remove("selected"));
      label.classList.add("selected");
    });
  });
}

// 2. Auto-suggest outcome from score inputs
function initScoreSync() {
  const home = document.querySelector("input[name='home_score']");
  const away = document.querySelector("input[name='away_score']");
  if (!home || !away) return;

  function sync() {
    const h = parseInt(home.value) || 0;
    const a = parseInt(away.value) || 0;
    const val = h > a ? "home_win" : h < a ? "away_win" : "draw";
    document.querySelectorAll("input[name='outcome']").forEach(r => {
      if (r.value === val) { r.checked = true; r.dispatchEvent(new Event("change")); }
    });
  }
  home.addEventListener("input", sync);
  away.addEventListener("input", sync);
}

// 3. Auto-dismiss flash messages after 5 seconds
function initFlashDismiss() {
  document.querySelectorAll(".flash").forEach(f => {
    setTimeout(() => {
      f.style.transition = "opacity 0.5s";
      f.style.opacity = "0";
      setTimeout(() => f.remove(), 500);
    }, 5000);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initOutcomeRadios();
  initScoreSync();
  initFlashDismiss();
});

// 4. Supporter logo popup toggle
function initSupporterPopup() {
  const btn   = document.getElementById("supporterBtn");
  const popup = document.getElementById("supporterPopup");
  if (!btn || !popup) return;

  // Toggle popup when logo clicked
  btn.addEventListener("click", function(e) {
    e.stopPropagation();
    popup.classList.toggle("open");
  });

  // Close popup if user clicks anywhere else
  document.addEventListener("click", function() {
    popup.classList.remove("open");
  });
}

document.addEventListener("DOMContentLoaded", function() {
  initSupporterPopup();
});
