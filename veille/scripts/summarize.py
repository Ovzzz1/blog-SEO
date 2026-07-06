"""
Passe en revue les nouveaux articles (summary == None) et demande à Claude,
pour chaque lot par source, de sélectionner ceux qui sont intéressants et
d'en faire un résumé court (2 phrases max, en français).
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS_PATH = os.path.join(ROOT, "data", "items.json")
NOTES_PATH = os.path.join(ROOT, "data", "notes.md")

CLAUDE_BIN = os.path.expanduser("~/.local/bin/claude")
TIMEOUT_S = 180

SYSTEM_PROMPT = """Tu es un veilleur SEO expérimenté qui filtre un flux RSS pour un opérateur \
de sites de netlinking (vente de liens, gestion d'une flotte de sites SEO). Pour chaque \
article fourni, décide s'il est réellement intéressant pour ce métier (mises à jour \
d'algorithme Google, techniques de link building, GSC/indexation, outils SEO, data/études \
utiles) — et écarte le bruit (actu générique, listicles creux, pub produit). Si des notes \
d'apprentissage sur les préférences de l'utilisateur sont fournies, applique-les pour juger \
ce qui est intéressant ou non.
Réponds UNIQUEMENT en JSON, un objet {"results": [{"id": "...", "interesting": bool, \
"summary": "..."}]}. Le résumé ne doit être rempli que si interesting=true, en français, \
2 phrases maximum, factuel, sans emoji."""


def call_claude(system_prompt, user_prompt):
    cmd = [CLAUDE_BIN, "-p", user_prompt,
           "--append-system-prompt", system_prompt,
           "--output-format", "json"]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_S)
    if proc.returncode != 0:
        raise RuntimeError(f"claude -p code {proc.returncode}: {proc.stderr[-1500:]}")
    envelope = json.loads(proc.stdout)
    return envelope.get("result", proc.stdout)


def parse_json_block(text):
    text = text.strip()
    if text.startswith("```"):
        import re
        text = re.sub(r"^```[a-zA-Z]*\n", "", text)
        text = re.sub(r"\n```$", "", text).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Aucun objet JSON trouvé dans la réponse Claude.")
    return json.loads(text[start:end + 1])


def load_items():
    with open(ITEMS_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_items(items):
    with open(ITEMS_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def load_notes():
    if os.path.exists(NOTES_PATH):
        with open(NOTES_PATH, encoding="utf-8") as f:
            return f.read().strip()
    return ""


def main():
    items = load_items()
    pending = [it for it in items if it.get("summary") is None]
    if not pending:
        print("Rien de nouveau à résumer.")
        return

    notes = load_notes()
    by_id = {it["id"]: it for it in items}

    batch_payload = [
        {"id": it["id"], "source": it["source"], "title": it["title"],
         "text": it["content_text"][:2000]}
        for it in pending
    ]

    user_prompt = "Notes d'apprentissage sur les préférences:\n" + (notes or "(aucune pour l'instant)")
    user_prompt += "\n\nArticles à juger (JSON):\n" + json.dumps(batch_payload, ensure_ascii=False)

    raw = call_claude(SYSTEM_PROMPT, user_prompt)
    parsed = parse_json_block(raw)

    for res in parsed.get("results", []):
        item = by_id.get(res.get("id"))
        if not item:
            continue
        item["interesting"] = bool(res.get("interesting"))
        item["summary"] = res.get("summary") or "" if item["interesting"] else ""

    save_items(items)
    interesting_count = sum(1 for r in parsed.get("results", []) if r.get("interesting"))
    print(f"Résumé terminé — {interesting_count}/{len(pending)} article(s) jugé(s) intéressant(s).")


if __name__ == "__main__":
    main()
