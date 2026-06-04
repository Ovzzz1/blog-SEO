import os
import re
import markdown
from datetime import datetime

GLOSSAIRE_DIR = "glossaire"
OUTPUT_INDEX = "glossaire/index.html"

# Common styles from seo-dom.html
CSS = """
  :root {
    --ink: #f9fafb;
    --ink-2: #d1d5db;
    --ink-3: #9ca3af;
    --paper: #17191a;
    --paper-2: #212426;
    --paper-3: #2d3134;
    --accent: #ff6e40;
    --accent-2: #60a5fa;
    --success: #34d399;
    --warn: #fbbf24;
    --danger: #f87171;
    --mono: 'DM Mono', monospace;
    --sans: 'DM Sans', sans-serif;
    --display: 'Syne', sans-serif;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { font-size: 16px; scroll-behavior: smooth; }
  body {
    background: var(--paper);
    color: var(--ink);
    font-family: var(--sans);
    font-size: 15px;
    line-height: 1.75;
    font-weight: 300;
  }

  .page-wrap { max-width: 860px; margin: 0 auto; padding: 0 2rem; }

  .site-header {
    border-bottom: 1px solid var(--paper-3);
    padding: 2rem 0 1.5rem;
    margin-bottom: 0;
  }
  .header-meta {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  .tag-badge {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 10px;
    border: 1px solid var(--paper-3);
    border-radius: 2px;
    color: var(--ink-3);
  }
  .tag-badge.accent { border-color: var(--accent); color: var(--accent); }

  .hero-title {
    font-family: var(--display);
    font-size: clamp(2.5rem, 5vw, 3.5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: var(--ink);
    margin-bottom: 1rem;
  }
  .hero-title em { font-style: normal; color: var(--accent); }

  .section { padding: 2rem 0; }
  
  h2 {
    font-family: var(--display);
    font-size: 1.6rem;
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.02em;
    color: var(--ink);
    margin: 2rem 0 1rem;
  }

  h3 {
    font-family: var(--display);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--ink);
    margin: 1.5rem 0 0.75rem;
  }

  p { margin-bottom: 1rem; color: var(--ink-2); }
  strong { font-weight: 500; color: var(--ink); }
  em { color: var(--ink-2); }
  
  ul, ol { margin: 0 0 1rem 1.5rem; color: var(--ink-2); }
  li { margin-bottom: 0.5rem; }

  code {
    font-family: var(--mono);
    font-size: 0.85em;
    background: var(--paper-2);
    border: 1px solid var(--paper-3);
    border-radius: 3px;
    padding: 2px 5px;
    color: var(--accent-2);
  }

  pre {
    background: #0f1113;
    border: 1px solid var(--paper-3);
    border-radius: 4px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    overflow-x: auto;
  }
  pre code {
    background: none;
    border: none;
    padding: 0;
    font-size: 0.82rem;
    color: #a8d8b8;
  }

  blockquote {
    border-left: 3px solid var(--paper-3);
    padding: 0.5rem 1rem;
    margin: 1.5rem 0;
    color: var(--ink-3);
    background: var(--paper-2);
    border-radius: 0 4px 4px 0;
  }
  blockquote p { margin-bottom: 0; }
  blockquote p + p { margin-top: 0.5rem; }

  .table-wrap { overflow-x: auto; margin: 1.5rem 0; }
  table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
  thead tr { background: var(--paper-2); color: var(--ink); }
  thead th {
    font-family: var(--mono); font-size: 10px; font-weight: 500;
    letter-spacing: 0.1em; text-transform: uppercase; padding: 0.75rem 1rem; text-align: left;
  }
  tbody tr { border-bottom: 1px solid var(--paper-2); }
  tbody tr:hover { background: var(--paper-2); }
  tbody td { padding: 0.65rem 1rem; color: var(--ink-2); vertical-align: top; }
  tbody td:first-child { font-weight: 400; color: var(--ink); }

  .site-footer {
    margin-top: 4rem; padding: 2rem 0;
    border-top: 1px solid var(--paper-3);
    display: flex; justify-content: space-between;
    font-family: var(--mono); font-size: 11px;
    color: var(--ink-3); letter-spacing: 0.05em;
  }
  
  a { color: var(--accent-2); text-decoration: none; }
  a:hover { text-decoration: underline; }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="tag" content="glossaire">
<meta name="date" content="{date}">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Glossaire SEO</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>

<div class="page-wrap">
  <div style="padding-top: 2rem;">
    <a href="index.html" style="font-family: var(--mono); font-size: 11px; text-decoration: none; color: var(--ink-3); text-transform: uppercase; letter-spacing: 0.1em; transition: color 0.15s;">← Retour au glossaire</a>
    <span style="color: var(--paper-3); margin: 0 0.5rem;">|</span>
    <a href="../index.html" style="font-family: var(--mono); font-size: 11px; text-decoration: none; color: var(--ink-3); text-transform: uppercase; letter-spacing: 0.1em; transition: color 0.15s;">Retour à l'accueil</a>
  </div>

  <header class="site-header">
    <div class="header-meta">
      <span class="tag-badge accent">Glossaire SEO</span>
      <span class="tag-badge">{category}</span>
    </div>
    <div class="hero-grid">
      <div>
        <h1 class="hero-title">{title}</h1>
      </div>
    </div>
  </header>

  <section class="section">
    {content}
  </section>

  <footer class="site-footer">
    <span>Base de connaissance SEO</span>
    <span>Glossaire technique</span>
  </footer>
</div>

</body>
</html>
"""

def build():
    md = markdown.Markdown(extensions=['tables', 'fenced_code'])
    
    terms = []
    
    for f in os.listdir(GLOSSAIRE_DIR):
        if not f.endswith(".md"):
            continue
            
        path = os.path.join(GLOSSAIRE_DIR, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Parse title
        title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else f.replace('.md', '')
        
        # Remove the title from content so it's not rendered twice
        content = re.sub(r'^#\s+.*', '', content, 1, re.MULTILINE)
        
        # Parse metadata
        category = "Technique"
        cat_match = re.search(r'\*\*Catégorie\*\*\s*:\s*(.*)', content)
        if cat_match:
            category = cat_match.group(1).strip()
            
        date = "2026"
        date_match = re.search(r'\*\*Dernière mise à jour\*\*\s*:\s*(.*)', content)
        if date_match:
            date = date_match.group(1).strip()
            
        # Remove metadata blockquote completely for cleaner look
        content = re.sub(r'>\s*\*\*Catégorie\*\*.*?\n>\s*\*\*Dernière.*?\n', '', content, flags=re.MULTILINE|re.IGNORECASE)
        content = re.sub(r'>\s*\*\*Catégorie\*\*.*?\n', '', content, flags=re.MULTILINE|re.IGNORECASE)
        
        # Fix internal links from .md to .html
        content = re.sub(r'\]\(([^)]+)\.md\)', r'](\1.html)', content)
        
        html_content = md.convert(content)
        
        # Wrap tables with table-wrap for responsiveness
        html_content = html_content.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
        
        final_html = HTML_TEMPLATE.format(
            title=title,
            category=category,
            date=date,
            content=html_content,
            css=CSS
        )
        
        html_filename = f.replace('.md', '.html')
        html_path = os.path.join(GLOSSAIRE_DIR, html_filename)
        
        with open(html_path, 'w', encoding='utf-8') as out:
            out.write(final_html)
            
        terms.append({
            "title": title,
            "file": html_filename,
            "category": category
        })
        
        print(f"Generated {html_filename}")

    # Generate glossaire/index.html
    terms.sort(key=lambda x: x["title"].lower())
    
    # CSS for index
    INDEX_CSS = CSS + """
    .term-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }
    .term-card {
        background: var(--paper-2);
        border: 1px solid var(--paper-3);
        padding: 1.5rem;
        border-radius: 4px;
        text-decoration: none;
        transition: border-color 0.2s, transform 0.2s;
    }
    .term-card:hover {
        border-color: var(--accent);
        transform: translateY(-2px);
    }
    .term-title {
        font-family: var(--display);
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--ink);
        margin-bottom: 0.5rem;
    }
    .term-cat {
        font-family: var(--mono);
        font-size: 10px;
        color: var(--ink-3);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    """
    
    cards_html = ""
    for t in terms:
        cards_html += f'''
        <a href="{t["file"]}" class="term-card">
            <div class="term-title">{t["title"]}</div>
            <div class="term-cat">{t["category"]}</div>
        </a>'''

    index_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glossaire SEO</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet">
<style>
{INDEX_CSS}
</style>
</head>
<body>

<div class="page-wrap">
  <div style="padding-top: 2rem;">
    <a href="../index.html" style="font-family: var(--mono); font-size: 11px; text-decoration: none; color: var(--ink-3); text-transform: uppercase; letter-spacing: 0.1em; transition: color 0.15s;">← Retour à l'accueil</a>
  </div>

  <header class="site-header">
    <div class="hero-grid">
      <div>
        <h1 class="hero-title">Glossaire <em>SEO</em></h1>
        <p style="color: var(--ink-3); font-family: var(--mono); font-size: 0.9rem; letter-spacing: 0.03em;">{len(terms)} concepts techniques</p>
      </div>
    </div>
  </header>

  <section class="section">
    <div class="term-list">
        {cards_html}
    </div>
  </section>

  <footer class="site-footer">
    <span>Base de connaissance SEO</span>
    <span>Glossaire technique</span>
  </footer>
</div>

</body>
</html>
"""

    with open(OUTPUT_INDEX, 'w', encoding='utf-8') as out:
        out.write(index_html)
    print(f"Generated {OUTPUT_INDEX}")

if __name__ == "__main__":
    build()
