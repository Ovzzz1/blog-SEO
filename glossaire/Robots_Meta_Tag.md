# Robots Meta Tag

> **Catégorie** : SEO Technique / Indexation / Directives aux bots  
> **Dernière mise à jour** : 2026

---

## Définition

La **balise meta robots** est une directive HTML placée dans la section `<head>` d'une page web qui indique aux robots des moteurs de recherche comment **indexer** cette page et **suivre** ses liens. Contrairement au fichier `robots.txt` qui contrôle l'accès au crawl, la balise meta robots est lue **après que le bot a crawlé la page** et agit au niveau de l'indexation.

C'est l'un des outils les plus précis pour contrôler la visibilité individuelle d'une page dans les moteurs de recherche.

---

## Syntaxe

### Syntaxe de base

```html
<meta name="robots" content="directive1, directive2">
```

### Cibler un bot spécifique

```html
<!-- Directive pour tous les bots -->
<meta name="robots" content="noindex, nofollow">

<!-- Directive spécifique à Googlebot -->
<meta name="googlebot" content="noindex, nofollow">

<!-- Directive spécifique à Bingbot -->
<meta name="bingbot" content="noindex">

<!-- Les deux coexistent — Googlebot suit la règle la plus spécifique -->
<meta name="robots" content="noindex">
<meta name="googlebot" content="noindex, nosnippet">
```

---

## Les directives disponibles

### Contrôle de l'indexation

| Directive | Effet |
|-----------|-------|
| `index` | ✅ Autorise l'indexation (comportement par défaut) |
| `noindex` | ❌ Exclut la page de l'index |

### Contrôle du suivi des liens

| Directive | Effet |
|-----------|-------|
| `follow` | ✅ Autorise le suivi des liens (comportement par défaut) |
| `nofollow` | ❌ Empêche le suivi de tous les liens de la page |

### Contrôle des snippets et aperçus

| Directive | Effet |
|-----------|-------|
| `snippet` | ✅ Autorise les extraits dans les SERPs (défaut) |
| `nosnippet` | ❌ Aucun extrait de texte ni aperçu vidéo dans les SERPs |
| `max-snippet:[n]` | Limite l'extrait à **n** caractères (ex : `max-snippet:160`) |
| `max-image-preview:[valeur]` | Taille max des aperçus d'image : `none`, `standard`, `large` |
| `max-video-preview:[n]` | Durée max de l'aperçu vidéo en secondes (`-1` = illimité) |

### Contrôle du cache et archivage

| Directive | Effet |
|-----------|-------|
| `noarchive` | ❌ Ne pas mettre en cache la page (supprime le lien "En cache") |
| `nocache` | Alias de `noarchive` pour certains bots (non standard) |
| `noimageindex` | ❌ Ne pas indexer les images de cette page |

### Directives temporelles

| Directive | Effet |
|-----------|-------|
| `unavailable_after: [date]` | Ne plus indexer après la date spécifiée (format RFC 850) |

```html
<!-- Contenu d'un événement, à désindexer après la date -->
<meta name="robots" content="index, unavailable_after: 2026-12-31T23:59:59Z">
```

---

## Exemples pratiques

### Page standard (comportement par défaut)
```html
<!-- Équivalent à ne rien mettre — tout est autorisé par défaut -->
<meta name="robots" content="index, follow">
```

### Exclure complètement une page de l'index
```html
<meta name="robots" content="noindex, nofollow">
```

### Exclure de l'index mais suivre les liens (pour conserver le flux de PageRank)
```html
<meta name="robots" content="noindex, follow">
```

### Page indexée mais sans extrait dans les SERPs (ex : page produit premium)
```html
<meta name="robots" content="index, nosnippet">
```

### Contrôle fin des snippets (recommandé pour les médias)
```html
<meta name="robots" content="max-snippet:300, max-image-preview:large, max-video-preview:10">
```

### Page de confirmation de commande
```html
<!-- Ne pas indexer les pages de confirmation transactionnelles -->
<meta name="robots" content="noindex, nofollow">
```

### Page de résultats de recherche interne
```html
<meta name="robots" content="noindex, follow">
```

---

## Règles de priorité et conflits

### Conflit robots.txt vs meta robots

| Scénario | Résultat |
|----------|---------|
| `robots.txt` Disallow + `<meta noindex>` | Page non crawlée → Google **ne peut pas lire le noindex** → page peut rester dans l'index si elle a des liens entrants |
| `robots.txt` Allow + `<meta noindex>` | ✅ Google crawle la page, lit le noindex, la déindexe |

> **Piège classique** : Bloquer une page dans `robots.txt` ET mettre un `noindex` dessus. Le noindex n'est jamais lu car Google ne peut pas crawler la page. Si vous voulez déindexer une page, **ne la bloquez pas dans robots.txt**.

### Conflit entre directives multiples

En présence de plusieurs balises meta robots ou directives contradictoires, Google applique la directive la **plus restrictive** :

```html
<!-- Google appliquera noindex (plus restrictif) -->
<meta name="robots" content="index">
<meta name="robots" content="noindex">
```

---

## Meta robots vs X-Robots-Tag vs robots.txt

| Mécanisme | Où ? | Contrôle | Portée |
|-----------|------|----------|--------|
| **robots.txt** | Fichier racine | Crawl | Par chemin URL |
| **Meta Robots** | `<head>` HTML | Indexation | Par page HTML |
| **X-Robots-Tag** | Header HTTP | Indexation | Par ressource (HTML, PDF, images…) |

La meta robots est la méthode privilégiée pour les pages HTML. Pour les fichiers non-HTML (PDF, images), utiliser le [X-Robots-Tag](./X_Robots_Tag.md).

---

## Cas d'usage courants

### Pages à toujours exclure de l'index

| Type de page | Directive recommandée | Raison |
|-------------|----------------------|--------|
| Page de connexion | `noindex, nofollow` | Sans valeur SEO |
| Page de panier | `noindex, nofollow` | Transactionnel, pas de contenu |
| Confirmation de commande | `noindex, nofollow` | Unique par utilisateur |
| Résultats de recherche interne | `noindex, follow` | Contenu dupliqué/thin |
| Pages de tags vides | `noindex, follow` | Thin content |
| Paramètres d'URL (facettes) | `noindex, follow` | Duplication |
| Pages de pagination | `index, follow` (avec canonical) | Indexable mais canonical vers page 1 |
| Pages d'erreur 404 | 404 HTTP suffit | Ne pas forcer noindex |
| Pages de staging | `noindex, nofollow` | Environnement de test |

### Gestion des pages de pagination

```html
<!-- Page 1 : index + self-canonical -->
<link rel="canonical" href="https://exemple.com/blog/">
<meta name="robots" content="index, follow">

<!-- Pages 2, 3, etc. : index avec self-canonical (chaque page a son propre canonical) -->
<link rel="canonical" href="https://exemple.com/blog/page/2/">
<meta name="robots" content="index, follow">
```

---

## Implémentation dans les CMS

### WordPress (avec Yoast SEO / RankMath)

```php
// Dans functions.php — forcer noindex sur une taxonomie custom
add_action('wp_head', function() {
  if (is_tax('color')) {
    echo '<meta name="robots" content="noindex, follow">';
  }
});
```

### Next.js (App Router)

```javascript
// app/page.js
export const metadata = {
  robots: {
    index: false,
    follow: true,
    googleBot: {
      index: false,
      follow: true,
      'max-snippet': -1,
      'max-image-preview': 'large',
    },
  },
}
```

### Nuxt.js

```javascript
// nuxt.config.js ou useHead()
useHead({
  meta: [
    { name: 'robots', content: 'noindex, follow' }
  ]
})
```

---

## Vérification et monitoring

### Google Search Console
- **Rapport Couverture** → "Exclues" → "Exclue par balise 'noindex'" : liste des pages exclues
- **Inspection d'URL** → Section "Indexation de l'URL" : affiche les directives lues par Google

### Screaming Frog
- **Crawl → Meta robots** : liste toutes les pages avec leur directive
- Filtrer par "noindex" pour auditer les exclusions
- Identifier les pages avec `noindex` qui reçoivent des liens internes (PageRank gaspillé)

### Test manuel
```bash
curl -s https://exemple.com/page | grep -i 'name="robots"'
```

---

## Voir aussi

- [Robots.txt](./Robots_txt.md)
- [X-Robots-Tag](./X_Robots_Tag.md)
- [Crawl Budget](./Crawl_Budget.md)
- [Canonical](./Canonical.md)
- [Rel Follow/Nofollow](./Rel_Follow_Nofollow.md)
