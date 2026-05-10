# Canonical URL (Balise Canonique)

> **Catégorie** : SEO Technique / Duplication de contenu / Indexation  
> **Dernière mise à jour** : 2026

---

## Définition

Une **URL canonique** est l'URL de référence désignée comme la version "officielle" d'une page lorsque plusieurs URLs pointent vers un contenu identique ou très similaire. La balise canonique (`<link rel="canonical">`) est le signal envoyé aux moteurs de recherche pour indiquer quelle version doit être indexée et à laquelle attribuer le link equity.

Introduite en **2009** par Google, Bing et Yahoo! conjointement, la canonicalisation est l'un des piliers de la gestion du contenu dupliqué en SEO.

---

## Pourquoi le contenu dupliqué existe

Le contenu dupliqué survient naturellement dans de nombreux contextes :

| Cause | Exemple |
|-------|---------|
| Paramètres d'URL | `/produit?color=rouge` vs `/produit?color=bleu` |
| HTTP vs HTTPS | `http://exemple.com` vs `https://exemple.com` |
| WWW vs non-WWW | `www.exemple.com` vs `exemple.com` |
| Slash final | `/page/` vs `/page` |
| Pagination | `/blog/` vs `/blog/page/2` |
| Tri / filtres e-commerce | `/chaussures?tri=prix-asc` |
| Syndication de contenu | Article republié sur plusieurs domaines |
| Versions mobiles | `m.exemple.com` vs `www.exemple.com` |
| Versions d'impression | `/article?print=1` |
| Sessions tracking | `/page?sessionid=abc123` |

Sans signal canonique, les moteurs peuvent diviser le link equity entre plusieurs versions, diluer l'autorité de la page, et indexer la mauvaise version.

---

## Syntaxe et implémentation

### Dans le `<head>` HTML (méthode principale)

```html
<link rel="canonical" href="https://www.exemple.com/page-canonique">
```

**Règles** :
- Toujours utiliser l'URL **absolue** (pas relative)
- Inclure le protocole (https://) et le domaine
- Une seule balise canonique par page
- Placer dans le `<head>`, pas dans le `<body>`

### Auto-référencement (self-canonical)

Même sur la page canonique elle-même, il est recommandé d'ajouter une balise canonique pointant vers elle-même. Cela protège contre les paramètres d'URL ajoutés par des outils tiers.

```html
<!-- Sur https://www.exemple.com/article -->
<link rel="canonical" href="https://www.exemple.com/article">
```

### Via header HTTP (pour les PDFs et ressources non-HTML)

```http
HTTP/1.1 200 OK
Link: <https://www.exemple.com/document.pdf>; rel="canonical"
```

### Via le Sitemap XML

Les URLs incluses dans le sitemap sont implicitement considérées comme canoniques par Google, même si ce signal est moins fort que la balise `<link>`.

---

## Canonical cross-domain

La balise canonique peut pointer vers un **autre domaine**. C'est utilisé dans les cas de syndication de contenu : si votre article est republié sur un autre site, ce site peut pointer sa version vers votre URL originale.

```html
<!-- Sur site-partenaire.com/article-syndiqué -->
<link rel="canonical" href="https://votre-site.com/article-original">
```

> ⚠️ Google accepte le canonical cross-domain mais peut choisir de l'ignorer si le signal semble manipulateur.

---

## Canonical vs Autres signaux de déduplication

| Signal | Force | Usage recommandé |
|--------|-------|------------------|
| `<link rel="canonical">` | Fort | Contenu dupliqué sur le même site |
| Redirect 301 | Très fort | URLs obsolètes à supprimer définitivement |
| `noindex` | Très fort | Pages à exclure totalement de l'index |
| Paramètres GSC | Faible | Paramètres d'URL courants |
| Sitemap | Faible | Signal d'intention, pas une directive |

**Règle générale** : Si vous voulez qu'une URL disparaisse pour toujours → 301. Si vous voulez qu'une URL existe mais ne soit pas l'URL indexée → canonical.

---

## Erreurs canoniques fréquentes

### 1. Canonical vers une page 404 ou redirigée
```html
<!-- ❌ ERREUR : pointe vers une page inexistante -->
<link rel="canonical" href="https://exemple.com/page-supprimee">
```
→ Google ignore le signal et choisit lui-même l'URL canonique.

### 2. Canonical vers une page noindex
Un canonical vers une page noindex crée une contradiction : "Indexe cette version, mais n'indexe pas cette version." Google peut ignorer les deux.

### 3. Conflits canonical / hreflang
Les pages hreflang doivent avoir leur propre canonical. Une page FR-FR ne doit pas pointer en canonical vers la page EN-US.

### 4. Canonicals en chaîne
```
Page A → canonical → Page B → canonical → Page C
```
Pointer directement vers la destination finale.

### 5. Ignorer le canonical sur les pages paginées
Chaque page de pagination doit avoir son propre canonical (self-canonical), pas un canonical vers la page 1.

```html
<!-- ✅ Page 3 de pagination -->
<link rel="canonical" href="https://exemple.com/blog/page/3">
```

---

## Canonical et JavaScript

Si la balise canonical est injectée via JavaScript, Google peut la voir lors du rendu JS (deuxième vague de crawl), mais avec un délai. Pour les signaux SEO critiques, **inclure la balise canonical dans le HTML initial** (SSR ou statique).

---

## Vérification et audit

### Google Search Console
- **Rapport Couverture** → "URLs exclues - Dupliquée sans canonical sélectionné par l'utilisateur"
- **Inspection d'URL** → Affiche l'URL canonique sélectionnée par Google (peut différer de votre signal !)

> 💡 Si Google choisit une URL canonique différente de celle que vous spécifiez, c'est un signal fort que votre implémentation est incorrecte ou que vos signaux sont contradictoires.

### Screaming Frog
- Filtre "Canonical" → voir toutes les pages avec canonical
- Filtre "Non-Indexable Canonical" → détecter les canonicals problématiques

### Commande rapide (si accès logs)
```bash
curl -I https://exemple.com/page | grep -i link
```

---

## Voir aussi

- [3XX HTTP Response Codes](./3XX_HTTP_Response_Codes.md)
- [Hreflang](./Hreflang.md)
- [Robots Meta Tag](./Robots_Meta_Tag.md)
- [XML Sitemap](./XML_Sitemap.md)
- [AMP et rel=amphtml](./AMP_et_rel_amphtml.md)
