"""
Génère veille/index.html à partir de data/items.json :
- section "Résumés du jour" (articles interesting=true du dernier fetch)
- flux brut façon Feedly (titre + image mise en avant) pour tout le reste
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS_PATH = os.path.join(ROOT, "data", "items.json")
OUTPUT = os.path.join(ROOT, "index.html")


def load_items():
    with open(ITEMS_PATH, encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return (s or "").replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def main():
    items = load_items()
    items.sort(key=lambda x: x.get("date", ""), reverse=True)

    sources = sorted(set(it["source"] for it in items))

    items_js = ",\n    ".join([
        '{{ id: "{id}", source: "{source}", title: "{title}", link: "{link}", '
        'image: {image}, date: "{date}", summary: "{summary}", interesting: {interesting} }}'.format(
            id=esc(it["id"]), source=esc(it["source"]), title=esc(it["title"]),
            link=esc(it["link"]),
            image=('"' + esc(it["image"]) + '"') if it.get("image") else "null",
            date=it.get("date", ""), summary=esc(it.get("summary") or ""),
            interesting="true" if it.get("interesting") else "false",
        )
        for it in items
    ])

    filter_buttons = '\n    <button class="filter-btn active" onclick="filter(\'tous\')">Tous</button>\n'
    for s in sources:
        filter_buttons += f'    <button class="filter-btn" onclick="filter(\'{esc(s)}\')">{s}</button>\n'

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Veille SEO</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    :root {{
      --ink: #f9fafb;
      --ink-2: #d1d5db;
      --ink-3: #9ca3af;
      --paper: #17191a;
      --paper-2: #212426;
      --paper-3: #2d3134;
      --accent: #ff6e40;
      --mono: 'DM Mono', monospace;
      --sans: 'DM Sans', sans-serif;
      --display: 'Syne', sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: var(--sans); background: var(--paper); color: var(--ink); font-size: 15px; line-height: 1.6; font-weight: 300; }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 0 2rem; }}

    header {{ border-bottom: 1px solid var(--paper-3); padding: 2.5rem 0 2rem; }}
    header h1 {{ font-family: var(--display); font-size: clamp(2rem, 5vw, 3rem); font-weight: 800; letter-spacing: -0.03em; line-height: 1; }}
    header h1 em {{ font-style: normal; color: var(--accent); }}
    header p {{ font-size: 0.9rem; color: var(--ink-3); margin-top: 0.4rem; font-family: var(--mono); letter-spacing: 0.03em; }}

    h2.section-title {{
      font-family: var(--display); font-size: 1.3rem; font-weight: 700;
      margin: 2.5rem 0 1rem; letter-spacing: -0.01em;
    }}

    .digest-list {{ display: flex; flex-direction: column; gap: 0.9rem; margin-bottom: 1rem; }}
    .digest-card {{
      border: 1px solid var(--paper-3); border-radius: 6px; padding: 1rem 1.2rem;
      background: var(--paper-2); text-decoration: none; color: inherit; display: block;
      transition: border-color 0.15s;
    }}
    .digest-card:hover {{ border-color: var(--accent); }}
    .digest-source {{
      font-family: var(--mono); font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
      color: var(--accent); margin-bottom: 0.3rem;
    }}
    .digest-title {{ font-weight: 500; font-size: 1rem; margin-bottom: 0.35rem; }}
    .digest-summary {{ color: var(--ink-2); font-size: 0.9rem; }}

    .filters {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0; }}
    .filter-btn {{
      font-family: var(--mono); font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase;
      padding: 0.35rem 0.9rem; border-radius: 2px; border: 1px solid var(--paper-3);
      background: transparent; cursor: pointer; color: var(--ink-3); transition: all 0.15s;
    }}
    .filter-btn:hover {{ border-color: var(--ink-3); color: var(--ink); }}
    .filter-btn.active {{ background: var(--ink); color: var(--paper); border-color: var(--ink); }}

    .meta-line {{ font-family: var(--mono); font-size: 11px; color: var(--ink-3); letter-spacing: 0.04em; margin-bottom: 1rem; }}

    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1.1rem; }}
    .card {{
      border: 1px solid var(--paper-3); border-radius: 6px; overflow: hidden; text-decoration: none;
      color: inherit; background: var(--paper-2); display: flex; flex-direction: column; transition: border-color 0.15s;
    }}
    .card:hover {{ border-color: var(--ink-3); }}
    .card-img {{ width: 100%; aspect-ratio: 16/9; object-fit: cover; background: var(--paper-3); display: block; }}
    .card-body {{ padding: 0.8rem 0.9rem; display: flex; flex-direction: column; gap: 0.4rem; flex: 1; }}
    .card-source {{ font-family: var(--mono); font-size: 10px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-3); }}
    .card-title {{ font-size: 0.9rem; font-weight: 400; line-height: 1.35; flex: 1; }}
    .card:hover .card-title {{ color: var(--accent); }}
    .card-date {{ font-family: var(--mono); font-size: 10px; color: var(--ink-3); }}

    .empty {{ padding: 3rem 0; font-family: var(--mono); font-size: 12px; color: var(--ink-3); letter-spacing: 0.05em; }}

    footer {{
      margin: 4rem 0 2rem; padding-top: 1.5rem; border-top: 1px solid var(--paper-3);
      display: flex; justify-content: space-between; font-family: var(--mono); font-size: 10px;
      color: var(--ink-3); letter-spacing: 0.05em;
    }}
  </style>
</head>
<body>

<header>
  <div class="wrap">
    <h1>Veille <em>SEO</em></h1>
    <p>Search Engine Journal · PressWhizz · Ahrefs Blog · Abondance — flux quotidien</p>
  </div>
</header>

<div class="wrap">
  <h2 class="section-title">À checker aujourd'hui</h2>
  <div class="digest-list" id="digest"></div>

  <h2 class="section-title">Flux brut</h2>
  <div class="filters" id="filters">
    {filter_buttons}
  </div>
  <p class="meta-line" id="count"></p>
  <div class="grid" id="grid"></div>

  <footer>
    <span>Veille SEO — usage interne</span>
    <span>Généré automatiquement</span>
  </footer>
</div>

<script>
  const items = [
    {items_js}
  ];

  let current = "tous";

  function fmt(s) {{
    const d = new Date(s);
    return d.toLocaleDateString("fr-FR", {{ day: "2-digit", month: "short", year: "numeric" }});
  }}

  function renderDigest() {{
    const interesting = items.filter(a => a.interesting);
    const el = document.getElementById("digest");
    if (interesting.length === 0) {{
      el.innerHTML = '<p class="empty">Rien de marquant pour l\\'instant.</p>';
      return;
    }}
    el.innerHTML = interesting.slice(0, 20).map(a => `
      <a class="digest-card" href="${{a.link}}" target="_blank" rel="noopener">
        <div class="digest-source">${{a.source}} — ${{fmt(a.date)}}</div>
        <div class="digest-title">${{a.title}}</div>
        <div class="digest-summary">${{a.summary}}</div>
      </a>
    `).join("");
  }}

  function filter(source) {{
    current = source;
    document.querySelectorAll(".filter-btn").forEach(b => {{
      b.classList.toggle("active",
        (source === "tous" && b.textContent === "Tous") || b.textContent === source
      );
    }});
    renderGrid();
  }}

  function renderGrid() {{
    const filtered = current === "tous" ? items : items.filter(a => a.source === current);
    document.getElementById("count").textContent = filtered.length + " article" + (filtered.length > 1 ? "s" : "");
    if (filtered.length === 0) {{
      document.getElementById("grid").innerHTML = '<p class="empty">Aucun article.</p>';
      return;
    }}
    document.getElementById("grid").innerHTML = filtered.map(a => `
      <a class="card" href="${{a.link}}" target="_blank" rel="noopener">
        ${{a.image ? `<img class="card-img" src="${{a.image}}" loading="lazy" onerror="this.style.display='none'">` : ''}}
        <div class="card-body">
          <div class="card-source">${{a.source}}</div>
          <div class="card-title">${{a.title}}</div>
          <div class="card-date">${{fmt(a.date)}}</div>
        </div>
      </a>
    `).join("");
  }}

  renderDigest();
  renderGrid();
</script>

</body>
</html>"""

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    interesting_count = sum(1 for it in items if it.get("interesting"))
    print(f"Build terminé — {len(items)} article(s), {interesting_count} en résumé du jour.")


if __name__ == "__main__":
    main()
