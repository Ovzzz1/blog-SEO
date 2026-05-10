# Follow et Nofollow (`rel="nofollow"`, `rel="ugc"`, `rel="sponsored"`)

> **Catégorie** : SEO Technique / Liens / PageRank  
> **Dernière mise à jour** : 2026

---

## Définition

L'attribut `rel` sur une balise `<a>` permet de qualifier la **nature de la relation** entre la page source et la page de destination d'un lien. En SEO, sa valeur la plus connue est `nofollow`, qui indique aux moteurs de recherche de ne pas transmettre de **link equity (PageRank)** via ce lien et de ne pas le prendre en compte pour le classement de la page de destination.

En **septembre 2019**, Google a introduit deux nouveaux attributs complémentaires : `rel="ugc"` et `rel="sponsored"`, transformant `nofollow` en un ensemble de valeurs permettant de qualifier plus précisément l'origine d'un lien.

---

## Les valeurs de l'attribut `rel` pour les liens

### `rel="follow"` (ou absence d'attribut)

Il n'existe pas de valeur `follow` à proprement parler — un lien est **suivi par défaut** si aucun attribut `rel` restrictif n'est présent.

```html
<!-- Lien suivi (transmet du PageRank) -->
<a href="https://exemple.com/page">Texte du lien</a>

<!-- Équivalent explicite — rarement nécessaire -->
<a href="https://exemple.com/page" rel="follow">Texte du lien</a>
```

### `rel="nofollow"`

Introduit par Google en **2005**, `nofollow` indique aux moteurs de recherche de ne **pas suivre ce lien** ni de lui transférer du PageRank.

```html
<a href="https://exemple.com" rel="nofollow">Lien nofollow</a>
```

**Depuis septembre 2019** : Google traite `nofollow` comme un **hint** (indice) et non plus comme une directive absolue. En pratique, Google peut choisir de suivre et d'indexer la page de destination, mais sans lui attribuer de PageRank via ce lien.

### `rel="ugc"` (User Generated Content)

Introduit en 2019 pour les **liens générés par les utilisateurs** : commentaires de blog, forums, reviews, wikis, etc.

```html
<!-- Dans les commentaires d'un blog ou d'un forum -->
<a href="https://example.com" rel="ugc">Lien posté par un utilisateur</a>

<!-- Combinable avec nofollow -->
<a href="https://example.com" rel="ugc nofollow">Lien</a>
```

### `rel="sponsored"`

Pour les **liens payants**, partenariats, publicités, liens d'affiliation. L'utilisation de `sponsored` est obligatoire selon les guidelines Google pour tout lien rémunéré.

```html
<!-- Lien d'affiliation -->
<a href="https://partenaire.com?ref=monsite" rel="sponsored">Partenaire</a>

<!-- Publicité -->
<a href="https://pub.com" rel="sponsored nofollow">Notre sponsor</a>
```

> ⚠️ Ne pas qualifier les liens sponsorisés avec `sponsored` peut être interprété comme une tentative de manipulation des résultats de recherche (black hat link building) et entraîner une pénalité manuelle.

---

## Tableau comparatif

| Valeur | Introduit | Transmet PageRank | Suivi par Google | Usage |
|--------|:---------:|:-----------------:|:----------------:|-------|
| *(aucun)* | — | ✅ Oui | ✅ Oui | Lien éditorial normal |
| `nofollow` | 2005 | ❌ Non (hint) | ⚠️ Possible | Liens non cautionnés |
| `ugc` | 2019 | ❌ Non (hint) | ⚠️ Possible | Contenu généré par utilisateurs |
| `sponsored` | 2019 | ❌ Non | ⚠️ Possible | Liens payants / affiliation |

---

## Utilisations recommandées

### Quand utiliser `nofollow`

- Liens vers des sites non vérifiés ou de confiance inconnue
- Liens dans les commentaires ou les forums (si pas d'UGC disponible)
- Liens vers des pages légales/mentions légales de partenaires sans endorsement éditorial
- Widget links, badges automatiques

### Quand utiliser `ugc`

- Commentaires de blog
- Posts dans des forums ou communautés
- Contributions wiki ouvertes
- Reviews et avis utilisateurs

### Quand utiliser `sponsored`

- Liens d'affiliation (Amazon Associates, Awin, ShareASale…)
- Articles sponsorisés / publi-rédactionnels
- Bannières et liens publicitaires
- Partenariats rémunérés

### Combinaisons valides

```html
rel="ugc nofollow"          <!-- Contenu user + nofollow -->
rel="sponsored nofollow"    <!-- Sponsorisé + nofollow -->
rel="noopener noreferrer"   <!-- Sécurité + pas de referrer (links target=_blank) -->
rel="nofollow noopener"     <!-- Nofollow + sécurité -->
```

---

## `nofollow` sur les liens internes : attention

L'utilisation de `nofollow` sur des liens internes est **généralement déconseillée**.

### Historique : PageRank Sculpting

Entre 2005 et 2009, certains SEOs utilisaient `nofollow` sur des liens internes pour "sculpter" le flux de PageRank et le concentrer sur les pages importantes. Google a mis fin à cette pratique en 2009 en annonçant que le PageRank est **toujours consommé** même si le lien est nofollow (il disparaît, il n'est pas redistribué).

### Conséquences du nofollow interne en 2026

1. **Crawl Budget** : Les liens internes nofollow peuvent empêcher Googlebot de découvrir certaines pages, réduisant l'efficacité du crawl
2. **PageRank** : Le PageRank est "perdu" dans le vide plutôt que distribué aux autres pages
3. **Navigation utilisateur** : Un nofollow interne peut créer des impasses de navigation
4. **Cas exceptionnel valide** : Lien vers une page de connexion, une page de panier, ou des zones purement transactionnelles

### Alternatives recommandées au nofollow interne

| Problème | Solution recommandée |
|----------|---------------------|
| Page à ne pas indexer | `<meta name="robots" content="noindex">` |
| Page à ne pas crawlér | `Disallow` dans `robots.txt` |
| Concentrer le PageRank | Améliorer l'architecture et le maillage interne |
| Liens de navigation répétitifs | Laisser en follow — c'est normal |

---

## `nofollow` sur les liens externes

C'est le cas d'usage principal et légitime.

### Bonnes pratiques pour les liens externes

```html
<!-- ✅ Lien éditorial vers un contenu de qualité que vous cautionnez -->
<a href="https://source-fiable.com/etude">Selon cette étude</a>

<!-- ✅ Lien affilié clairement identifié -->
<a href="https://amazon.fr/produit?tag=monsite" rel="sponsored">
  Voir le produit sur Amazon
</a>

<!-- ✅ Commentaire utilisateur -->
<a href="https://siteutilisateur.com" rel="ugc nofollow">
  Site de Jean Dupont
</a>

<!-- ✅ Lien vers site non vérifié / annuaire -->
<a href="https://site-inconnu.com" rel="nofollow">
  Voir leur site
</a>
```

---

## Impact du nofollow sur le référencement : nuances 2026

### Ce que `nofollow` ne fait PAS

- Il ne rend pas la page de destination invisible pour Google
- Il n'empêche pas l'indexation de la page de destination (si elle a d'autres liens entrants)
- Il ne supprime pas le lien des logs de crawl de Google
- Il n'empêche pas les utilisateurs de cliquer sur le lien

### Ce que `nofollow` fait

- Signale à Google de ne pas attribuer de PageRank via ce lien
- Peut réduire la découverte de nouvelles URLs via ce lien (mais Google reste libre)
- Protège contre une pénalité algorithmique si les liens sortants sont de mauvaise qualité

### Le cas des liens de presse / RP en 2026

Les liens dans les communiqués de presse et articles sponsorisés doivent utiliser `sponsored` ou `nofollow`. Google peut pénaliser des sites qui construisent leur profil de liens principalement via des RP avec des liens follow.

---

## Audit et détection

### Screaming Frog
- Rapport "All Outlinks" → filtrer par `rel` attribute
- Détecter les liens internes nofollow involontaires
- Identifier les liens affiliés non qualifiés

### Google Search Console
- Rapport "Liens" → vérifier la distribution des liens entrants
- Pas de vue directe sur les nofollow (GSC ne les distingue pas des follow dans le rapport)

### Ahrefs / Semrush
- Profil de backlinks avec distinction follow/nofollow
- Ratio follow/nofollow du profil de liens entrants (un ratio très déséquilibré peut sembler artificiel)

### Vérification manuelle
```bash
# Vérifier les attributs rel sur une page
curl -s https://exemple.com/page | grep -oP 'rel="[^"]*"' | sort | uniq -c
```

---

## Voir aussi

- [Canonical](./Canonical.md)
- [Crawl Budget](./Crawl_Budget.md)
- [Robots Meta Tag](./Robots_Meta_Tag.md)
- [X-Robots-Tag](./X_Robots_Tag.md)
- [Robots.txt](./Robots_txt.md)
