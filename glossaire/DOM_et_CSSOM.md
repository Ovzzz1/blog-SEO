# DOM et CSSOM

> **Catégorie** : Navigateur / Rendu Web / Performance / SEO Technique  
> **Dernière mise à jour** : 2026

---

## Définition

Le **DOM** (Document Object Model) et le **CSSOM** (CSS Object Model) sont les deux représentations en mémoire construites par le navigateur lors du chargement d'une page web. Ensemble, ils forment le **Render Tree**, qui sert de base au calcul du layout et au dessin de la page à l'écran.

Comprendre DOM et CSSOM est essentiel pour optimiser les **Core Web Vitals**, détecter les problèmes de rendu JavaScript, et comprendre pourquoi Googlebot peut voir un contenu différent de celui visible dans le navigateur.

---

## Le pipeline de rendu du navigateur (Critical Rendering Path)

```
HTML  →  DOM
                 →  Render Tree  →  Layout  →  Paint  →  Composite
CSS   →  CSSOM
```

### Vue détaillée

```
1. Réseau       : Téléchargement HTML, CSS, JS, polices, images
2. Parsing HTML : Construction du DOM (token → nœuds → arbre)
3. Parsing CSS  : Construction du CSSOM
4. JS Execution : Modification potentielle du DOM/CSSOM
5. Render Tree  : Fusion DOM + CSSOM (éléments visibles seulement)
6. Layout       : Calcul des positions et dimensions (Reflow)
7. Paint        : Remplissage des pixels par couches (Repaint)
8. Composite    : Assemblage des couches sur le GPU
```

---

## Le DOM (Document Object Model)

### Construction

Quand le navigateur reçoit le HTML, il le **tokenise** puis construit un arbre de nœuds :

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Ma Page</title>
  </head>
  <body>
    <h1>Bonjour</h1>
    <p>Paragraphe <strong>important</strong></p>
  </body>
</html>
```

Donne l'arbre DOM :
```
Document
└── html
    ├── head
    │   └── title
    │       └── "Ma Page"
    └── body
        ├── h1
        │   └── "Bonjour"
        └── p
            ├── "Paragraphe "
            └── strong
                └── "important"
```

### Propriétés du DOM

- **Dynamique** : Le DOM peut être modifié par JavaScript à tout moment
- **Interface de programmation** : `document.getElementById()`, `querySelector()`, etc.
- **Vivant** : Reflète l'état actuel de la page, pas juste le HTML initial
- **Lié aux performances** : Un DOM très large (>1500 nœuds) ralentit le rendu

### DOM et SEO

Google crawle et indexe le **DOM rendu** (après exécution JS), pas le HTML source. C'est pourquoi :
- Le contenu injecté par JavaScript est (généralement) indexable
- Mais avec un délai (second wave indexing)
- Les modifications du DOM par JS sont visibles dans l'outil "Inspection d'URL" de GSC

---

## Le CSSOM (CSS Object Model)

### Construction

Parallèlement au DOM, le navigateur parse les feuilles de style CSS et construit le CSSOM, un arbre représentant les styles appliqués à chaque élément.

```css
body { font-size: 16px; color: #333; }
h1   { font-size: 2em; margin-bottom: 0.5em; }
p    { line-height: 1.6; }
p strong { font-weight: bold; color: #000; }
```

Donne un CSSOM où chaque nœud hérite et cumule les styles applicables.

### Caractéristique critique : le CSSOM bloque le rendu

Le CSSOM est un **render-blocking resource** : le navigateur ne peut pas construire le Render Tree (et donc afficher quoi que ce soit) tant que le CSSOM n'est pas complet. C'est pourquoi :

- Le CSS doit être chargé aussi tôt que possible (`<link>` dans le `<head>`)
- Le CSS inline critique (above-the-fold) doit être inliné dans le HTML
- Les feuilles de style volumineuses retardent le rendu initial

---

## Le Render Tree

### Formation

Le Render Tree est construit en combinant DOM et CSSOM :

```
DOM                     CSSOM                   Render Tree
html                    html { display:block }   html
└── body                body { display:block }   └── body
    ├── h1              h1 { display:block }         ├── h1
    └── p               p { display:block }          └── p
        └── span[hidden] span { display:none }           (exclu)
```

**Règles** :
- Les éléments `display:none` sont **exclus** du Render Tree
- Les éléments `visibility:hidden` sont **inclus** (espace réservé mais invisible)
- Les pseudo-éléments CSS (`::before`, `::after`) sont **inclus**
- Les nœuds texte sont inclus comme nœuds feuilles

### Impact SEO du Render Tree

Google utilise le Render Tree pour déterminer ce qui est "visible" sur la page. Du contenu dans le DOM mais masqué via CSS (`display:none` ou `visibility:hidden`) peut recevoir **moins de poids SEO** dans certains contextes.

---

## Layout, Paint et Composite

### Layout (Reflow)
Calcul des dimensions et positions de chaque élément dans le Render Tree. Déclenché par :
- Ajout/suppression de nœuds DOM
- Modification de propriétés CSS géométriques (width, height, margin, padding…)
- Redimensionnement de la fenêtre

Le Reflow est **coûteux** : il recalcule les positions de tous les éléments descendants.

### Paint (Repaint)
Remplissage des pixels : couleurs, ombres, textes, images. Déclenché par les changements visuels (couleur, opacité, background).

### Composite
Assemblage des couches de rendu sur le GPU. Les propriétés `transform` et `opacity` sont gérées au niveau Composite (sans Layout ni Paint), d'où leur utilisation recommandée pour les animations fluides.

---

## Optimisations basées sur DOM/CSSOM

### Critical CSS
Inliner le CSS nécessaire pour le rendu above-the-fold directement dans le `<head>` :

```html
<head>
  <style>
    /* CSS critique — hero, navigation, typographie principale */
    body { font-family: sans-serif; margin: 0; }
    .hero { background: #f0f0f0; padding: 4rem 2rem; }
    h1 { font-size: 2.5rem; line-height: 1.2; }
  </style>
  <!-- CSS non-critique chargé de manière asynchrone -->
  <link rel="stylesheet" href="/styles.css" media="print" onload="this.media='all'">
</head>
```

### Réduire la taille du DOM
Google recommande un DOM < 1500 nœuds pour de bonnes performances. Techniques :
- Lazy rendering des composants hors viewport
- Virtualisation des longues listes (React Virtual, Vue Virtual Scroller)
- Suppression des nœuds inutiles générés par le CMS

### Éviter les Reflows forcés en JS
```javascript
// ❌ Mauvais : force un Reflow à chaque itération
elements.forEach(el => {
  el.style.width = (el.offsetWidth + 10) + 'px'; // lecture + écriture = Reflow forcé
});

// ✅ Bon : batch lecture puis écriture
const widths = elements.map(el => el.offsetWidth); // lecture en batch
elements.forEach((el, i) => {
  el.style.width = (widths[i] + 10) + 'px'; // écriture en batch
});
```

### `content-visibility: auto`
Propriété CSS moderne permettant au navigateur de **sauter le rendu** des éléments hors viewport :

```css
.article-card {
  content-visibility: auto;
  contain-intrinsic-size: 0 200px; /* Placeholder height pendant le skip */
}
```

Gain de performance typique : **50-70% de réduction du temps de rendu initial** sur les longues pages.

---

## DOM/CSSOM et les Core Web Vitals

| Métrique | Lien DOM/CSSOM | Optimisation |
|----------|:--------------:|:------------:|
| **LCP** | Render-blocking CSS retarde le LCP | Critical CSS inline, preload |
| **CLS** | Reflows inattendus causent des décalages | `min-height` sur conteneurs, éviter insertions DOM tardives |
| **INP** | Long Tasks JS sur le DOM bloquent l'interaction | Réduire la taille du DOM, éviter Reflows en JS |

---

## Outils de debug

| Outil | Usage |
|-------|-------|
| **Chrome DevTools → Performance** | Visualiser Layout, Paint, Composite dans la timeline |
| **Chrome DevTools → Rendering** | Activer "Paint flashing", "Layout Shift Regions" |
| **Lighthouse** | Score performance + recommandations DOM |
| **WebPageTest** | Filmstrip du rendu, waterfall chart |
| **GSC → Inspection d'URL** | Voir le DOM rendu par Googlebot |

---

## Voir aussi

- [AJAX](./AJAX.md)
- [CDN](./CDN.md)
- [Key Locations SEO](./Key_Locations_SEO.md)
- [AMP et rel=amphtml](./AMP_et_rel_amphtml.md)
