/* ============================================================
   Western Forms Inc — interactions
   ============================================================ */
(function () {
  "use strict";

  /* --- Page load curtain --- */
  window.addEventListener("load", function () {
    document.body.classList.add("loaded");
  });
  // Fallback in case load already fired
  if (document.readyState === "complete") document.body.classList.add("loaded");

  /* --- Current year --- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* --- Sticky nav background on scroll --- */
  var nav = document.getElementById("nav");
  function onScrollNav() {
    if (window.scrollY > 40) nav.classList.add("scrolled");
    else nav.classList.remove("scrolled");
  }
  onScrollNav();

  /* --- Mobile menu toggle --- */
  var toggle = document.getElementById("navToggle");
  var links = document.querySelector(".nav__links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("open");
        toggle.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* --- Reveal on scroll (IntersectionObserver) --- */
  var revealEls = document.querySelectorAll(".reveal, .reveal-img, .card");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -8% 0px" }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* --- Staggered reveal for the work cards --- */
  document.querySelectorAll("#workGrid .card").forEach(function (card, i) {
    card.style.transitionDelay = (i * 90) + "ms";
  });

  /* --- Animated stat counters --- */
  var counters = document.querySelectorAll("[data-count]");
  function animateCount(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var dur = 1400;
    var start = performance.now();
    function tick(now) {
      var p = Math.min((now - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
      el.textContent = Math.round(eased * target).toString();
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  if ("IntersectionObserver" in window) {
    var countIO = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCount(entry.target);
            countIO.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.6 }
    );
    counters.forEach(function (el) { countIO.observe(el); });
  } else {
    counters.forEach(function (el) { el.textContent = el.getAttribute("data-count"); });
  }

  /* --- Lightweight parallax (rAF-throttled) --- */
  var parallaxEls = document.querySelectorAll("[data-parallax]");
  var ticking = false;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function applyParallax() {
    var y = window.scrollY;
    parallaxEls.forEach(function (el) {
      var speed = parseFloat(el.getAttribute("data-parallax")) || 0.2;
      el.style.transform = "translate3d(0," + (y * speed).toFixed(1) + "px,0)";
    });
    ticking = false;
  }
  function onScroll() {
    onScrollNav();
    if (!reduceMotion && !ticking) {
      ticking = true;
      requestAnimationFrame(applyParallax);
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  /* --- Pointer-tracked tilt on work cards --- */
  if (!reduceMotion && window.matchMedia("(hover: hover)").matches) {
    document.querySelectorAll("#workGrid .card").forEach(function (card) {
      card.addEventListener("pointermove", function (e) {
        var r = card.getBoundingClientRect();
        var cx = (e.clientX - r.left) / r.width - 0.5;
        var cy = (e.clientY - r.top) / r.height - 0.5;
        var media = card.querySelector(".card__media");
        if (media) {
          media.style.transform =
            "scale(1.12) translate(" + (cx * -14).toFixed(1) + "px," + (cy * -14).toFixed(1) + "px)";
        }
      });
      card.addEventListener("pointerleave", function () {
        var media = card.querySelector(".card__media");
        if (media) media.style.transform = "";
      });
    });
  }

  /* --- Quote form (front-end only demo) --- */
  var form = document.getElementById("quoteForm");
  var note = document.getElementById("formNote");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = form.querySelector('[name="name"]').value.trim();
      var email = form.querySelector('[name="email"]').value.trim();
      if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        note.textContent = "Please enter your name and a valid email.";
        note.style.color = "#ff7a7a";
        return;
      }
      note.style.color = "";
      note.textContent = "Thanks, " + name + "! Our Kansas City team will be in touch shortly.";
      form.reset();
    });
  }
})();
