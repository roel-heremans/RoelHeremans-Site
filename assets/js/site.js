// Roel Heremans — small progressive enhancements (no dependencies):
// phone menu, copy-to-clipboard buttons, fade-in on scroll.
(function () {
  "use strict";

  // Phone/tablet menu (≤ 959px): button toggles the nav panel; Escape, a click
  // outside the header, or widening past the breakpoint closes it.
  var header = document.querySelector(".site-header");
  var toggle = header && header.querySelector(".menu-toggle");
  if (toggle) {
    var setOpen = function (open, focusToggle) {
      header.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      var label = toggle.getAttribute(open ? "data-label-close" : "data-label-open");
      if (label) toggle.setAttribute("aria-label", label);
      if (focusToggle) toggle.focus();
    };
    var isOpen = function () { return header.classList.contains("nav-open"); };
    toggle.addEventListener("click", function () { setOpen(!isOpen()); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && isOpen()) setOpen(false, true);
    });
    document.addEventListener("click", function (e) {
      if (isOpen() && !header.contains(e.target)) setOpen(false);
    });
    var mq = window.matchMedia("(min-width: 960px)");
    var onWide = function () { if (mq.matches) setOpen(false); };
    if (mq.addEventListener) mq.addEventListener("change", onWide); else mq.addListener(onWide);
  }

  // Copy buttons (Contact email): <button data-copy="id-of-element" hidden>. The text stays
  // visible and selectable without JS; with JS the button appears and copies it. If the
  // clipboard is unavailable, the text is selected instead.
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    var source = document.getElementById(btn.getAttribute("data-copy"));
    if (!source) return;
    var status = btn.parentNode.querySelector("[data-copy-status]");
    var label = btn.textContent;
    var timer;
    var done = function (msg) {
      btn.textContent = msg;
      if (status) status.textContent = msg;
      clearTimeout(timer);
      timer = setTimeout(function () {
        btn.textContent = label;
        if (status) status.textContent = "";
      }, 1800);
    };
    var select = function () {
      var range = document.createRange();
      range.selectNodeContents(source);
      var sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
      done(btn.getAttribute("data-label-selected") || label);
    };
    btn.hidden = false;
    btn.addEventListener("click", function () {
      var text = source.textContent.trim();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          done(btn.getAttribute("data-label-done") || label);
        }, select);
      } else {
        select();
      }
    });
  });

  // Opt-in fade-up on scroll: add data-reveal to an element.
  var items = document.querySelectorAll("[data-reveal]");
  if (!("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("is-visible"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: "0px 0px -10% 0px" });
  items.forEach(function (el) { io.observe(el); });
})();
