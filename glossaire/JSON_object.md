# JSON (JavaScript Object Notation)

> **Catégorie** : Format de données / APIs / Développement Web / SEO Structured Data  
> **Dernière mise à jour** : 2026

---

## Définition

**JSON** (JavaScript Object Notation) est un format léger d'échange de données, indépendant du langage de programmation. Basé sur la syntaxe des objets JavaScript, il est conçu pour être **facile à lire par les humains** et **facile à parser par les machines**. Défini par la [RFC 8259](https://tools.ietf.org/html/rfc8259) et le standard ECMA-404, JSON est devenu le format d'échange dominant sur le web, remplaçant largement XML dans la plupart des cas d'usage.

En SEO, JSON est fondamental via le format **JSON-LD**, utilisé pour les données structurées (schema.org) qui alimentent les rich results de Google.

---

## Structure et types de données

### Les 6 types primitifs JSON

| Type | Exemple | Description |
|------|---------|-------------|
| **String** | `"Hello, monde"` | Chaîne entre guillemets doubles |
| **Number** | `42`, `3.14`, `-7` | Entier ou décimal, pas de distinction |
| **Boolean** | `true`, `false` | Littéraux en minuscules |
| **Null** | `null` | Valeur nulle |
| **Object** | `{"clé": valeur}` | Collection de paires clé-valeur |
| **Array** | `[1, 2, 3]` | Liste ordonnée de valeurs |

### Objet JSON

```json
{
  "nom": "John Doe",
  "age": 30,
  "email": "john@example.com",
  "actif": true,
  "adresse": null,
  "tags": ["développeur", "javascript", "seo"],
  "coordonnées": {
    "latitude": 48.8566,
    "longitude": 2.3522
  }
}
```

### Règles de syntaxe

- Les clés doivent être des **strings entre guillemets doubles**
- Pas de guillemets simples (`'clé'` → invalide)
- Pas de commentaires (contrairement à JSON5 ou JSONC)
- Pas de virgule finale (trailing comma) : `["a", "b",]` → invalide
- L'encodage recommandé est **UTF-8**
- Les valeurs `undefined`, `NaN`, `Infinity` ne sont **pas valides en JSON** (JavaScript seulement)

---

## Exemples pratiques

### Profil utilisateur
```json
{
  "id": 1234,
  "username": "alice_dev",
  "email": "alice@example.com",
  "createdAt": "2024-03-15T09:30:00Z",
  "preferences": {
    "language": "fr",
    "theme": "dark",
    "notifications": true
  },
  "roles": ["user", "editor"]
}
```

### Réponse API paginée
```json
{
  "data": [
    {"id": 1, "title": "Article 1", "slug": "article-1"},
    {"id": 2, "title": "Article 2", "slug": "article-2"}
  ],
  "pagination": {
    "page": 1,
    "perPage": 10,
    "total": 234,
    "totalPages": 24
  },
  "status": "success"
}
```

---

## JSON en JavaScript

### Parsing (String → Objet JS)
```javascript
const jsonString = '{"nom": "Alice", "age": 25}';
const obj = JSON.parse(jsonString);
console.log(obj.nom); // "Alice"

// Avec gestion d'erreur
try {
  const data = JSON.parse(jsonString);
} catch (e) {
  console.error('JSON invalide:', e.message);
}
```

### Sérialisation (Objet JS → String)
```javascript
const user = { nom: "Bob", age: 30, actif: true };
const jsonString = JSON.stringify(user);
// '{"nom":"Bob","age":30,"actif":true}'

// Formaté (indentation 2 espaces)
const jsonFormatted = JSON.stringify(user, null, 2);
/*
{
  "nom": "Bob",
  "age": 30,
  "actif": true
}
*/
```

### Fetch API + JSON (usage moderne)
```javascript
// GET
const response = await fetch('https://api.exemple.com/articles');
const articles = await response.json();

// POST avec JSON
const newArticle = await fetch('https://api.exemple.com/articles', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Mon Article', content: '...' })
});
```

---

## JSON-LD : JSON pour le SEO

### Qu'est-ce que JSON-LD ?

**JSON-LD** (JSON for Linked Data) est un format de données structurées recommandé par Google pour implémenter les **rich results** (résultats enrichis). Il est basé sur JSON mais enrichi avec un contexte (`@context`) qui lie les données au vocabulaire **schema.org**.

> Google préfère JSON-LD aux autres formats (Microdata, RDFa) pour sa facilité d'implémentation et de maintenance.

### Syntaxe JSON-LD

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Guide complet du JSON pour le SEO",
  "author": {
    "@type": "Person",
    "name": "Alice Dupont"
  },
  "datePublished": "2026-01-15",
  "dateModified": "2026-04-20",
  "image": "https://exemple.com/images/article-hero.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "Mon Site",
    "logo": {
      "@type": "ImageObject",
      "url": "https://exemple.com/logo.png"
    }
  }
}
</script>
```

### Types schema.org les plus utiles pour le SEO

| Type | Rich Result généré | Usage |
|------|:-----------------:|-------|
| `Article` / `NewsArticle` | Article dans Top Stories | Blog, presse |
| `Product` | Prix, stock, avis | E-commerce |
| `FAQPage` | Accordion FAQ dans SERP | Pages FAQ |
| `HowTo` | Étapes avec images | Tutoriels |
| `Recipe` | Carte recette | Cuisine |
| `Event` | Événement dans SERP | Billetterie, événements |
| `JobPosting` | Offre d'emploi | RH, recrutement |
| `LocalBusiness` | Knowledge Panel | Commerce local |
| `BreadcrumbList` | Fil d'Ariane dans l'URL SERP | Tous sites |
| `VideoObject` | Miniature vidéo | Contenu vidéo |
| `Review` / `AggregateRating` | Étoiles dans les résultats | Avis produits |

### Exemple JSON-LD complet pour un produit e-commerce

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Chaussures Running Pro X500",
  "description": "Chaussures de running légères avec semelle amortissante",
  "sku": "RUN-X500-42",
  "brand": {
    "@type": "Brand",
    "name": "SportTech"
  },
  "image": [
    "https://exemple.com/produits/x500-1.jpg",
    "https://exemple.com/produits/x500-2.jpg"
  ],
  "offers": {
    "@type": "Offer",
    "url": "https://exemple.com/chaussures/x500",
    "priceCurrency": "EUR",
    "price": "129.99",
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "2026-12-31"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "reviewCount": "248"
  }
}
</script>
```

---

## JSONL (JSON Lines)

Format dérivé de JSON où **chaque ligne est un objet JSON valide** et indépendant. Utilisé pour les flux de données et le streaming.

```jsonl
{"id": 1, "event": "page_view", "url": "/accueil", "timestamp": "2026-01-15T10:00:00Z"}
{"id": 2, "event": "click", "element": "nav-menu", "timestamp": "2026-01-15T10:00:05Z"}
{"id": 3, "event": "page_view", "url": "/produits", "timestamp": "2026-01-15T10:00:08Z"}
```

---

## JSON vs XML vs YAML

| Critère | JSON | XML | YAML |
|---------|:----:|:---:|:----:|
| Lisibilité humaine | ✅ Bonne | ⚠️ Verbeuse | ✅ Excellente |
| Légèreté | ✅ Léger | ❌ Verbeux | ✅ Léger |
| Support schemas | ⚠️ JSON Schema | ✅ XSD/DTD | ⚠️ YAML Schema |
| Commentaires | ❌ Non | ✅ Oui | ✅ Oui |
| Types de données | ⚠️ Limités | ❌ Tout texte | ✅ Riches |
| Usage web dominant | ✅ APIs REST | ⚠️ Legacy/SOAP | ✅ Config files |
| SEO (données structurées) | ✅ JSON-LD | ⚠️ RDFa | ❌ Non supporté |

---

## Validation et outils

| Outil | Usage |
|-------|-------|
| [jsonlint.com](https://jsonlint.com) | Validation et formatage JSON |
| [json-schema.org](https://json-schema.org) | Définir des schémas JSON |
| **Google Rich Results Test** | Tester les données JSON-LD |
| **Schema.org Validator** | Validation schema.org |
| `jq` (CLI) | Manipulation JSON en ligne de commande |
| **Postman / Insomnia** | Tester les APIs JSON |

---

## Voir aussi

- [AJAX](./AJAX.md)
- [DOM et CSSOM](./DOM_et_CSSOM.md)
- [Key Locations SEO](./Key_Locations_SEO.md)
