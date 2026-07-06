"""
Fetch les flux RSS de veille SEO, dédup, récupère l'image mise en avant (og:image)
pour les nouveaux articles, et met à jour data/items.json.
"""
import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS_PATH = os.path.join(ROOT, "data", "items.json")

FEEDS = [
    {"source": "Search Engine Journal", "url": "https://www.searchenginejournal.com/feed/"},
    {"source": "PressWhizz", "url": "https://presswhizz.com/blog/feed/"},
    {"source": "Ahrefs Blog", "url": "https://ahrefs.com/blog/feed/"},
    {"source": "Abondance", "url": "https://www.abondance.com/feed"},
]

HEADERS = {"User-Agent": "Mozilla/5.0 (veille-seo bot)"}


def load_items():
    if os.path.exists(ITEMS_PATH):
        with open(ITEMS_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_items(items):
    items.sort(key=lambda x: x.get("date", ""), reverse=True)
    with open(ITEMS_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def strip_html(html):
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_feed(source, url):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    entries = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date_raw = item.findtext("pubDate")
        try:
            pub_date = parsedate_to_datetime(pub_date_raw).astimezone(timezone.utc).isoformat()
        except Exception:
            pub_date = datetime.now(timezone.utc).isoformat()
        description = strip_html(item.findtext("description") or "")
        content_encoded = item.findtext("content:encoded", namespaces=ns) or ""
        content_text = strip_html(content_encoded) or description
        entries.append({
            "id": link,
            "source": source,
            "title": title,
            "link": link,
            "date": pub_date,
            "description": description[:500],
            "content_text": content_text[:6000],
        })
    return entries


def fetch_og_image(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        match = re.search(
            r'<meta[^>]+(?:property|name)=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
            resp.text, re.IGNORECASE
        )
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def main():
    items = load_items()
    known_ids = {it["id"] for it in items}
    new_count = 0

    for feed in FEEDS:
        try:
            entries = parse_feed(feed["source"], feed["url"])
        except Exception as e:
            print(f"[WARN] échec fetch {feed['source']}: {e}")
            continue

        for entry in entries:
            if entry["id"] in known_ids:
                continue
            entry["image"] = fetch_og_image(entry["link"])
            entry["summary"] = None
            entry["interesting"] = False
            entry["fetched_at"] = datetime.now(timezone.utc).isoformat()
            items.append(entry)
            known_ids.add(entry["id"])
            new_count += 1
            print(f"[NEW] {feed['source']}: {entry['title']}")

    save_items(items)
    print(f"Terminé — {new_count} nouvel(le)s article(s), {len(items)} au total.")


if __name__ == "__main__":
    main()
