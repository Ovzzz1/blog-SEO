# CDN (Content Delivery Network)

> **Catégorie** : Infrastructure Web / Performance / SEO International  
> **Dernière mise à jour** : 2026

---

## Définition

Un **CDN (Content Delivery Network)** est un réseau de serveurs distribués géographiquement à travers le monde, conçu pour servir le contenu web aux utilisateurs depuis le point de présence (PoP) le plus proche de leur localisation. L'objectif principal est de **réduire la latence** et d'**améliorer les temps de chargement** en minimisant la distance physique que les données doivent parcourir.

Les CDN sont devenus des composants critiques de l'infrastructure web moderne, servant non seulement des fichiers statiques (images, CSS, JS) mais aussi des pages entières, des APIs, et même des fonctions serverless (edge computing).

---

## Comment fonctionne un CDN

### Sans CDN
```
Utilisateur (Tokyo) ──────────────── Serveur Origine (Paris)
                     ~150ms latence
```

### Avec CDN
```
Utilisateur (Tokyo) ──── PoP CDN (Tokyo) ── Serveur Origine (Paris)
                    ~5ms              (si non en cache)
```

### Mécanisme de cache

1. L'utilisateur demande `https://exemple.com/image.jpg`
2. Le CDN vérifie si la ressource est en cache au PoP le plus proche
3. **Cache HIT** : La ressource est servie directement depuis le PoP (~millisecondes)
4. **Cache MISS** : Le CDN interroge le serveur d'origine, met en cache, puis sert la réponse
5. Les requêtes suivantes pour cette ressource dans la même région utilisent le cache

### Headers CDN essentiels

```http
Cache-Control: public, max-age=31536000, immutable  # Ressources statiques
Cache-Control: public, max-age=300, s-maxage=3600   # Pages dynamiques
X-Cache: HIT                                         # Indique un cache hit
CF-Cache-Status: HIT                                 # Header Cloudflare
Age: 7234                                            # Âge de la ressource en cache (secondes)
```

---

## Impact sur les Core Web Vitals et le SEO

### LCP (Largest Contentful Paint)
Le CDN accélère directement le LCP en servant les images et ressources heroïques depuis un nœud proche. **C'est l'un des gains les plus rapides pour le LCP.**

### TTFB (Time To First Byte)
Un CDN bien configuré réduit le TTFB de plusieurs centaines de millisecondes, voire secondes pour les utilisateurs éloignés du serveur d'origine.

### Impact sur le classement Google
Depuis l'introduction des **Core Web Vitals** comme facteur de ranking (2021), la performance est directement liée au positionnement. Un CDN est l'un des leviers les plus efficaces pour améliorer les scores CWV.

| Métrique | Impact CDN | Gain typique |
|----------|:----------:|:------------:|
| LCP | ✅ Fort | -30% à -60% |
| TTFB | ✅ Fort | -50% à -80% |
| CLS | Neutre | - |
| INP | ⚠️ Indirect | Marginal |

---

## CDN et SEO International

### Problème sans CDN
Pour un site ciblant l'Europe, l'Asie et les Amériques depuis un seul serveur parisien, les utilisateurs asiatiques peuvent subir 300-400ms de latence rien que sur le TTFB, pénalisant directement leur expérience et le score CWV de la région.

### Solution CDN multi-région
Les CDN modernes permettent de configurer des règles géographiques :
- Servir des versions localisées selon la géolocalisation IP
- Configurer des headers `Vary: Accept-Language` pour les versions hreflang
- Router vers des backends régionaux (edge routing)

### Cas particulier : La Chine 🇨🇳

La Chine représente un cas unique qui nécessite une attention particulière :

- Le **Grand Firewall** bloque ou ralentit fortement de nombreux CDN occidentaux
- Cloudflare, AWS CloudFront, Fastly ont des performances dégradées en Chine sans accord local
- **Solution** : ICP License (备案) + CDN local (Alibaba Cloud CDN, Tencent CDN, Baidu CDN)
- Sans infrastructure locale, les temps de chargement peuvent dépasser 5-10 secondes

**Recommandation 2026** : Pour cibler la Chine, un CDN avec PoP mainland China (nécessitant une ICP license) est indispensable.

### Autres marchés spécifiques
- **Russie** : Yandex Cloud CDN pour les meilleures performances locales
- **Inde** : Couverture CDN généralement bonne (Mumbai, Chennai), mais vérifier la présence en Inde du Nord
- **Afrique** : CDN coverage encore inégale ; Cloudflare a investi massivement en 2022-2024

---

## Types de CDN et acteurs majeurs (2026)

### CDN généralistes

| CDN | Points forts | Cas d'usage |
|-----|-------------|-------------|
| **Cloudflare** | 300+ PoP, DDoS, Workers (edge) | Tout type de site, edge computing |
| **AWS CloudFront** | Intégration AWS, Lambda@Edge | Projets AWS |
| **Fastly** | Purge instantanée, Compute@Edge | Médias, streaming, APIs |
| **Akamai** | Réseau le plus vaste, SLA enterprise | Grands groupes, e-commerce |
| **BunnyCDN** | Excellent rapport qualité/prix | PME, blogs |

### CDN spécialisés
- **Cloudinary** / **imgix** : CDN + optimisation d'images à la volée (WebP, AVIF, resize)
- **jsDelivr** / **cdnjs** : CDN open-source pour librairies JS
- **Vercel Edge Network** / **Netlify Edge** : CDN intégré pour JAMstack

---

## CDN et Edge Computing

L'évolution majeure 2022-2026 : les CDN ne servent plus uniquement des fichiers statiques. Ils exécutent désormais du code **à la périphérie du réseau** (edge), permettant :

- **Personnalisation** sans latence de serveur central
- **A/B testing** au niveau CDN
- **Authentification** à l'edge (avant même d'atteindre le serveur d'origine)
- **Réécriture d'URLs** en temps réel
- **Redirections géographiques** (hreflang dynamique)

```javascript
// Exemple Cloudflare Worker (edge function)
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const country = request.cf.country;
  if (country === 'FR') {
    return Response.redirect('https://exemple.com/fr/', 302);
  }
  return fetch(request);
}
```

---

## Configuration SEO d'un CDN

### Headers à configurer

```
# Ressources statiques (JS, CSS, polices) - cache long
Cache-Control: public, max-age=31536000, immutable

# Pages HTML - cache court avec revalidation
Cache-Control: public, max-age=0, s-maxage=3600, must-revalidate

# APIs - pas de cache CDN
Cache-Control: private, no-cache
```

### Pièges à éviter

1. **Cacher les pages avec personnalisation** → Servir le même contenu à tous les utilisateurs
2. **Oublier de purger le cache** après une mise à jour de contenu
3. **Bloquer Googlebot via CDN** → Vérifier les règles WAF/bot management
4. **URLs CDN exposées dans le sitemap** → Toujours utiliser les URLs canoniques du domaine

### Vérification que Googlebot n'est pas bloqué
```bash
# Simuler Googlebot
curl -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
  https://exemple.com/page
```

---

## Outils de diagnostic

| Outil | Usage |
|-------|-------|
| **GTmetrix** / **WebPageTest** | Test depuis différentes localisations |
| **Pingdom** | TTFB par région |
| **KeyCDN Performance Test** | Test multi-régions |
| **Google PageSpeed Insights** | Score CWV réel (Field Data) |
| `curl -I` + headers | Vérifier Cache-Control et X-Cache |

---

## Voir aussi

- [DOM et CSSOM](./DOM_et_CSSOM.md)
- [Key Locations SEO](./Key_Locations_SEO.md)
- [Crawl Budget](./Crawl_Budget.md)
- [Hreflang](./Hreflang.md)
