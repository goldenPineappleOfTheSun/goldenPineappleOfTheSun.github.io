#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пересобирает блок карты сайта в index.html между маркерами:
  <!-- SITE-MAP-START -->
  <!-- SITE-MAP-END -->

Обходит pages/**/*.html, группирует по имени непосредственной подпапки pages/
(«категория»), вставляет списки ссылок с href от корня сайта (как в index.html).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


START = "<!-- SITE-MAP-START -->"
END = "<!-- SITE-MAP-END -->"


def wiki_root_from_script() -> Path:
    return Path(__file__).resolve().parent


def page_link_label(html: str, fallback_stem: str) -> str:
    m = re.search(r"<title>\s*([^<]+?)\s*</title>", html, re.I | re.DOTALL)
    if not m:
        return fallback_stem.replace("_", " ")
    title = " ".join(m.group(1).split())
    for sep in (" — ", " – ", " - "):
        if sep in title:
            title = title.split(sep)[0].strip()
            break
    return title or fallback_stem


def collect_pages(pages_dir: Path) -> list[tuple[str, Path]]:
    """List of (category_name, path) sorted for stable output."""
    out: list[tuple[str, Path]] = []
    if not pages_dir.is_dir():
        return out
    for p in sorted(pages_dir.rglob("*.html")):
        try:
            rel = p.resolve().relative_to(pages_dir.resolve())
        except ValueError:
            continue
        parts = rel.parts
        if len(parts) == 1:
            category = ""
        else:
            category = parts[0]
        out.append((category, p))
    out.sort(key=lambda t: (t[0], t[1].name.lower()))
    return out


def href_from_site_root(site_root: Path, page_path: Path) -> str:
    rel = page_path.resolve().relative_to(site_root.resolve())
    return rel.as_posix()


def build_map_html(site_root: Path, pages: list[tuple[str, Path]], indent: str = "          ") -> str:
    by_cat: dict[str, list[Path]] = defaultdict(list)
    for cat, p in pages:
        key = cat if cat else "(в корне pages)"
        by_cat[key].append(p)

    def I(s: str) -> str:
        return indent + s

    lines: list[str] = [I(START), I('<div class="wiki-site-map">')]

    for category in sorted(by_cat.keys(), key=lambda s: (s == "(в корне pages)", s.lower())):
        paths = sorted(by_cat[category], key=lambda x: x.name.lower())
        lines.append(I('  <section class="wiki-site-map__group">'))
        lines.append(
            I(f'    <h3 class="wiki-site-map__heading">{_html_escape(category)}</h3>')
        )
        lines.append(I('    <ul class="wiki-home-list">'))
        for p in paths:
            href = href_from_site_root(site_root, p)
            text = page_link_label(p.read_text(encoding="utf-8"), p.stem)
            lines.append(
                I(
                    f'      <li><a href="{_html_escape(href)}">{_html_escape(text)}</a></li>'
                )
            )
        lines.append(I("    </ul>"))
        lines.append(I("  </section>"))

    lines.append(I("</div>"))
    lines.append(I(END))
    return "\n".join(lines) + "\n"


def _html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def replace_site_map(index_path: Path, new_block: str) -> None:
    raw = index_path.read_text(encoding="utf-8")
    if START not in raw or END not in raw:
        print(f"Ошибка: в {index_path} не найдены {START!r} и/или {END!r}", file=sys.stderr)
        sys.exit(1)
    pre, rest = raw.split(START, 1)
    _mid, post = rest.split(END, 1)
    pre = pre.rstrip() + "\n\n"
    post = post.lstrip("\n")
    updated = pre + new_block + post
    index_path.write_text(updated, encoding="utf-8", newline="\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Обновить карту сайта в index.html по pages/**/*.html")
    ap.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Корень вики (по умолчанию — папка, где лежит этот скрипт)",
    )
    ap.add_argument(
        "--index",
        type=Path,
        default=None,
        help="Файл index.html (по умолчанию ROOT/index.html)",
    )
    args = ap.parse_args()
    root = (args.root or wiki_root_from_script()).resolve()
    index = (args.index or (root / "index.html")).resolve()
    pages = root / "pages"

    items = collect_pages(pages)
    block = build_map_html(root, items)
    replace_site_map(index, block)
    print(f"OK: {index} ({len(items)} page(s))")


if __name__ == "__main__":
    main()
