# AJAX (Asynchronous JavaScript and XML)

> **Catégorie** : Développement Web / JavaScript / SEO Technique  
> **Dernière mise à jour** : 2026

---

## Définition

**AJAX** (Asynchronous JavaScript and XML) est un ensemble de techniques de développement web permettant à un navigateur d'envoyer et recevoir des données depuis un serveur **sans recharger entièrement la page**. Le terme a été popularisé en 2005 par Jesse James Garrett, bien que les technologies sous-jacentes existaient depuis la fin des années 1990.

Malgré son nom, AJAX n'utilise plus nécessairement XML : aujourd'hui, **JSON est le format de données dominant** dans les échanges AJAX.

---

## Comment fonctionne AJAX

### Flux d'une requête AJAX

```
[Utilisateur interagit]
        ↓
[JS crée une requête HTTP asynchrone]
        ↓
[Requête envoyée au serveur en arrière-plan]
        ↓
[Le reste de la page reste interactif]
        ↓
[Serveur renvoie les données (JSON, HTML, XML…)]
        ↓
[JS met à jour le DOM sans rechargement]
```

### Mécanismes techniques

**1. XMLHttpRequest (legacy)**
```javascript
const xhr = new XMLHttpRequest();
xhr.open('GET', '/api/articles');
xhr.onload = function() {
  if (xhr.status === 200) {
    const data = JSON.parse(xhr.responseText);
    // mettre à jour le DOM
  }
};
xhr.send();
```

**2. Fetch API (standard moderne, ES6+)**
```javascript
fetch('/api/articles')
  .then(res => res.json())
  .then(data => {
    document.getElementById('content').innerHTML = renderArticles(data);
  })
  .catch(err => console.error('Erreur:', err));
```

**3. Async/Await (syntaxe recommandée en 2026)**
```javascript
async function loadArticles() {
  try {
    const response = await fetch('/api/articles');
    const data = await response.json();
    updateDOM(data);
  } catch (error) {
    handleError(error);
  }
}
```

---

## Cas d'usage courants

- **Autocomplétion** de champs de recherche (ex : Google Suggest)
- **Chargement infini** (infinite scroll) sur les réseaux sociaux et blogs
- **Mise à jour de paniers** e-commerce sans rechargement
- **Formulaires dynamiques** (ex : calcul de prix en temps réel)
- **Notifications en temps réel** (polling AJAX ou WebSocket)
- **Filtres de recherche** sans rechargement de page
- **Lazy loading** de contenu au scroll

---

## AJAX et SEO : les défis

### Le problème historique

Jusqu'en 2015 environ, les moteurs de recherche ne pouvaient pas exécuter JavaScript, ce qui signifiait que le contenu chargé via AJAX était **invisible pour les bots**. Ce problème a largement disparu avec la montée en capacité du moteur de rendu JavaScript de Google.

### L'état en 2026

Google **exécute JavaScript** et peut crawler le contenu AJAX, mais avec des nuances importantes :

| Aspect | Situation 2026 |
|--------|---------------|
| Rendu JS par Google | ✅ Oui, via Chrome headless (WRS) |
| Délai de rendu | ⚠️ 2e vague de crawl (peut prendre des jours/semaines) |
| Bing / Yandex | ⚠️ Capacités JS limitées |
| Moteurs IA (Perplexity, etc.) | ⚠️ Variable selon implémentation |

### Problèmes persistants

**1. Délai d'indexation (Two-Wave Crawling)**
Google crawle d'abord le HTML brut, puis revient plus tard pour exécuter le JS. Le contenu AJAX peut donc ne pas être indexé immédiatement.

**2. Gestion des URLs**
Si AJAX change le contenu sans changer l'URL, les différents états de la page partagent la même URL, rendant impossible l'indexation de ces états individuellement.

**Solution** : Utiliser l'**History API** (`pushState`) pour mettre à jour l'URL lors des changements de contenu AJAX.

```javascript
// Bonne pratique : mettre à jour l'URL avec le History API
history.pushState({ page: 'articles' }, 'Articles', '/articles');
```

**3. Contenu critique chargé en AJAX**
Si le contenu principal de la page (titres H1, texte SEO, balises meta) est chargé via AJAX et non dans le HTML initial, Google peut :
- Ne pas l'indexer du tout
- L'indexer avec retard
- Lui accorder moins de poids

### Recommandations SEO 2026

| Pratique | Recommandation |
|----------|---------------|
| Contenu SEO critique | Dans le HTML initial (SSR ou SSG) |
| Contenu interactif secondaire | AJAX acceptable |
| URLs des états | Utiliser `pushState` / URL fragments gérés |
| Lazy loading images | `loading="lazy"` natif préférable |
| Infinite scroll | Implémenter la pagination classique en fallback |

---

## AJAX vs SSR vs SSG : quel impact SEO ?

### Server-Side Rendering (SSR)
Le HTML complet est généré côté serveur et envoyé au navigateur. Idéal pour le SEO car Google reçoit directement le contenu.

### Static Site Generation (SSG)
Le HTML est pré-généré au moment du build. Performance maximale, SEO optimal.

### Client-Side Rendering (CSR/AJAX)
Le HTML initial est vide (ou minimal), le contenu est chargé via JS/AJAX. Risqué pour le SEO si le contenu critique n'est pas dans le HTML initial.

### Hydration / Islands Architecture (2024-2026)
Architectures comme **Next.js**, **Astro**, **Nuxt** permettent de combiner SSR/SSG pour le contenu SEO et des îlots AJAX pour les éléments interactifs. C'est l'approche recommandée en 2026.

---

## AJAX et le Crawl Budget

Les requêtes AJAX supplémentaires consomment du crawl budget. Si chaque page déclenche 10 appels AJAX, le Googlebot doit potentiellement les crawler tous.

**Bonnes pratiques** :
- Bloquer via `robots.txt` les endpoints AJAX qui ne contiennent pas de contenu indexable
- Utiliser `noindex` sur les réponses partielles si elles sont accessibles par URL directe

---

## Outils de débogage AJAX / SEO

| Outil | Usage |
|-------|-------|
| **Google Search Console** → Inspection d'URL | Voir le HTML rendu par Google |
| **Chrome DevTools → Network** | Surveiller les appels XHR/Fetch |
| **Fetch as Google (GSC)** | Comparer HTML source vs HTML rendu |
| **Screaming Frog** (mode JS) | Crawler avec rendu JavaScript |
| **Sitebulb** | Analyse rendu JS + détection contenu AJAX |

---

## Voir aussi

- [DOM et CSSOM](./DOM_et_CSSOM.md)
- [JSON Object](./JSON_object.md)
- [Crawl Budget](./Crawl_Budget.md)
- [Key Locations in SEO](./Key_Locations_SEO.md)
