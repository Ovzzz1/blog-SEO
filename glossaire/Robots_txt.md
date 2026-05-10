# Robots.txt

> **Catégorie** : SEO Technique / Crawl / Indexation  
> **Dernière mise à jour** : 2026

---

## Définition

Le fichier **robots.txt** est un fichier texte placé à la **racine d'un site web** qui sert à communiquer avec les robots d'exploration (crawlers) via le protocole **REP (Robots Exclusion Protocol)**. Il indique aux bots quelles parties du site ils sont autorisés ou non à crawler.

> **Distinction fondamentale** : `robots.txt` contrôle le **crawl**, pas l'**indexation**. Une page bloquée dans robots.txt peut toujours apparaître dans les résultats de recherche si elle reçoit des liens externes — Google peut l'indexer sans la crawler.

**URL standard** : Toujours accessible à `https://votre-domaine.com/robots.txt`

---

## Syntaxe et composants

### Structure de base

```
User-agent: [nom du bot ou *]
Disallow: [chemin à bloquer]
Allow: [chemin à autoriser]
Sitemap: [URL du sitemap XML]
Crawl-delay: [secondes entre les requêtes]
```

### Règles de syntaxe

- Une ligne = une directive
- Les commentaires commencent par `#`
- Une ligne vide **sépare les groupes** de règles
- Les chemins sont **sensibles à la casse** (Linux)
- Le fichier doit être en **UTF-8** (ou ASCII)
- Taille maximale supportée par Google : **500 Ko** (les règles au-delà sont ignorées)

---

## Les directives principales

### `User-agent`

Spécifie le bot auquel s'appliquent les règles suivantes.

```
User-agent: *               # Tous les bots
User-agent: Googlebot       # Seulement Google
User-agent: Bingbot         # Seulement Bing
User-agent: GPTBot          # Bot OpenAI (depuis 2023)
User-agent: ClaudeBot       # Bot Anthropic
User-agent: PerplexityBot   # Bot Perplexity
User-agent: AhrefsBot       # Bot Ahrefs
User-agent: SemrushBot      # Bot Semrush
```

### `Disallow`

Bloque l'accès à un chemin ou une ressource.

```
Disallow: /          # Bloque tout le site
Disallow: /admin/    # Bloque le répertoire /admin/ et tout son contenu
Disallow: /private   # Bloque /private et /private-stuff (correspondance par préfixe)
Disallow: /*.pdf$    # Bloque tous les PDFs (syntaxe Google uniquement)
Disallow:            # Ligne vide = autorise tout (équivaut à Allow: /)
```

### `Allow`

Autorise l'accès à un chemin, même si un `Disallow` parent le bloquerait. **Priorité à la règle la plus spécifique**.

```
User-agent: Googlebot
Disallow: /css/
Allow: /css/style.css    # Autorise ce fichier spécifique malgré le Disallow du dossier

User-agent: *
Disallow: /private/
Allow: /private/public-report.pdf    # Exception pour ce document
```

### `Sitemap`

Indique l'URL du ou des sitemaps XML. Peut apparaître n'importe où dans le fichier.

```
Sitemap: https://exemple.com/sitemap.xml
Sitemap: https://exemple.com/sitemap-news.xml
Sitemap: https://exemple.com/sitemap-images.xml
```

### `Crawl-delay`

Demande au bot d'attendre un délai (en secondes) entre chaque requête. **Non supporté par Googlebot** (à gérer via Google Search Console).

```
User-agent: *
Crawl-delay: 2    # 2 secondes entre chaque requête
```

---

## Wildcards (caractères génériques)

Google supporte deux wildcards dans robots.txt :

| Caractère | Signification | Exemple |
|-----------|--------------|---------|
| `*` | N'importe quelle séquence de caractères | `Disallow: /search?*` |
| `$` | Fin d'URL | `Disallow: /*.pdf$` |

```
# Bloquer toutes les URLs contenant "?s=" (paramètres de recherche WP)
Disallow: /*?s=

# Bloquer uniquement les fichiers .xls (pas les dossiers contenant "xls")
Disallow: /*.xls$

# Bloquer les URLs avec des paramètres de session
Disallow: /*?sessionid=
```

---

## Exemples complets

### Site standard avec zones privées

```
User-agent: *
Disallow: /admin/
Disallow: /compte/
Disallow: /panier/
Disallow: /checkout/
Disallow: /search?
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

Sitemap: https://exemple.com/sitemap.xml
```

### E-commerce avec gestion des facettes

```
User-agent: *
Disallow: /compte/
Disallow: /checkout/
Disallow: /panier/
Disallow: /wishlist/
# Bloquer les paramètres de tri/filtres qui ne créent pas de contenu unique
Disallow: /*?tri=
Disallow: /*?sort=
Disallow: /*?color=
Disallow: /*?taille=
Disallow: /*?page=

# Autoriser la pagination sémantique (catégories)
Allow: /categorie/*/page/

Sitemap: https://exemple.com/sitemap.xml
Sitemap: https://exemple.com/sitemap-products.xml
```

### Bloquer les bots IA tout en autorisant les bots SEO

```
# Bloquer les scrapers IA
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: PerplexityBot
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Omgilibot
Disallow: /

# Autoriser Google et Bing normalement
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# Règle par défaut pour les autres
User-agent: *
Disallow: /admin/
Disallow: /private/

Sitemap: https://exemple.com/sitemap.xml
```

### Bloquer tout le site (site en construction)

```
User-agent: *
Disallow: /

Sitemap: https://exemple.com/sitemap.xml
```

---

## Robots.txt vs autres mécanismes de contrôle

| Mécanisme | Contrôle | Empêche indexation | Empêche crawl | Granularité |
|-----------|:--------:|:-----------------:|:-------------:|:-----------:|
| **robots.txt** | Crawl | ❌ Non | ✅ Oui | Par chemin |
| **Robots Meta Tag** | Indexation | ✅ Oui | ❌ Non | Par page |
| **X-Robots-Tag** | Indexation | ✅ Oui | ❌ Non | Par fichier |
| **Canonical** | Indexation | Indirect | ❌ Non | Par page |
| **noindex** dans CSS/JS | — | ❌ (invisible) | ❌ Non | — |

> 💡 **Règle d'or** : Pour **empêcher l'indexation** d'une page → `noindex`. Pour **réduire le crawl** d'URLs inutiles → `Disallow` dans robots.txt.

---

## Pièges et erreurs fréquentes

### 1. Bloquer les ressources CSS/JS

```
# ❌ ERREUR : empêche Google de rendre la page correctement
User-agent: Googlebot
Disallow: /wp-content/themes/
Disallow: /wp-content/plugins/
```

Google a besoin d'accéder aux CSS et JS pour comprendre le rendu de la page. Les bloquer peut entraîner une mauvaise compréhension du contenu et une baisse de positionnement.

### 2. Bloquer et mettre en canonical simultanément

Une page bloquée dans robots.txt ET ayant un canonical ne peut pas voir son canonical respecté — Google ne peut pas lire le canonical s'il ne peut pas crawler la page.

### 3. Utiliser robots.txt comme seule protection des données sensibles

`robots.txt` est un fichier public. N'importe qui peut le lire et accéder aux URLs listées dedans. Pour sécuriser de vraies données sensibles : authentification + 401/403.

### 4. Slash final absent

```
Disallow: /admin     # Bloque aussi /administrator, /admintools...
Disallow: /admin/    # Bloque uniquement le dossier /admin/ ← plus précis
```

---

## Robots.txt et les bots IA (2024-2026)

L'essor des LLMs (ChatGPT, Claude, Perplexity, Gemini) a introduit une nouvelle catégorie de bots qui crawlent le web pour entraîner leurs modèles ou répondre à des requêtes. En 2026, de nombreux sites choisissent de contrôler cet accès.

### Principaux bots IA à connaître

| Bot | Organisation | User-Agent |
|-----|-------------|-----------|
| GPTBot | OpenAI | `GPTBot/1.0` |
| ChatGPT-User | OpenAI | `ChatGPT-User` |
| ClaudeBot | Anthropic | `ClaudeBot` |
| Claude-User | Anthropic | `Claude-User` |
| PerplexityBot | Perplexity AI | `PerplexityBot` |
| Gemini | Google | (via Googlebot) |
| Amazonbot | Amazon (Alexa) | `Amazonbot` |
| Bytespider | ByteDance | `Bytespider` |
| CCBot | Common Crawl | `CCBot` |

> Note : Certains de ces bots (notamment ceux d'OpenAI) respectent robots.txt depuis mi-2023 suite à des pressions légales. Le respect n'est cependant pas garanti pour tous les acteurs.

---

## Monitoring et validation

### Google Search Console
- **Rapport d'exploration** → Statistiques de crawl : observer le comportement de Googlebot
- **Outil de test robots.txt** : Tester si une URL spécifique est bloquée (dans l'ancien Search Console)

### Validation en ligne
- [robots.txt Tester de Google](https://search.google.com/search-console/robots-testing-tool)
- [Merkle robots.txt validator](https://technicalseo.com/tools/robots-txt/)

### Test manuel
```bash
# Afficher le robots.txt
curl https://exemple.com/robots.txt

# Vérifier qu'une URL est accessible (simuler Googlebot)
curl -A "Googlebot/2.1" -I https://exemple.com/page-test
```

---

## Voir aussi

- [Robots Meta Tag](./Robots_Meta_Tag.md)
- [X-Robots-Tag](./X_Robots_Tag.md)
- [Crawl Budget](./Crawl_Budget.md)
- [XML Sitemap](./XML_Sitemap.md)
- [Rel Follow/Nofollow](./Rel_Follow_Nofollow.md)
