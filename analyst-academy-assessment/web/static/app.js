/* Theme toggle, mobile nav, and the exercise-catalogue filter.
   No dependencies. Degrades to a plain readable list with JS disabled. */
(function () {
  "use strict";

  /* ---------- theme ---------- */
  var KEY = "aa-theme";
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function save(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  var saved = stored();
  if (saved === "light" || saved === "dark") {
    document.documentElement.setAttribute("data-theme", saved);
  }

  function currentTheme() {
    var attr = document.documentElement.getAttribute("data-theme");
    if (attr) return attr;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark" : "light";
  }

  function wireTheme() {
    var btns = document.querySelectorAll("[data-theme-toggle]");
    Array.prototype.forEach.call(btns, function (btn) {
      function label() {
        var t = currentTheme();
        btn.textContent = t === "dark" ? "☀" : "☾";
        btn.setAttribute("aria-label", "Switch to " + (t === "dark" ? "light" : "dark") + " theme");
        btn.setAttribute("title", btn.getAttribute("aria-label"));
      }
      label();
      btn.addEventListener("click", function () {
        var next = currentTheme() === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        save(next);
        Array.prototype.forEach.call(btns, function () {});
        label();
      });
    });
  }

  /* ---------- mobile nav ---------- */
  function wireNav() {
    var toggles = document.querySelectorAll("[data-nav-toggle]");
    Array.prototype.forEach.call(toggles, function (t) {
      t.addEventListener("click", function () {
        document.body.classList.toggle("nav-open");
      });
    });
    document.addEventListener("click", function (e) {
      if (!document.body.classList.contains("nav-open")) return;
      var side = document.querySelector(".sidebar");
      if (!side) return;
      if (!side.contains(e.target) && !e.target.closest("[data-nav-toggle]")) {
        document.body.classList.remove("nav-open");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") document.body.classList.remove("nav-open");
    });
  }

  /* ---------- exercise filter ---------- */
  function wireFilter() {
    var list = document.getElementById("exlist");
    if (!list) return;
    var rows = Array.prototype.slice.call(list.querySelectorAll(".exrow"));
    var q = document.getElementById("f-q");
    var mod = document.getElementById("f-module");
    var diff = document.getElementById("f-difficulty");
    var build = document.getElementById("f-build");
    var grade = document.getElementById("f-grading");
    var flagOnly = document.getElementById("f-flagship");
    var count = document.getElementById("f-count");
    var reset = document.getElementById("f-reset");
    var empty = document.getElementById("f-empty");

    function norm(s) { return (s || "").toLowerCase(); }

    function apply() {
      var qv = norm(q && q.value).trim();
      var mv = mod ? mod.value : "";
      var dv = diff ? diff.value : "";
      var bv = build ? build.value : "";
      var gv = grade ? grade.value : "";
      var fo = flagOnly ? flagOnly.checked : false;
      var shown = 0;

      rows.forEach(function (r) {
        var ok = true;
        if (mv && r.dataset.module !== mv) ok = false;
        if (ok && dv && r.dataset.difficulty !== dv) ok = false;
        if (ok && bv && r.dataset.build !== bv) ok = false;
        if (ok && gv && norm(r.dataset.grading).indexOf(norm(gv)) === -1) ok = false;
        if (ok && fo && r.dataset.flagship !== "1") ok = false;
        if (ok && qv && norm(r.dataset.search).indexOf(qv) === -1) ok = false;
        r.hidden = !ok;
        if (ok) shown++;
      });

      if (count) {
        count.textContent = shown === rows.length
          ? rows.length + " exercises"
          : shown + " of " + rows.length + " exercises";
      }
      if (empty) empty.hidden = shown !== 0;
      try {
        var p = new URLSearchParams();
        if (qv) p.set("q", qv);
        if (mv) p.set("m", mv);
        if (dv) p.set("d", dv);
        if (bv) p.set("b", bv);
        if (gv) p.set("g", gv);
        if (fo) p.set("f", "1");
        var s = p.toString();
        history.replaceState(null, "", s ? "?" + s : location.pathname);
      } catch (e) {}
    }

    [q, mod, diff, build, grade].forEach(function (el) {
      if (!el) return;
      el.addEventListener(el.tagName === "SELECT" ? "change" : "input", apply);
    });
    if (flagOnly) flagOnly.addEventListener("change", apply);
    if (reset) reset.addEventListener("click", function () {
      if (q) q.value = "";
      [mod, diff, build, grade].forEach(function (s) { if (s) s.value = ""; });
      if (flagOnly) flagOnly.checked = false;
      apply();
    });

    /* restore state from the URL so filtered views are shareable */
    try {
      var p = new URLSearchParams(location.search);
      if (q && p.get("q")) q.value = p.get("q");
      if (mod && p.get("m")) mod.value = p.get("m");
      if (diff && p.get("d")) diff.value = p.get("d");
      if (build && p.get("b")) build.value = p.get("b");
      if (grade && p.get("g")) grade.value = p.get("g");
      if (flagOnly && p.get("f")) flagOnly.checked = true;
    } catch (e) {}
    apply();
  }

  function init() { wireTheme(); wireNav(); wireFilter(); }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
