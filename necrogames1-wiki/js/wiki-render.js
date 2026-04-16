/**
 * Renders Markdown from <script id="wiki-md" type="text/plain">…</script>
 * into <div id="wiki-body" class="wiki-body"></div>.
 * Expects global `marked` (marked.min.js).
 */
(function () {
  "use strict";

  function getMarkdownSource() {
    var el = document.getElementById("wiki-md");
    if (!el) return "";
    return el.textContent.replace(/^\n+/, "").replace(/\n+$/, "");
  }

  function configureMarked() {
    if (typeof marked === "undefined" || !marked.parse) {
      console.error("wiki-render: marked is not loaded");
      return false;
    }
    marked.setOptions({
      gfm: true,
      breaks: false,
      headerIds: true,
      mangle: false,
    });
    return true;
  }

  function render() {
    var out = document.getElementById("wiki-body");
    if (!out) return;

    if (!configureMarked()) {
      out.innerHTML =
        "<p>Не удалось загрузить парсер Markdown (<code>marked</code>).</p>";
      return;
    }

    var md = getMarkdownSource();
    out.innerHTML = marked.parse(md);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
})();
