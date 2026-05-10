# 4XX HTTP Response Codes

> **Catégorie** : HTTP / Erreurs Client / SEO Technique  
> **Dernière mise à jour** : 2026

---

## Définition

Les codes de réponse HTTP **4XX** indiquent des **erreurs côté client** : la requête envoyée par le navigateur (ou le bot) est invalide, non autorisée, ou pointe vers une ressource inexistante ou inaccessible. Contrairement aux erreurs 5XX (serveur), la responsabilité incombe ici à la requête elle-même.

En SEO, les erreurs 4XX ont un impact direct sur :
- **L'indexation** : les pages en 404/410 sont délistées par Google
- **Le link equity** : les liens pointant vers des pages 4XX ne transmettent plus de PageRank
- **Le crawl budget** : les bots qui tombent sur des 4XX gaspillent du budget de crawl
- **L'expérience utilisateur** : pages mortes, accès refusés, formulaires mal construits

---

## Les 10 codes 4XX essentiels

### 400 Bad Request

**Description** : Le serveur ne peut pas comprendre la requête en raison d'une **syntaxe invalide** (paramètres malformés, headers incorrects, corps de requête corrompu).

**Impact SEO** : Faible si isolé. Peut indiquer des problèmes de paramètres d'URL à surveiller dans GSC.

**Causes fréquentes** :
- URL avec caractères non encodés
- Payload JSON malformé dans une API
- Headers HTTP corrompus

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{"error": "Invalid query parameter: 'sort' must be 'asc' or 'desc'"}
```

---

### 401 Unauthorized

**Description** : La ressource requiert une **authentification** qui n'a pas été fournie ou est invalide. Ne signifie pas "vous n'avez pas la permission" (c'est le 403), mais "identifiez-vous d'abord".

**Impact SEO** : Les pages en 401 ne sont pas indexées par Google. Utile pour les espaces membres.

**Mécanisme** : Le serveur doit renvoyer un header `WWW-Authenticate` précisant le schéma d'auth requis (Basic, Bearer, Digest…).

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="API"
```

---

### 403 Forbidden

**Description** : Le serveur comprend la requête mais **refuse de l'exécuter**, même si le client est authentifié. C'est une décision d'autorisation, pas d'authentification.

**Impact SEO** : Google déindexe les pages en 403 permanentes. À surveiller sur des ressources qui devraient être publiques (CSS, JS, images).

**Cas d'usage légitimes** :
- Répertoires système (ex : `/wp-admin/`)
- Ressources privées (espace client)
- Protection géographique (geo-blocking)

```http
HTTP/1.1 403 Forbidden
```

---

### 404 Not Found

**Description** : La ressource demandée est **introuvable** sur le serveur. C'est le code d'erreur le plus connu du web.

**Impact SEO** :
- Google déindexe les pages en 404 persistantes (après plusieurs recrawls confirmant le statut)
- Les backlinks pointant vers une 404 ne transmettent plus de PageRank → à corriger via des 301
- Les 404 "douces" (soft 404 : page qui renvoie 200 mais affiche un message "page introuvable") sont particulièrement pénalisantes

**Bonnes pratiques** :
- Créer une page 404 personnalisée avec navigation et moteur de recherche interne
- Monitorer les 404 via Google Search Console → Couverture
- Rediriger (301) les URLs qui ont des backlinks vers leur équivalent le plus proche

```http
HTTP/1.1 404 Not Found
```

---

### 405 Method Not Allowed

**Description** : La méthode HTTP utilisée (GET, POST, PUT, DELETE…) **n'est pas supportée** pour cette ressource.

**Cas d'usage** : Tentative de POST sur une URL qui n'accepte que GET, ou DELETE sur une ressource en lecture seule.

```http
HTTP/1.1 405 Method Not Allowed
Allow: GET, HEAD
```

---

### 406 Not Acceptable

**Description** : Le serveur ne peut pas générer de réponse correspondant aux critères **Accept** de la requête (type MIME, langue, encodage).

**Exemple** : Le client demande `Accept: application/xml` mais le serveur ne sert que du JSON.

---

### 407 Proxy Authentication Required

**Description** : Similaire au 401 mais pour un **proxy** intermédiaire. L'authentification doit se faire auprès du proxy, pas du serveur final.

**Contexte** : Courant dans les environnements d'entreprise avec proxy réseau.

---

### 408 Request Timeout

**Description** : Le serveur a attendu trop longtemps la requête du client et ferme la connexion. Souvent lié à des problèmes réseau côté client.

---

### 409 Conflict

**Description** : La requête ne peut pas être complétée en raison d'un **conflit avec l'état actuel** de la ressource. Typique des APIs REST lors de conflits de versions.

**Exemples** :
- Tentative de créer une ressource qui existe déjà
- Conflit lors d'une mise à jour concurrente (ETag mismatch)

---

### 410 Gone

**Description** : La ressource a été **supprimée définitivement** et ne reviendra plus. Contrairement au 404 (la page pourrait revenir), le 410 est un signal fort de suppression intentionnelle.

**Impact SEO** : Google retire la page de son index plus rapidement qu'un 404. À utiliser pour les pages volontairement supprimées (anciennes promos, produits discontinués, articles retirés).

**Quand préférer 410 à 404** :
- Page supprimée délibérément et définitivement
- Page de spam ou de contenu de mauvaise qualité retirée
- Contenu expiré (offre d'emploi, event passé)

```http
HTTP/1.1 410 Gone
```

---

## Tableau comparatif

| Code | Nom | Responsabilité | Impact SEO | Action recommandée |
|------|-----|:--------------:|:----------:|-------------------|
| 400  | Bad Request | Requête malformée | Faible | Corriger les paramètres URL |
| 401  | Unauthorized | Auth manquante | Neutre (zone privée) | Normal si zone protégée |
| 403  | Forbidden | Accès refusé | Neutre/négatif | Vérifier les ressources publiques |
| 404  | Not Found | Page absente | ⚠️ Négatif | Rediriger (301) ou recréer |
| 405  | Method Not Allowed | Mauvaise méthode | Faible | Corriger les formulaires/APIs |
| 408  | Request Timeout | Timeout réseau | Faible | Optimiser perfs serveur |
| 410  | Gone | Suppression définitive | Neutre (signal propre) | Utiliser pour suppressions intentionnelles |

---

## Soft 404 : le piège SEO

Un **soft 404** est une page qui retourne un code HTTP 200 (succès) mais qui affiche un contenu de type "page introuvable". Google détecte ce comportement et peut le traiter comme une vraie 404 ou comme du **contenu mince (thin content)**, ce qui est pénalisant.

**Causes fréquentes** :
- CMS qui redirige les 404 vers la homepage avec un 200
- Pages produit "rupture de stock" vides
- Pages de résultats de recherche interne vides

**Détection** : Google Search Console → section "Couverture" → "Exclues" → "Soft 404"

**Solution** : Renvoyer un vrai code 404 ou 410, ou mettre à jour le contenu de la page.

---

## Monitoring et outils

| Outil | Usage |
|-------|-------|
| **Google Search Console** | Rapport Couverture, erreurs 404 découvertes par Googlebot |
| **Screaming Frog** | Crawl complet pour détecter les 4XX internes et externes |
| **Ahrefs / Semrush** | Backlinks pointant vers des 4XX |
| **Logs serveur** | Identifier les 404/403 réels avec volume et source |
| **Sentry / Datadog** | Monitoring en temps réel des erreurs HTTP |

---

## Voir aussi

- [3XX HTTP Response Codes](./3XX_HTTP_Response_Codes.md)
- [503 + Retry-After](./503_Retry_After.md)
- [Crawl Budget](./Crawl_Budget.md)
- [Robots.txt](./Robots_txt.md)
- [XML Sitemap](./XML_Sitemap.md)
