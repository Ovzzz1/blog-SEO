# 503 Service Unavailable + Header "Retry-After"

> **Catégorie** : HTTP / SEO Technique / Maintenance  
> **Dernière mise à jour** : 2026

---

## Définition

Le code HTTP **503 Service Unavailable** indique que le serveur est temporairement **incapable de traiter la requête**, généralement en raison d'une surcharge ou d'une maintenance planifiée. Contrairement aux erreurs 4XX (faute du client), le 503 est une erreur côté serveur (5XX) avec une particularité cruciale : il est **temporaire par nature**.

Pour les moteurs de recherche, le 503 est le signal correct à envoyer pendant une maintenance planifiée. Accompagné du header `Retry-After`, il indique explicitement quand le service reprendra, évitant ainsi la déindexation des pages.

---

## Pourquoi le 503 est crucial pour le SEO en maintenance

| Code utilisé | Comportement de Google |
|:---:|---|
| **200** (page de maintenance) | Indexe la page de maintenance → **catastrophique** |
| **301/302** vers page de maintenance | Peut indexer la page de maint., perd le link equity |
| **404** pendant maintenance | Commence à déindexer après quelques recrawls |
| **503 + Retry-After** | ✅ Revient à la date indiquée, ne déindexe pas |

---

## Le Header `Retry-After`

### Syntaxe

Le header `Retry-After` indique au client (navigateur ou bot) quand réessayer. Il accepte deux formats :

**Format délai (secondes)** :
```http
HTTP/1.1 503 Service Unavailable
Retry-After: 3600
```
→ Réessayer dans 3600 secondes (1 heure)

**Format date HTTP** :
```http
HTTP/1.1 503 Service Unavailable
Retry-After: Sat, 10 May 2026 14:00:00 GMT
```
→ Réessayer après cette date/heure précise

### Comportement de Googlebot face au 503

- Googlebot lit le header `Retry-After` et programme son prochain passage à la date indiquée
- Sans `Retry-After`, Googlebot réessaie selon son propre algorithme (généralement quelques heures)
- Si le 503 persiste pendant **plusieurs jours sans Retry-After**, Google commence à réduire la fréquence de crawl et éventuellement à signaler des erreurs dans GSC
- Une maintenance de moins de 24h avec `Retry-After` correct **n'entraîne aucune pénalité SEO**

---

## Implémentation sur WordPress

### Étape 1 : Créer la page de maintenance

Dans le tableau de bord WordPress :
1. Créer une nouvelle page "Maintenance en cours"
2. Y insérer le message de maintenance et les informations de contact/retour
3. Publier et noter l'URL (ex : `/maintenance/`)

### Étape 2 : Configurer `.htaccess` (Apache)

```apache
RewriteEngine On
RewriteBase /

# Exclure votre IP de la maintenance (remplacer par votre IP)
RewriteCond %{REMOTE_ADDR} !^123\.456\.789\.000$

# Exclure la page de maintenance elle-même (éviter boucle infinie)
RewriteCond %{REQUEST_URI} !/maintenance/$

# Exclure les ressources statiques
RewriteCond %{REQUEST_URI} !\.(css|js|png|jpg|gif|ico|woff|woff2)$

# Rediriger tout vers la page de maintenance avec 503
RewriteRule .* /maintenance/ [R=503,L]

# Header Retry-After (maintenance de 2 heures)
Header always set Retry-After "7200"
```

### Étape 3 : S'assurer que la page de maintenance renvoie bien 503

```php
// À ajouter dans le template de la page de maintenance (page.php ou template custom)
<?php
if (is_page('maintenance')) {
    header('HTTP/1.1 503 Service Unavailable');
    header('Retry-After: 7200'); // 2 heures
    header('Status: 503 Service Unavailable');
}
?>
```

---

## Implémentation sur Nginx

```nginx
# nginx.conf ou virtual host

# Variable pour activer/désactiver la maintenance
# Créer un fichier /var/www/html/maintenance.flag pour activer
location / {
    if (-f /var/www/html/maintenance.flag) {
        return 503;
    }
    # Configuration normale...
}

# Page d'erreur 503 personnalisée
error_page 503 /503.html;

location = /503.html {
    root /var/www/html;
    internal;
    add_header Retry-After 3600 always;
}
```

---

## Implémentation en PHP pur

```php
<?php
// maintenance.php

// Activer la maintenance (peut être conditionné à un fichier flag)
$maintenanceMode = true;
$retryAfterSeconds = 3600; // 1 heure
$maintenanceEndTime = 'Sat, 10 May 2026 18:00:00 GMT'; // optionnel

if ($maintenanceMode) {
    header('HTTP/1.1 503 Service Unavailable');
    header('Retry-After: ' . $retryAfterSeconds);
    header('Content-Type: text/html; charset=UTF-8');
    
    // Afficher la page de maintenance
    include 'maintenance-template.html';
    exit();
}
?>
```

---

## Implémentation en Node.js / Express

```javascript
const express = require('express');
const app = express();

const MAINTENANCE_MODE = process.env.MAINTENANCE_MODE === 'true';
const RETRY_AFTER = 3600; // secondes

app.use((req, res, next) => {
  if (MAINTENANCE_MODE) {
    return res.status(503)
      .set('Retry-After', String(RETRY_AFTER))
      .send(`
        <!DOCTYPE html>
        <html>
          <head><title>Maintenance en cours</title></head>
          <body>
            <h1>Site en maintenance</h1>
            <p>Nous serons de retour dans environ ${RETRY_AFTER / 60} minutes.</p>
          </body>
        </html>
      `);
  }
  next();
});
```

---

## Vérification du bon fonctionnement

```bash
# Vérifier le code HTTP et le header Retry-After
curl -I https://votre-site.com/

# Réponse attendue :
# HTTP/1.1 503 Service Unavailable
# Retry-After: 3600
# Content-Type: text/html; charset=UTF-8
```

---

## Checklist maintenance SEO-safe

- [ ] Le code HTTP retourné est bien **503** (pas 200, 302 ou 404)
- [ ] Le header **`Retry-After`** est présent et indique une durée réaliste
- [ ] La page de maintenance elle-même retourne 503 (pas 200)
- [ ] Les **ressources statiques** (CSS, images) sont toujours accessibles pour un rendu correct
- [ ] **Votre IP** est exclue du mode maintenance pour vérifier le site
- [ ] **Googlebot** n'est pas spécifiquement bloqué (le 503 + Retry-After est le bon signal)
- [ ] La maintenance est la **plus courte possible** (idéalement < 1h, max 24h pour le SEO)
- [ ] GSC est surveillé après le retour pour détecter des erreurs résiduelles

---

## Différence 503 vs autres codes de maintenance

| Scénario | Code recommandé | Raison |
|----------|:--------------:|--------|
| Maintenance planifiée courte | **503 + Retry-After** | Temporaire, pas de déindexation |
| Site en construction (avant lancement) | **503** ou page Coming Soon avec `noindex` | Éviter l'indexation du placeholder |
| Page supprimée définitivement | **410** | Signal de suppression permanente |
| URL déplacée | **301** | Redirection permanente |
| Erreur serveur non planifiée | **500** ou **503** | Selon le cas |

---

## Voir aussi

- [3XX HTTP Response Codes](./3XX_HTTP_Response_Codes.md)
- [4XX HTTP Response Codes](./4XX_HTTP_Response_Codes.md)
- [Crawl Budget](./Crawl_Budget.md)
- [Robots Meta Tag](./Robots_Meta_Tag.md)
