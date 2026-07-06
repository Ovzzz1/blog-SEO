"""
Backfill ponctuel : remonte tous les articles publiés dans les N derniers jours
(par défaut 15) sur les 4 sites, via leur API REST WordPress (wp-json). Plus
fiable qu'un flux RSS (limité aux ~10-25 derniers articles) et plus fiable
qu'un sitemap (dont le lastmod reflète une modification, pas la publication).
À lancer une fois pour rattraper l'historique ; le fetch RSS quotidien prend
ensuite le relais pour les nouveautés.
"""
import html
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS_PATH = os.path.join(ROOT, "data", "items.json")
HEADERS = {"User-Agent": "Mozilla/5.0 (veille-seo bot)"}

SOURCES = [
    {"source": "Search Engine Journal", "api": "https://www.searchenginejournal.com/wp-json/wp/v2/posts"},
    {"source": "PressWhizz", "api": "https://presswhizz.com/wp-json/wp/v2/posts"},
    {"source": "Ahrefs Blog", "api": "https://ahrefs.com/blog/wp-json/wp/v2/posts"},
    {"source": "Abondance", "api": "https://www.abondance.com/wp-json/wp/v2/posts"},
]


def strip_html(s):
    text = re.sub(r"<[^>]+>", " ", s or "")
    text = re.sub(r"\s+", " ", text).strip()
    return html.unescape(text)


def load_items():
    if os.path.exists(ITEMS_PATH):
        with open(ITEMS_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_items(items):
    items.sort(key=lambda x: x.get("date", ""), reverse=True)
    with open(ITEMS_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def fetch_posts_since(api_url, cutoff):
    """Pagine sur l'API REST WP (posts triés du plus récent au plus ancien)
    et retourne tous les posts dont la date de publication est >= cutoff."""
    posts = []
    page = 1
    while True:
        resp = requests.get(
            api_url,
            params={"per_page": 50, "page": page, "orderby": "date", "order": "desc"},
            headers=HEADERS, timeout=20,
        )
        if resp.status_code == 400:
            break  # page au-delà du total (WP renvoie 400 rest_post_invalid_page_number)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break

        stop = False
        for p in batch:
            pub_date = datetime.fromisoformat(p["date"]).replace(tzinfo=timezone.utc)
            if pub_date < cutoff:
                stop = True
                continue
            posts.append(p)

        if stop:
            break
        page += 1

    return posts


def extract_image(post):
    yhj = post.get("yoast_head_json") or {}
    og_images = yhj.get("og_image") or []
    if og_images:
        return og_images[0].get("url")
    return None


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    items = load_items()
    known_ids = {it["id"] for it in items}
    added = 0

    for src in SOURCES:
        try:
            posts = fetch_posts_since(src["api"], cutoff)
        except Exception as e:
            print(f"[WARN] échec API {src['source']}: {e}")
            continue

        print(f"=== {src['source']} — {len(posts)} article(s) sur les {days} derniers jours ===")

        for p in posts:
            link = p.get("link", "").strip()
            if not link or link in known_ids:
                continue

            title = strip_html(p.get("title", {}).get("rendered", ""))
            description = strip_html(p.get("excerpt", {}).get("rendered", ""))[:500]
            pub_date = datetime.fromisoformat(p["date"]).replace(tzinfo=timezone.utc).isoformat()

            items.append({
                "id": link,
                "source": src["source"],
                "title": title,
                "link": link,
                "date": pub_date,
                "description": description,
                "content_text": description,
                "image": extract_image(p),
                "summary": None,
                "interesting": False,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            })
            known_ids.add(link)
            added += 1
            print(f"[BACKFILL] {src['source']}: {title}")

    save_items(items)
    print(f"Backfill terminé — {added} article(s) ajouté(s), {len(items)} au total.")


if __name__ == "__main__":
    main()
