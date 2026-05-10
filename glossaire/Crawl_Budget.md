# Crawl Budget

> **Catégorie** : SEO Technique / Indexation / Architecture de site  
> **Dernière mise à jour** : 2026

---

## Définition

Le **Crawl Budget** désigne le nombre de pages qu'un moteur de recherche (principalement Googlebot) est prêt à crawler et à traiter sur un site web dans un laps de temps donné. Ce concept, formalisé officiellement par Google dans un billet de blog de 2017, est particulièrement crucial pour les **grands sites** (e-commerce, médias, sites d'actualités, marketplaces) qui publient des milliers, voire des millions d'URLs.

> "Pour la plupart des sites, le crawl budget n'est pas un souci." — Google, 2017  
> Mais pour les sites à forte volumétrie (100K+ URLs) ou à architecture complexe, c'est un facteur limitant réel.

---

## Les deux composantes du Crawl Budget

Google définit le crawl budget comme le produit de deux facteurs :

### 1. Crawl Rate Limit (Limite de taux de crawl)

La **vitesse maximale** à laquelle Googlebot peut crawler un site sans surcharger le serveur. Google ajuste automatiquement ce taux en fonction de :
- **La disponibilité et la réactivité du serveur** : Un serveur lent ou instable amène Google à réduire la fréquence
- **Le signal de limite défini** : Via Google Search Console, on peut demander à Googlebot de ralentir
- **L'historique de crawl** : Google apprend progressivement le comportement du serveur

> Google ne pénalise pas un site dont le serveur signale de la surcharge (503) — il revient plus tard. En revanche, des erreurs répétées peuvent réduire durablement le budget.

### 2. Crawl Demand (Demande de crawl)

La **priorité** que Google accorde au recrawl d'un site, basée sur :
- **La popularité** : Les pages avec beaucoup de backlinks et de trafic sont recrawlées plus souvent
- **La fraîcheur du contenu** : Sites d'actualités, blogs actifs → forte demande
- **L'historique de changement** : Pages qui changent fréquemment → recrawl plus fréquent
- **L'autorité du domaine** : Sites à forte autorité bénéficient d'un budget plus élevé

**Crawl Budget = min(Crawl Rate Limit, Crawl Demand)**

---

## Crawl Waste : l'ennemi du Crawl Budget

Le **Crawl Waste** (gaspillage de budget) survient lorsque Googlebot passe du temps à crawler des URLs qui ne méritent pas d'être indexées. C'est la principale cause d'un crawl budget insuffisant.

### Sources courantes de Crawl Waste

| Source | Description | Ampleur potentielle |
|--------|-------------|:-------------------:|
| **Paramètres d'URL** | `?sort=prix&color=rouge&page=2` | ×100 à ×1000 |
| **Facettes e-commerce** | Filtres générant des URLs uniques | ×1000 à ×100000 |
| **Pagination excessive** | `/page/500` sur un site avec 10 articles | Faible à modéré |
| **Contenu dupliqué** | Mêmes pages avec URLs différentes | ×2 à ×10 |
| **URLs de session** | `/page?sessionid=abc123` | Très élevé |
| **Pages vides/thin content** | Catégories sans produits, tags vides | Modéré |
| **URLs de test/staging** | URLs dev accessibles en prod | Modéré |
| **Pages bloquées puis débloquées** | Signaux contradictoires | Faible |
| **Redirections en chaîne** | A → B → C → D | Modéré |

---

## Crawl Prioritization (Priorisation du crawl)

Google ne crawle pas toutes les URLs avec la même priorité. L'algorithme de priorisation tient compte de :

1. **PageRank interne** : Les pages recevant le plus de liens internes sont crawlées en priorité
2. **Fraîcheur** : Le sitemap avec `<lastmod>` récent envoie un signal de priorité
3. **Profondeur** : Les pages proches de la racine (1-2 clics) sont mieux crawlées
4. **Liens externes** : Les URLs avec des backlinks sont prioritaires
5. **Soumission GSC** : La demande d'indexation manuelle (Inspect URL → Submit) prioritise une URL

---

## Optimiser son Crawl Budget

### Réduire le Crawl Waste

**robots.txt** : Bloquer les URLs inutiles
```
User-agent: Googlebot
Disallow: /search?
Disallow: /cart
Disallow: /checkout
Disallow: /compte/
Disallow: /tag/
```

> ⚠️ `Disallow` empêche le crawl mais pas l'indexation si la page a des liens entrants. Pour l'indexation, utiliser `noindex`.

**Paramètres d'URL dans Google Search Console** :  
GSC → Ancien Search Console → Paramètres d'URL → Indiquer les paramètres qui ne créent pas de contenu unique.

**Noindex sur les pages de faible valeur** :
```html
<meta name="robots" content="noindex, follow">
```

**Canonicals** : Consolider les URLs dupliquées vers une URL de référence.

### Améliorer l'efficacité du crawl

**Vitesse du serveur** : Un TTFB < 200ms encourage Google à crawler plus rapidement.

**Architecture en silo / maillage interne** : Un bon maillage interne aide Googlebot à découvrir et prioriser les pages importantes.

**Sitemap XML à jour** : Ne soumettre que les URLs indexables, avec `<lastmod>` précis.

**Supprimer les pages mortes** : 
- 404 persistants → 410 (suppression définitive) ou recréer la page
- Ne pas laisser des 404 s'accumuler dans l'index

### Monitoring du Crawl Budget

**Google Search Console → Statistiques de crawl** :
- Volume de crawl quotidien
- Temps de réponse moyen
- Codes de réponse (ratio 200/301/404/500)
- Pages crawlées par type (HTML, CSS, JS, images)

**Logs serveur** (source la plus fiable) :
```bash
# Extraire les requêtes Googlebot des logs Apache/Nginx
grep "Googlebot" /var/log/nginx/access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -50
```

---

## Crawl Budget et sites spécifiques

### E-commerce (Shopify, Magento, WooCommerce)
Problème majeur : les facettes de filtrage (taille, couleur, prix) génèrent exponentiellement des URLs.

**Solution** :
- Facettes via JavaScript sans changement d'URL (mais perte de deep linking)
- `noindex` + `follow` sur les URLs de facettes
- Robots.txt sur les paramètres non-sémantiques

### Sites multilingues (Hreflang)
Chaque version linguistique duplique le budget. S'assurer que toutes les URLs hreflang sont bien indexables et de qualité.

### JavaScript-heavy (SPA)
Le rendu JS est plus lent pour Googlebot → consomme plus de budget. Préférer SSR/SSG pour le contenu SEO critique.

---

## Évolutions 2024-2026

- **Google a confirmé en 2024** que le crawl budget reste une contrainte réelle pour les grands sites, même avec des serveurs puissants
- **L'IA de Google (Gemini)** influence de plus en plus les décisions de recrawl, en priorisant les pages à fort "potentiel de réponse" aux requêtes utilisateurs
- **INP (Interaction to Next Paint)**, devenu Core Web Vital en 2024, n'impacte pas directement le crawl budget mais l'expérience de rendu côté Googlebot

---

## Voir aussi

- [Robots.txt](./Robots_txt.md)
- [Robots Meta Tag](./Robots_Meta_Tag.md)
- [XML Sitemap](./XML_Sitemap.md)
- [Canonical](./Canonical.md)
- [3XX HTTP Response Codes](./3XX_HTTP_Response_Codes.md)
- [AJAX](./AJAX.md)
