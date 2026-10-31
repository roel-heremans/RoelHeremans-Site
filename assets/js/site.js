// Roel Heremans — small progressive enhancements (no dependencies).
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
