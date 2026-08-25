/* HA International Chemicals — interaction layer
   Ripple, scroll reveals, count-ups, hero slider, nav drawer. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Short page transition with no forced waiting. */
  function clearTransition() {
    document.documentElement.classList.remove("is-loading", "is-transitioning");
  }

  document.documentElement.classList.add("is-loading");
  window.addEventListener("pageshow", function () {
    window.requestAnimationFrame(clearTransition);
  });
  window.addEventListener("load", clearTransition);
  setTimeout(clearTransition, 1400);

  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var link = e.target.closest ? e.target.closest("a[href]") : null;
    if (!link || link.target === "_blank" || link.hasAttribute("download")) return;
    var href = link.getAttribute("href");
    if (!href || href.charAt(0) === "#" || /^(mailto:|tel:|javascript:)/i.test(href)) return;
    var destination;
    try { destination = new URL(link.href, window.location.href); } catch (ignore) { return; }
    if (destination.origin !== window.location.origin) return;
    if (destination.pathname === window.location.pathname && destination.search === window.location.search && destination.hash) return;
    document.documentElement.classList.add("is-transitioning");
  });

  /* ------------------------------------------------------------------
     Ripple — pointer-origin bloom.
     Vanilla port of interior.dev/docs/ripple: bloom .5s linear from the
     exact pointer coordinate, fade 320ms on cubic-bezier(.23,1,.32,1),
     40px base circle scaled to reach the furthest corner, max 4 live.
     ------------------------------------------------------------------ */
  var RIPPLE_MAX = 4;
  var FADE_MS = 320;

  function layerFor(host) {
    var layer = host.querySelector(":scope > .ripple-layer");
    if (!layer) {
      layer = document.createElement("span");
      layer.className = "ripple-layer";
      layer.setAttribute("aria-hidden", "true");
      host.appendChild(layer);
    }
    return layer;
  }

  function spawn(host, clientX, clientY) {
    if (reduceMotion || host.hasAttribute("disabled")) return;

    var rect = host.getBoundingClientRect();
    if (!rect.width || !rect.height) return;

    // centre the ripple when triggered by keyboard (no pointer coords)
    var x = clientX == null ? rect.width / 2 : clientX - rect.left;
    var y = clientY == null ? rect.height / 2 : clientY - rect.top;

    // scale a 40px circle until it covers the furthest corner
    var far = Math.max(
      Math.hypot(x, y),
      Math.hypot(rect.width - x, y),
      Math.hypot(x, rect.height - y),
      Math.hypot(rect.width - x, rect.height - y)
    );

    var layer = layerFor(host);
    while (layer.childElementCount >= RIPPLE_MAX) {
      layer.removeChild(layer.firstElementChild);
    }

    var dot = document.createElement("span");
    dot.className = "ripple";
    dot.style.left = x + "px";
    dot.style.top = y + "px";
    dot.style.setProperty("--ripple-scale", (far / 20) + 1);
    layer.appendChild(dot);
    return dot;
  }

  function release(host) {
    var layer = host.querySelector(":scope > .ripple-layer");
    if (!layer) return;
    Array.prototype.forEach.call(layer.children, function (dot) {
      if (dot.classList.contains("is-releasing")) return;
      dot.classList.add("is-releasing");
      setTimeout(function () {
        if (dot.parentNode) dot.parentNode.removeChild(dot);
      }, FADE_MS + 60);
    });
  }

  function rippleHost(target) {
    return target.closest ? target.closest("[data-ripple]") : null;
  }

  document.addEventListener("pointerdown", function (e) {
    var host = rippleHost(e.target);
    if (host) spawn(host, e.clientX, e.clientY);
  }, { passive: true });

  ["pointerup", "pointercancel", "pointerleave"].forEach(function (evt) {
    document.addEventListener(evt, function (e) {
      var host = rippleHost(e.target);
      if (host) release(host);
    }, { passive: true });
  });

  // keyboard parity — Space/Enter spawn a centred ripple
  document.addEventListener("keydown", function (e) {
    if (e.key !== " " && e.key !== "Enter" && e.key !== "Spacebar") return;
    if (e.repeat) return;
    var host = rippleHost(e.target);
    if (host) spawn(host, null, null);
  });
  document.addEventListener("keyup", function (e) {
    if (e.key !== " " && e.key !== "Enter" && e.key !== "Spacebar") return;
    var host = rippleHost(e.target);
    if (host) release(host);
  });
  document.addEventListener("blur", function (e) {
    var host = rippleHost(e.target);
    if (host) release(host);
  }, true);

  /* ------------------------------------------------------------------
     Scroll reveals
     ------------------------------------------------------------------ */
  function inViewport(el) {
    var r = el.getBoundingClientRect();
    return r.top < (window.innerHeight || 0) && r.bottom > 0;
  }

  function activate(el) {
    el.classList.add("is-visible");
    // the counter/progress hook may sit on the revealed element itself or on
    // a child of it, so check both
    if (el.hasAttribute("data-count")) runCount(el);
    el.querySelectorAll("[data-count]").forEach(runCount);
    if (el.hasAttribute("data-progress")) runProgress(el);
    el.querySelectorAll("[data-progress]").forEach(runProgress);
  }

  function initReveals() {
    var items = document.querySelectorAll("[data-reveal]");
    if (!items.length) return;

    if (reduceMotion || !("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(items, activate);
      return;
    }

    var pending = Array.prototype.slice.call(items);

    function take(el) {
      var n = pending.indexOf(el);
      if (n > -1) pending.splice(n, 1);
      activate(el);
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        take(entry.target);
        io.unobserve(entry.target);
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });

    Array.prototype.forEach.call(items, function (el) { io.observe(el); });

    // Safety net. IntersectionObserver can be suspended (a backgrounded or
    // non-rendered document delivers nothing), and content that never
    // reveals is content the user can never read. A cheap geometric sweep
    // on scroll guarantees anything on screen becomes visible regardless.
    function sweep() {
      if (!pending.length) {
        window.removeEventListener("scroll", onScroll);
        window.removeEventListener("resize", onScroll);
        return;
      }
      pending.slice().forEach(function (el) {
        if (inViewport(el)) {
          io.unobserve(el);
          take(el);
        }
      });
    }

    var queued = false;
    function onScroll() {
      if (queued) return;
      queued = true;
      setTimeout(function () { queued = false; sweep(); }, 120);
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    sweep();
  }

  /* ------------------------------------------------------------------
     Count-ups + progress bars
     ------------------------------------------------------------------ */
  function runCount(el) {
    if (el.dataset.counted) return;
    el.dataset.counted = "1";
    var target = parseInt(el.getAttribute("data-count"), 10) || 0;
    if (reduceMotion) { el.textContent = target.toLocaleString(); return; }

    var dur = 1600, start = null, done = false;
    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased).toLocaleString();
      if (p < 1) requestAnimationFrame(step);
      else done = true;
    }
    requestAnimationFrame(step);
    // rAF is paused in a hidden document — never leave the number stuck at 0
    setTimeout(function () {
      if (!done) el.textContent = target.toLocaleString();
    }, dur + 400);
  }

  function runProgress(el) {
    if (el.dataset.filled) return;
    el.dataset.filled = "1";
    var pct = parseInt(el.getAttribute("data-progress"), 10) || 0;
    var fill = el.querySelector(".progress__fill");
    var num = el.querySelector("[data-progress-num]");
    // setTimeout rather than rAF: still lets the CSS transition pick up the
    // change, but works in a hidden document where rAF is suspended
    if (fill) setTimeout(function () { fill.style.width = pct + "%"; }, 20);
    if (num) {
      if (reduceMotion) { num.textContent = pct + "%"; return; }
      var dur = 1400, start = null, done = false;
      requestAnimationFrame(function step(ts) {
        if (start === null) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        num.textContent = Math.round(pct * (1 - Math.pow(1 - p, 3))) + "%";
        if (p < 1) requestAnimationFrame(step);
        else done = true;
      });
      setTimeout(function () {
        if (!done) num.textContent = pct + "%";
      }, dur + 400);
    }
  }

  /* ------------------------------------------------------------------
     Hero slider — crossfade + Ken Burns
     ------------------------------------------------------------------ */
  function initHero() {
    var slides = document.querySelectorAll(".hero__slide");
    if (slides.length < 2) return;
    var dots = document.querySelectorAll(".hero__dots button");
    var i = 0, timer = null, DELAY = 7000;

    function show(n) {
      slides[i].classList.remove("is-active");
      if (dots[i]) dots[i].classList.remove("is-active");
      i = n % slides.length;
      slides[i].classList.add("is-active");
      if (dots[i]) dots[i].classList.add("is-active");
    }
    function start() {
      if (reduceMotion || timer) return;
      timer = setInterval(function () { show(i + 1); }, DELAY);
    }
    function stop() { clearInterval(timer); timer = null; }

    Array.prototype.forEach.call(dots, function (dot, n) {
      dot.addEventListener("click", function () { stop(); show(n); start(); });
    });

    // don't animate while the tab is hidden
    document.addEventListener("visibilitychange", function () {
      document.hidden ? stop() : start();
    });
    start();
  }

  /* ------------------------------------------------------------------
     Sticky header state
     ------------------------------------------------------------------ */
  function initHeader() {
    var header = document.querySelector("header.site");
    if (!header) return;
    var ticking = false;
    function apply() {
      try {
        header.classList.toggle("is-scrolled", window.scrollY > 80);
      } finally {
        ticking = false;
      }
    }
    function onScroll() {
      if (ticking) return;
      ticking = true;
      // rAF where available for smoothness, timeout as the fallback so the
      // header state still tracks in a suspended document
      if (typeof requestAnimationFrame === "function") requestAnimationFrame(apply);
      else setTimeout(apply, 16);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ------------------------------------------------------------------
     Mobile nav drawer
     ------------------------------------------------------------------ */
  function initNav() {
    var toggle = document.getElementById("menuToggle");
    var nav = document.getElementById("mainNav");
    if (!toggle || !nav) return;

    var links = nav.querySelectorAll("a");
    Array.prototype.forEach.call(links, function (a, n) {
      a.style.setProperty("--n", n);
    });

    function setOpen(open) {
      nav.classList.toggle("open", open);
      toggle.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
    }

    toggle.setAttribute("aria-expanded", "false");
    toggle.addEventListener("click", function () {
      setOpen(!nav.classList.contains("open"));
    });
    Array.prototype.forEach.call(links, function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    // reset when resizing back to desktop
    window.addEventListener("resize", function () {
      if (window.innerWidth > 760 && nav.classList.contains("open")) setOpen(false);
    });
  }

  /* ------------------------------------------------------------------
     Quote deep-link — product pages link through as ?quote_product=<slug>,
     so arrive with the enquiry already started rather than a blank box.
     ------------------------------------------------------------------ */
  function initQuotePrefill() {
    var slug = new URLSearchParams(window.location.search).get("quote_product");
    if (!slug) return;
    var name = slug.replace(/-/g, " ").replace(/\b\w/g, function (c) {
      return c.toUpperCase();
    });
    var fields = document.querySelectorAll(
      '#ms, textarea[name="mf-textarea"], input[name="wpforms[fields][8]"]'
    );
    Array.prototype.forEach.call(fields, function (field) {
      if (!field.value) field.value = "I'd like a quote for " + name + " — quantity: ";
    });
    var heading = document.querySelector(".hachemicals-form-shell h2");
    if (heading) heading.textContent = "Request a Quote — " + name;
  }

  /* ------------------------------------------------------------------
     Form accessibility — MetForm marks required fields visually but its
     rendered markup omits native required semantics. Keep the plugin's AJAX
     and delivery pipeline intact while synchronising labels and constraints.
     ------------------------------------------------------------------ */
  function syncMetFormAccessibility() {
    document.querySelectorAll(".mf-input-wrapper").forEach(function (wrapper) {
      var field = wrapper.querySelector("input:not([type=hidden]), textarea, select");
      var label = wrapper.querySelector("label");
      if (!field) return;
      if (label && label.querySelector(".mf-input-required-indicator")) {
        field.required = true;
        field.setAttribute("aria-required", "true");
      }
      if (label && field.id && label.getAttribute("for") !== field.id) {
        label.setAttribute("for", field.id);
      }
    });
  }

  function initFormAccessibility() {
    syncMetFormAccessibility();
    if (!("MutationObserver" in window) || !document.body) return;
    var observer = new MutationObserver(syncMetFormAccessibility);
    observer.observe(document.body, { childList: true, subtree: true });
    setTimeout(function () { observer.disconnect(); }, 10000);
  }

  /* ------------------------------------------------------------------ */
  function init() {
    initReveals();
    initHero();
    initHeader();
    initNav();
    initQuotePrefill();
    initFormAccessibility();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
