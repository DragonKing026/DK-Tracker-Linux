// DK Tracker — project page: language and theme switches, copying the install command.
// The first choice (browser language, system theme) is made in the <head> before the first paint.
(function () {
  "use strict";
  var root = document.documentElement;
  var titles = {
    pl: document.title,
    en: "DK Tracker — Kimai time tracking in the Linux system tray",
  };

  function save(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (e) {
      // Private window or blocked storage: the choice lasts until the page is closed.
    }
  }

  function showLang(lang) {
    root.dataset.lang = lang;
    root.lang = lang;
    document.title = titles[lang];
    document.querySelectorAll("[data-set-lang]").forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.dataset.setLang === lang));
    });
  }

  document.querySelectorAll("[data-set-lang]").forEach(function (button) {
    button.addEventListener("click", function () {
      showLang(button.dataset.setLang);
      save("dk-lang", button.dataset.setLang);
    });
  });
  showLang(root.dataset.lang === "en" ? "en" : "pl");

  var systemDark = window.matchMedia("(prefers-color-scheme: dark)");
  document.querySelectorAll("[data-toggle-theme]").forEach(function (button) {
    button.addEventListener("click", function () {
      var dark = root.dataset.theme ? root.dataset.theme === "dark" : systemDark.matches;
      root.dataset.theme = dark ? "light" : "dark";
      save("dk-theme", root.dataset.theme);
    });
  });

  function copied(button) {
    button.classList.add("is-done");
    setTimeout(function () {
      button.classList.remove("is-done");
    }, 1800);
  }

  document.querySelectorAll("[data-copy]").forEach(function (button) {
    button.addEventListener("click", function () {
      var code = button.closest("[data-copy-box]").querySelector("code");
      var text = code.textContent.trim();
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function () {
          copied(button);
        });
        return;
      }
      var range = document.createRange();
      range.selectNodeContents(code);
      var selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      try {
        if (document.execCommand("copy")) copied(button);
      } catch (e) {
        // Left selected: Ctrl+C still works.
      }
    });
  });
})();
