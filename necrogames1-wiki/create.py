#!/usr/bin/env python3
import sys
import os

TRANSLIT_MAP = {
	'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z',
	'и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
	'с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'ts','ч':'ch','ш':'sh','щ':'sch',
	'ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya',
	' ':'_','-':'-'
}

def translit(text):
	result = ""
	for ch in text.lower():
		result += TRANSLIT_MAP.get(ch, ch)
	return result

def main():
	if len(sys.argv) != 3:
		print("Usage: script.py <category> <name>")
		sys.exit(1)

	category = sys.argv[1]
	name = sys.argv[2]

	name_translit = translit(name)

	dir_path = os.path.join("pages", category)
	os.makedirs(dir_path, exist_ok=True)

	file_path = os.path.join(dir_path, f"{name_translit}.html")

	html_content = f"""<!DOCTYPE html>
<html lang="ru" data-wiki-accent="indigo">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{name}</title>
  <link rel="stylesheet" href="../../css/wiki.css">
</head>
<body>
  <div class="wiki-shell">
    <header class="wiki-masthead">
      <h1 class="wiki-masthead__title"><a href="../../index.html">NecroGames Wiki</a></h1>
      <p class="wiki-masthead__tagline">Статическая вики в стиле классических fan-wiki.</p>
    </header>

    <main class="wiki-paper">
      <div class="wiki-article-grid">
        <div class="wiki-article-main">
          <div id="wiki-body" class="wiki-body" aria-live="polite"></div>
        </div>

        <aside class="wiki-infobox" aria-label="Сводка по сюжету">
          <figure class="wiki-infobox__figure">
            <img src="../../media/portrait-placeholder.svg" width="200" height="257" alt="Схематичная иллюстрация">
          </figure>
          <h2 class="wiki-infobox__title">{name}</h2>

          <h3 class="wiki-infobox__section-title"></h3>
          <table class="wiki-infobox__table">
            <tbody>
              <tr>
                <th scope="row">заголовок</th>
                <td>
                  <ul>
                    <li><a href="nekromant.html">строка</a></li>
                  </ul>
                </td>
              </tr>
            </tbody>
          </table>

          <h3 class="wiki-infobox__section-title"></h3>
          <table class="wiki-infobox__table">
            <tbody>
              <tr>
                <th scope="row">заголовок</th>
                <td>
                  <ul>
                    <li><a href="nekromant.html">строка</a></li>
                  </ul>
                </td>
              </tr>
            </tbody>
          </table>
          
        </aside>
      </div>
    </main>

    <footer class="wiki-footer">
      <a href="../../index.html">← На главную</a>
    </footer>
  </div>

  <script id="wiki-md" type="text/plain">
# {name}

  </script>

  <script src="../../js/marked.min.js"></script>
  <script src="../../js/wiki-render.js"></script>
</body>
</html>
"""

	with open(file_path, "w", encoding="utf-8") as f:
		f.write(html_content)

	print(f"Created: {file_path}")

if __name__ == "__main__":
	main()