# AMP (Accelerated Mobile Pages) & `rel="amphtml"`

> **Catégorie** : Performance Web / Mobile / SEO Technique  
> **Dernière mise à jour** : 2026  
> **Statut** : Technologie en déclin progressif — voir section [AMP en 2026](#amp-en-2026)

---

## Définition

**AMP** (Accelerated Mobile Pages) est un framework open-source initié par Google en 2015, conçu pour créer des pages web ultra-rapides sur mobile. Les pages AMP utilisent un sous-ensemble restreint de HTML, une version optimisée de CSS, et un runtime JavaScript spécifique (`amp.js`) pour garantir des temps de chargement quasi-instantanés.

À son apogée (2016-2021), AMP offrait un avantage de positionnement dans les résultats mobiles de Google via le **Top Stories carousel**, réservé aux pages AMP. Cet avantage a été supprimé en **juin 2021**.

---

## Architecture technique d'une page AMP

### Composants fondamentaux

**1. AMP HTML** : HTML standard avec restrictions et extensions
- Interdiction de `<script>` personnalisés
- Tous les éléments visuels via composants AMP (`<amp-img>`, `<amp-video>`, etc.)
- CSS inline uniquement, limité à 75 KB

**2. AMP JS** : Bibliothèque de runtime gérant :
- Le chargement asynchrone des ressources
- La priorisation des éléments visibles
- L'isolation des iframes tiers

**3. AMP Cache** : CDN de Google (et Cloudflare/Bing) qui sert les pages AMP
- Pré-rendu des pages pour un chargement instantané
- URL formatée : `https://www.exemple-com.cdn.ampproject.org/c/s/www.exemple.com/article`

### Structure minimale

```html
<!doctype html>
<html ⚡ lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,minimum-scale=1">
  <link rel="canonical" href="https://www.exemple.com/article">
  <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;}</style>
  <noscript><style amp-boilerplate>body{-webkit-animation:none}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>Mon Article</title>
</head>
<body>
  <amp-img src="hero.jpg" width="800" height="400" layout="responsive" alt="Hero"></amp-img>
  <p>Contenu de l'article...</p>
</body>
</html>
```

---

## Le tag `rel="amphtml"`

### Rôle
Le tag `rel="amphtml"` est placé dans la page HTML canonique pour indiquer aux moteurs de recherche qu'il existe une version AMP de cette page.

```html
<!-- Dans le <head> de la page canonique (HTML standard) -->
<link rel="amphtml" href="https://www.exemple.com/article?amp=1">
```

### Le tag `rel="canonical"` côté AMP

Réciproquement, la page AMP doit pointer vers la page canonique :

```html
<!-- Dans le <head> de la page AMP -->
<link rel="canonical" href="https://www.exemple.com/article">
```

### Relation canonique bidirectionnelle

```
Page standard                    Page AMP
     |                                |
     |── rel="amphtml" ─────────────→ |
     |                                |
     |← ── rel="canonical" ──────────|
```

> **Important** : Si une page n'existe qu'en version AMP (sans version standard), la page AMP doit être auto-canonique (`<link rel="canonical" href="[URL AMP elle-même]">`).

---

## Implémentation selon la stratégie

### Option 1 : URLs séparées (approche classique)
- Page standard : `https://exemple.com/article`
- Page AMP : `https://exemple.com/article/amp/` ou `?amp=1`

### Option 2 : Page unique AMP (AMP-first)
- Une seule URL, la page est nativement AMP
- Auto-référencement canonique

### Option 3 : Paired AMP avec CMS
La plupart des CMS majeurs proposent des plugins officiels :
- **WordPress** : Plugin officiel AMP (automatique)
- **Drupal** : Module AMP
- **Shopify** : Support natif partiel

---

## AMP en 2026 {#amp-en-2026}

### Évolution du contexte

| Événement | Date | Impact |
|-----------|------|--------|
| Lancement AMP | Oct 2015 | Début de l'adoption massive |
| AMP requis pour Top Stories | 2016 | Pic d'adoption |
| Annonce suppression privilège AMP | Nov 2020 | Début du déclin |
| Core Web Vitals remplace AMP pour Top Stories | Juin 2021 | Perte de l'avantage SEO |
| Google réduit ses investissements AMP | 2022-2023 | Signal de dépriorisation |
| Part de pages AMP en déclin mesurable | 2024-2026 | Abandon progressif |

### Pourquoi AMP est en déclin

1. **Suppression du privilège SEO** : Google n'exige plus AMP pour le Top Stories mobile. Seule la performance (Core Web Vitals) compte.
2. **Alternatives matures** : Next.js, Astro, Nuxt offrent des performances équivalentes sans les contraintes AMP.
3. **URLs AMP invasives** : Les URLs `cdn.ampproject.org` empêchaient le partage de l'URL réelle.
4. **Restrictions trop fortes** : Pas de JS custom, fonctionnalités marketing limitées.
5. **Complexité de maintenance** : Deux versions à maintenir en parallèle.

### Que faire en 2026 ?

**Si vous avez déjà AMP** :
- Évaluer le trafic AMP dans GA4 (segment `amp=1` ou source AMP cache)
- Si trafic marginal (<5%) : planifier la migration vers page unique responsive
- Si trafic significatif : maintenir mais ne plus investir dans AMP

**Si vous n'avez pas AMP** :
- Ne pas l'implémenter pour un nouveau projet
- Investir à la place dans les **Core Web Vitals** (LCP, INP, CLS)

**Alternative recommandée** : Framework moderne avec SSG/SSR (Next.js, Astro) + optimisation CWV.

---

## AMP vs Core Web Vitals

| Critère | AMP | Core Web Vitals |
|---------|-----|-----------------|
| Garantie de performance | ✅ Haute (si respecté) | Dépend de l'implémentation |
| Liberté de design | ❌ Très limitée | ✅ Totale |
| JS custom | ❌ Interdit | ✅ Libre |
| Avantage SEO | ❌ Supprimé | ✅ Facteur de ranking |
| Maintenance | ❌ Double version | ✅ Version unique |
| Adoption 2026 | 📉 En baisse | 📈 Standard |

---

## Validation et outils

| Outil | Usage |
|-------|-------|
| [AMP Validator](https://validator.ampproject.org/) | Valider la conformité AMP |
| **Google Search Console** → AMP | Erreurs et avertissements AMP |
| **Chrome DevTools** | Onglet AMP dans le panneau réseau |
| **Lighthouse** | Audit performance (remplace AMP pour les métriques) |

---

## Voir aussi

- [Canonical](./Canonical.md)
- [DOM et CSSOM](./DOM_et_CSSOM.md)
- [CDN](./CDN.md)
- [Key Locations SEO](./Key_Locations_SEO.md)
