# XML Sitemap

> **Catégorie** : SEO Technique / Crawl / Indexation  
> **Dernière mise à jour** : 2026

---

## Définition

Un **Sitemap XML** est un fichier structuré au format XML qui liste les URLs d'un site web, accompagnées de métadonnées optionnelles (date de dernière modification, fréquence de changement, priorité). Il sert de **carte routière** fournie aux moteurs de recherche pour les aider à découvrir et crawler efficacement les pages du site.

Introduit en 2005 par Google, le format sitemap.xml est devenu un standard supporté par tous les moteurs majeurs (Google, Bing, Yahoo, Yandex) via le protocole **Sitemaps.org**.

> **Important** : Un sitemap XML ne garantit pas l'indexation des URLs listées. C'est un signal de découverte, pas une directive. Google reste libre d'ignorer des URLs ou de crawler des pages non listées.

---

## Structure d'un Sitemap XML

### Exemple minimal

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.exemple.com/</loc>
  </url>
  <url>
    <loc>https://www.exemple.com/a-propos</loc>
  </url>
  <url>
    <loc>https://www.exemple.com/contact</loc>
  </url>
</urlset>
```

### Exemple complet avec toutes les métadonnées

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.exemple.com/article-important</loc>
    <lastmod>2026-04-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.exemple.com/page-standard</loc>
    <lastmod>2026-01-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
```

---

## Les balises XML détaillées

### `<loc>` *(obligatoire)*

L'URL complète et absolue de la page.

```xml
<loc>https://www.exemple.com/categorie/article-slug</loc>
```

**Règles** :
- URL absolue avec protocole (https://)
- Caractères spéciaux encodés en entités XML : `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`
- Max 2048 caractères par URL

### `<lastmod>` *(recommandé)*

Date de dernière modification au format **W3C Datetime** (ISO 8601).

```xml
<lastmod>2026-04-15</lastmod>              <!-- Date seule -->
<lastmod>2026-04-15T14:30:00+02:00</lastmod>  <!-- Avec heure et timezone -->
<lastmod>2026-04-15T12:30:00Z</lastmod>       <!-- UTC -->
```

> **Note 2026** : Google utilise `<lastmod>` pour prioriser le recrawl. Si vous renseignez cette valeur, elle **doit être précise**. Une `<lastmod>` incorrecte ou toujours mise à la date du jour est contre-productive et peut amener Google à l'ignorer.

### `<changefreq>` *(optionnel, peu utilisé)*

Indication de la fréquence théorique de changement. Google indique officiellement **ne pas en tenir compte** pour programmer les crawls.

```xml
<changefreq>always</changefreq>   <!-- Contenu temps réel -->
<changefreq>hourly</changefreq>
<changefreq>daily</changefreq>
<changefreq>weekly</changefreq>
<changefreq>monthly</changefreq>
<changefreq>yearly</changefreq>
<changefreq>never</changefreq>    <!-- Pages d'archives -->
```

### `<priority>` *(optionnel, peu utilisé)*

Valeur de 0.0 à 1.0 indiquant l'importance relative de la page au sein du site. Google indique **ne pas l'utiliser** pour le classement.

```xml
<priority>1.0</priority>   <!-- Page principale (homepage) -->
<priority>0.8</priority>   <!-- Pages importantes -->
<priority>0.5</priority>   <!-- Pages standard (défaut) -->
<priority>0.3</priority>   <!-- Pages secondaires -->
```

> **Recommandation** : Se concentrer sur `<loc>` et `<lastmod>`. `<changefreq>` et `<priority>` ont un impact négligeable sur le comportement réel de Googlebot.

---

## Sitemap Index

Pour les sites avec plus de **50 000 URLs** (limite par fichier sitemap), utiliser un **sitemap index** qui référence plusieurs sitemaps.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://www.exemple.com/sitemap-pages.xml</loc>
    <lastmod>2026-04-15</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.exemple.com/sitemap-articles.xml</loc>
    <lastmod>2026-04-15</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.exemple.com/sitemap-produits.xml</loc>
    <lastmod>2026-04-15</lastmod>
  </sitemap>
</sitemapindex>
```

**Limites** :
- Max **50 000 URLs** par fichier sitemap
- Max **50 000 sitemaps** dans un sitemap index
- Max **50 Mo** non compressé par fichier (ou 10 Mo compressé en .gz)

---

## Types de Sitemaps spécialisés

### Sitemap Images

Pour aider Google à découvrir et indexer les images d'un site.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://exemple.com/galerie/plage</loc>
    <image:image>
      <image:loc>https://exemple.com/images/plage-coucher-soleil.jpg</image:loc>
      <image:title>Coucher de soleil sur la plage</image:title>
      <image:caption>Photo prise à Biarritz en juillet 2025</image:caption>
    </image:image>
    <image:image>
      <image:loc>https://exemple.com/images/plage-matin.jpg</image:loc>
      <image:title>Plage au lever du soleil</image:title>
    </image:image>
  </url>
</urlset>
```

### Sitemap Vidéo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  <url>
    <loc>https://exemple.com/tutoriels/montage-video</loc>
    <video:video>
      <video:thumbnail_loc>https://exemple.com/thumb/tuto-montage.jpg</video:thumbnail_loc>
      <video:title>Comment monter une vidéo avec Premiere Pro</video:title>
      <video:description>Tutoriel complet pour débutants</video:description>
      <video:content_loc>https://exemple.com/videos/tuto-montage.mp4</video:content_loc>
      <video:duration>1842</video:duration>
      <video:publication_date>2026-03-01T09:00:00+01:00</video:publication_date>
    </video:video>
  </url>
</urlset>
```

### Sitemap News (Google News)

Spécifique aux publications d'actualité inscrites à Google News.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  <url>
    <loc>https://journal.exemple.com/article/evenement-important-2026</loc>
    <news:news>
      <news:publication>
        <news:name>Journal Exemple</news:name>
        <news:language>fr</news:language>
      </news:publication>
      <news:publication_date>2026-04-15T10:30:00+02:00</news:publication_date>
      <news:title>Événement important du 15 avril 2026</news:title>
    </news:news>
  </url>
</urlset>
```

### Sitemap Hreflang

Pour les sites multilingues, certains outils génèrent des sitemaps intégrant les annotations hreflang (voir [Hreflang](./Hreflang.md)).

---

## Ce qu'il faut inclure (et exclure) dans un sitemap

### ✅ À inclure

- Pages canoniques indexables (200 + `index`)
- Pages à fort enjeu SEO
- Nouvelles pages publiées récemment
- Pages mises à jour récemment (avec `<lastmod>` exact)

### ❌ À exclure

| Type de page | Raison |
|-------------|--------|
| Pages en `noindex` | Contradictoire : signaler une page tout en disant de ne pas l'indexer |
| Pages redirigées (301/302) | Lister l'URL finale, pas la source |
| Pages en erreur (404, 410, 5XX) | Inutile voire contre-productif |
| Pages dupliquées non-canoniques | Lister uniquement l'URL canonique |
| Pages bloquées dans robots.txt | Google ne peut pas les crawler |
| Paramètres d'URL (filtres, sessions) | Éviter la dilution du sitemap |
| Pages d'admin / backoffice | Pas de valeur SEO |

---

## Génération du sitemap

### CMS et plugins

| Plateforme | Solution recommandée |
|-----------|---------------------|
| WordPress | Yoast SEO, RankMath, Google XML Sitemaps |
| Shopify | Natif (auto-généré à `/sitemap.xml`) |
| Magento | Extension Sitemap (natif limité) |
| Drupal | Module XML Sitemap |
| Wix | Natif automatique |
| Next.js | `next-sitemap` package |
| Nuxt.js | `@nuxtjs/sitemap` module |
| Astro | `@astrojs/sitemap` integration |

### Génération programmatique (Node.js)

```javascript
const { SitemapStream, streamToPromise } = require('sitemap');
const { createWriteStream } = require('fs');

async function generateSitemap() {
  const sitemap = new SitemapStream({ hostname: 'https://exemple.com' });
  const writeStream = createWriteStream('./public/sitemap.xml');
  
  sitemap.pipe(writeStream);
  
  // Ajouter les URLs depuis la DB
  const pages = await db.getPublishedPages();
  pages.forEach(page => {
    sitemap.write({
      url: page.slug,
      lastmod: page.updatedAt,
      changefreq: 'weekly',
      priority: page.isHomepage ? 1.0 : 0.7
    });
  });
  
  sitemap.end();
  await streamToPromise(sitemap);
  console.log('Sitemap généré');
}
```

### Génération Python (Django)

```python
from django.contrib.sitemaps import Sitemap
from .models import Article

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/articles/{obj.slug}'
```

---

## Compression GZIP

Les sitemaps peuvent être compressés en `.gz` pour réduire la taille (jusqu'à 90% de gain) :

```bash
gzip -k sitemap.xml
# Produit : sitemap.xml.gz (à uploader à côté de sitemap.xml)
```

Déclarer le sitemap compressé dans robots.txt :
```
Sitemap: https://exemple.com/sitemap.xml.gz
```

---

## Soumettre et monitorer le sitemap

### Déclaration dans robots.txt (recommandé)

```
Sitemap: https://exemple.com/sitemap.xml
Sitemap: https://exemple.com/sitemap-images.xml
```

### Soumission dans Google Search Console

1. GSC → **Index** → **Sitemaps**
2. Entrer l'URL du sitemap → **Envoyer**
3. Surveiller le rapport : URLs soumises vs URLs indexées

### Soumission dans Bing Webmaster Tools

Bing dispose de son propre outil de soumission de sitemaps, accessible depuis Bing Webmaster Tools.

### Ping direct (méthode legacy, encore fonctionnelle)

```bash
# Ping Google
curl "https://www.google.com/ping?sitemap=https://exemple.com/sitemap.xml"

# Ping Bing
curl "https://www.bing.com/ping?sitemap=https://exemple.com/sitemap.xml"
```

---

## Monitoring : interpréter les métriques GSC

| Métrique GSC | Signification |
|-------------|--------------|
| **URLs soumises** | Nombre d'URLs dans le sitemap |
| **URLs indexées** | URLs effectivement dans l'index Google |
| Écart important soumises > indexées | Pages de faible qualité, dupliquées, ou bloquées |
| Statut "Succès" | Sitemap lu et traité correctement |
| Statut "En attente" | En cours de traitement |
| Statut "Erreur" | Problème de format XML ou d'accès |

> Un ratio indexées/soumises < 50% est un signal d'audit à creuser : thin content, duplication, pages `noindex` dans le sitemap, etc.

---

## Voir aussi

- [Robots.txt](./Robots_txt.md)
- [Robots Meta Tag](./Robots_Meta_Tag.md)
- [Crawl Budget](./Crawl_Budget.md)
- [Canonical](./Canonical.md)
- [Hreflang](./Hreflang.md)
- [3XX HTTP Response Codes](./3XX_HTTP_Response_Codes.md)
