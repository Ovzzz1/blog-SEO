# 3XX HTTP Response Codes

> **Catégorie** : HTTP / Redirections / SEO Technique  
> **Dernière mise à jour** : 2026

---

## Définition

Les codes de réponse HTTP **3XX** forment une classe de statuts indiquant que le client doit effectuer une action supplémentaire pour compléter la requête. Ils sont principalement utilisés pour les **redirections d'URL** et jouent un rôle fondamental en SEO : gestion du flux de trafic, préservation du link equity (PageRank), expérience utilisateur et signaux d'indexation envoyés aux moteurs de recherche.

Le serveur renvoie un code 3XX accompagné d'un header `Location` indiquant la nouvelle destination.

---

## Table des matières

1. [301 Moved Permanently](#301-moved-permanently)
2. [302 Found (Temporary Redirect)](#302-found-temporary-redirect)
3. [303 See Other](#303-see-other)
4. [304 Not Modified](#304-not-modified)
5. [307 Temporary Redirect](#307-temporary-redirect)
6. [308 Permanent Redirect](#308-permanent-redirect)
7. [Comparatif SEO des redirections](#comparatif-seo)
8. [Chaînes de redirections : risques et bonnes pratiques](#chaines-de-redirections)
9. [Erreurs courantes](#erreurs-courantes)

---

## 301 Moved Permanently

### Description
Un **301** indique qu'une ressource a été déplacée **définitivement** vers une nouvelle URL. C'est la redirection SEO la plus courante et la plus puissante.

Les moteurs de recherche mettent à jour leur index pour pointer vers la nouvelle URL et transfèrent la quasi-totalité du link equity (estimé à ~99% par Google depuis 2016).

### Cas d'usage
- Migration de domaine (ex : `http://` → `https://`)
- Changement permanent de structure d'URL
- Consolidation de contenu dupliqué
- Fusion de plusieurs pages en une seule

### Comportement des bots
- Google met généralement à jour son index en quelques jours à quelques semaines
- L'ancienne URL disparaît progressivement des SERPs
- Le Googlebot mémorise la redirection et réduit la fréquence de recrawl de l'ancienne URL

### Exemple
```http
HTTP/1.1 301 Moved Permanently
Location: https://www.example.com/nouvelle-page
```

---

## 302 Found (Temporary Redirect)

### Description
Un **302** indique que la ressource est **temporairement** disponible à une autre URL. Contrairement au 301, le moteur de recherche conserve l'URL d'origine dans son index.

> ⚠️ **Attention** : Le 302 ne transfère pas le link equity de façon fiable. Si une redirection doit être permanente, utilisez toujours un 301 (ou 308 pour les méthodes POST).

### Cas d'usage
- Redirection pendant une maintenance courte
- Test A/B (associé à des outils de split testing)
- Localisation temporaire (ex : redirection vers version locale pendant un event)

### Comportement des bots
- Google conserve l'URL source comme URL canonique
- En pratique, si un 302 reste en place trop longtemps, Google peut le traiter comme un 301 (comportement observé, non documenté officiellement)

### Exemple
```http
HTTP/1.1 302 Found
Location: https://www.example.com/maintenance
```

---

## 303 See Other

### Description
Le **303** est utilisé après un traitement de formulaire (méthode POST) pour rediriger le navigateur vers une page de confirmation via un GET. Il est au cœur du pattern **PRG (Post-Redirect-Get)**.

### Cas d'usage
- Soumission de formulaire → page de confirmation
- Prévention de la double soumission
- APIs REST : réponse après création de ressource

### Exemple
```http
HTTP/1.1 303 See Other
Location: /confirmation-commande
```

→ Voir aussi : [PRG (Post-Redirect-Get)](./PRG.md)

---

## 304 Not Modified

### Description
Le **304** n'est pas une redirection au sens strict : il indique au client que la ressource n'a **pas changé depuis la dernière requête** et que la version en cache est toujours valide. Aucune donnée n'est renvoyée dans le body.

### Mécanisme
Le client envoie un header conditionnel (`If-Modified-Since` ou `If-None-Match`) et le serveur répond 304 si la ressource est identique.

### Impact SEO / Performance
- Réduit la consommation de bande passante
- Améliore les temps de chargement
- Participe à l'optimisation du [Crawl Budget](./Crawl_Budget.md)

### Exemple
```http
GET /style.css HTTP/1.1
If-None-Match: "abc123"

HTTP/1.1 304 Not Modified
```

---

## 307 Temporary Redirect

### Description
Le **307** est la version stricte du 302 : il garantit que la **méthode HTTP** (GET, POST, PUT…) est **préservée** lors de la redirection. Là où un 302 peut transformer un POST en GET, le 307 maintient la méthode d'origine.

### Cas d'usage
- Redirection temporaire d'une requête POST sans changer la méthode
- APIs RESTful nécessitant la préservation du verbe HTTP
- Redirections HTTPS temporaires

### Exemple
```http
HTTP/1.1 307 Temporary Redirect
Location: https://api.example.com/v2/resource
```

---

## 308 Permanent Redirect

### Description
Le **308** est l'équivalent permanent du 307. Il redirige **définitivement** tout en **préservant la méthode HTTP**. C'est l'équivalent strict du 301 pour les requêtes POST/PUT.

### Cas d'usage
- Migration permanente d'endpoints API
- Changement de domaine pour des formulaires ou flux POST
- Environnements où la méthode HTTP doit être préservée à tout prix

### Support
Supporté par tous les navigateurs modernes et par Google (depuis 2016).

### Exemple
```http
HTTP/1.1 308 Permanent Redirect
Location: https://api.newdomain.com/endpoint
```

---

## Comparatif SEO des redirections {#comparatif-seo}

| Code | Type | Méthode préservée | Link Equity | Index mis à jour | Usage recommandé |
|------|------|:-----------------:|:-----------:|:----------------:|------------------|
| 301  | Permanent | Non (POST → GET) | ✅ Oui (~99%) | ✅ Oui | Migration URL permanente |
| 302  | Temporaire | Non (POST → GET) | ⚠️ Partiel | ❌ Non | Redirection courte durée |
| 303  | Temporaire | Non (toujours GET) | ❌ Non | ❌ Non | Post-Redirect-Get |
| 307  | Temporaire | ✅ Oui | ⚠️ Partiel | ❌ Non | Redirection temporaire API |
| 308  | Permanent | ✅ Oui | ✅ Oui | ✅ Oui | Migration API/POST permanente |

---

## Chaînes de redirections : risques et bonnes pratiques {#chaines-de-redirections}

Une **chaîne de redirections** (redirect chain) se produit lorsque plusieurs redirections se suivent avant d'atteindre la destination finale :

```
URL A → 301 → URL B → 301 → URL C → 200
```

### Risques
- **Dilution du link equity** : chaque saut supplémentaire peut réduire marginalement le PageRank transmis
- **Ralentissement** : chaque redirection ajoute un aller-retour réseau (latence HTTP)
- **Gaspillage de crawl budget** : les bots doivent suivre chaque saut
- Google recommande de limiter les chaînes à 3 redirections maximum

### Bonne pratique
Pointer directement vers l'URL finale :
```
URL A → 301 → URL C  ✅
```

### Boucles de redirections
Une boucle (`URL A → URL B → URL A`) provoque une erreur côté navigateur et empêche tout crawl. À surveiller systématiquement lors des audits techniques.

---

## Erreurs courantes {#erreurs-courantes}

| Erreur | Impact | Solution |
|--------|--------|----------|
| Utiliser un 302 à la place d'un 301 | Pas de transfert de link equity | Passer en 301 |
| Chaîne de redirections longue | Lenteur + dilution SEO | Aplatir en redirect direct |
| Rediriger vers une page 404 | Perte totale du link equity | Vérifier la destination |
| Boucle de redirection | Page inaccessible | Auditer avec Screaming Frog / Ahrefs |
| Rediriger toutes les 404 vers la home | Soft 404, pénalité Google | Résoudre les 404 ou utiliser un 410 |

---

## Outils de vérification

- **Screaming Frog** : audit des redirections en masse
- **Google Search Console** → Couverture : identifier les URLs redirigées mal gérées
- **Redirect Checker** (httpstatus.io) : vérification URL par URL
- **Ahrefs / Semrush** : détection des chaînes et boucles

---

## Voir aussi

- [4XX HTTP Response Codes](./4XX_HTTP_Response_Codes.md)
- [Crawl Budget](./Crawl_Budget.md)
- [PRG (Post-Redirect-Get)](./PRG.md)
- [Canonical](./Canonical.md)
- [503 + Retry-After](./503_Retry_After.md)
