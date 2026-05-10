# X-Robots-Tag

> **Catégorie** : SEO Technique / HTTP Headers / Indexation  
> **Dernière mise à jour** : 2026

---

## Définition

Le **X-Robots-Tag** est un **header HTTP** permettant de contrôler l'indexation d'une ressource par les moteurs de recherche, exactement comme la balise `<meta name="robots">` — mais avec un avantage majeur : il peut s'appliquer à **n'importe quel type de fichier** servi par un serveur web, qu'il s'agisse d'un PDF, d'une image, d'un fichier vidéo, d'un document Word, ou même d'une page HTML.

Là où la meta robots est limitée au `<head>` d'un document HTML, le X-Robots-Tag opère au niveau du protocole HTTP, avant même que le contenu du fichier soit analysé.

---

## Pourquoi X-Robots-Tag existe

### Le problème de la meta robots

La balise `<meta name="robots">` ne peut être placée que dans le `<head>` d'un fichier HTML. Pour les ressources non-HTML, il est impossible d'incorporer des directives d'indexation directement dans le fichier :

- Un PDF n'a pas de `<head>` HTML
- Une image JPG ne peut pas contenir de balise meta
- Un fichier CSV ou XLS n'a pas de structure HTML

Le X-Robots-Tag résout ce problème en permettant de délivrer les directives via le **header HTTP de réponse**, qui précède n'importe quel contenu.

---

## Syntaxe

### Header HTTP standard

```http
HTTP/1.1 200 OK
X-Robots-Tag: noindex
X-Robots-Tag: noindex, nofollow
X-Robots-Tag: max-snippet:150, max-image-preview:standard
```

### Cibler un bot spécifique

```http
X-Robots-Tag: googlebot: noindex
X-Robots-Tag: bingbot: noarchive
X-Robots-Tag: googlebot: noindex, nofollow
```

---

## Directives disponibles

Les mêmes directives que la meta robots sont supportées :

| Directive | Effet |
|-----------|-------|
| `noindex` | Exclut la ressource de l'index |
| `nofollow` | Ne pas suivre les liens dans la ressource |
| `noarchive` | Pas de version en cache |
| `nosnippet` | Pas d'extrait dans les SERPs |
| `noimageindex` | Pas d'indexation des images de la page |
| `max-snippet:[n]` | Limite l'extrait à n caractères |
| `max-image-preview:[none\|standard\|large]` | Taille de l'aperçu image |
| `max-video-preview:[n]` | Durée de l'aperçu vidéo en secondes |
| `unavailable_after:[date]` | Date d'expiration de l'indexation |
| `none` | Équivalent à `noindex, nofollow` |
| `all` | Comportement par défaut (index + follow) |

---

## Implémentation

### Apache (`.htaccess`)

**Pour tous les PDFs du site :**
```apache
<FilesMatch "\.pdf$">
  Header set X-Robots-Tag "noindex, noarchive"
</FilesMatch>
```

**Pour un répertoire entier :**
```apache
<Directory "/var/www/html/documents-prives/">
  Header set X-Robots-Tag "noindex, nofollow"
</Directory>
```

**Pour les images (pas d'indexation Google Images) :**
```apache
<FilesMatch "\.(jpg|jpeg|png|gif|webp|avif)$">
  Header set X-Robots-Tag "noimageindex"
</FilesMatch>
```

**Pour toutes les pages HTML d'un sous-répertoire staging :**
```apache
<Directory "/var/www/html/staging/">
  Header set X-Robots-Tag "noindex, nofollow"
</Directory>
```

### Nginx

```nginx
# Pour tous les PDFs
location ~* \.pdf$ {
  add_header X-Robots-Tag "noindex, noarchive" always;
}

# Pour les images
location ~* \.(jpg|jpeg|png|gif|webp|avif|svg)$ {
  add_header X-Robots-Tag "noimageindex" always;
}

# Pour un répertoire entier
location /documents-internes/ {
  add_header X-Robots-Tag "noindex, nofollow" always;
}

# Pour les fichiers de données
location ~* \.(csv|xls|xlsx|json)$ {
  add_header X-Robots-Tag "noindex" always;
}
```

### PHP

```php
<?php
// Appliquer noindex à une page PHP dynamiquement
if ($conditionNoIndex) {
    header('X-Robots-Tag: noindex, nofollow');
}

// Pour un fichier PDF servi dynamiquement
function servePDF($filename) {
    header('Content-Type: application/pdf');
    header('X-Robots-Tag: noindex, noarchive');
    header('Content-Disposition: inline; filename="' . $filename . '"');
    readfile($filename);
}
?>
```

### Node.js / Express

```javascript
const express = require('express');
const path = require('path');
const app = express();

// Middleware pour les fichiers PDF
app.use('/documents', (req, res, next) => {
  if (req.path.endsWith('.pdf')) {
    res.set('X-Robots-Tag', 'noindex, noarchive');
  }
  next();
});

// Middleware global pour l'environnement staging
if (process.env.NODE_ENV === 'staging') {
  app.use((req, res, next) => {
    res.set('X-Robots-Tag', 'noindex, nofollow');
    next();
  });
}

// Servir les fichiers statiques
app.use('/documents', express.static(path.join(__dirname, 'private-docs')));
```

### Python / Django

```python
# middleware.py
class XRobotsTagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Appliquer noindex en staging
        if settings.ENVIRONMENT == 'staging':
            response['X-Robots-Tag'] = 'noindex, nofollow'
        
        # Noindex pour les PDFs servis dynamiquement
        if request.path.endswith('.pdf'):
            response['X-Robots-Tag'] = 'noindex, noarchive'
            
        return response

# settings.py
MIDDLEWARE = [
    'myapp.middleware.XRobotsTagMiddleware',
    # ...
]
```

---

## Cas d'usage spécifiques

### Empêcher l'indexation des PDFs internes

Les PDFs techniques (bons de commande, fiches internes, contrats) ne doivent pas apparaître dans les résultats de recherche :

```apache
<FilesMatch "\.pdf$">
  Header set X-Robots-Tag "noindex, noarchive"
</FilesMatch>
```

### Contrôler Google Images

Pour éviter que les images d'un site e-commerce soient indexées dans Google Images indépendamment des pages produit :

```nginx
location ~* \.(jpg|jpeg|png|webp)$ {
  add_header X-Robots-Tag "noimageindex" always;
}
```

### Environnement de staging

Bloquer systématiquement l'indexation d'un environnement de recette/staging, même si Googlebot y accède :

```nginx
# Virtual host staging
server {
    server_name staging.exemple.com;
    
    location / {
        add_header X-Robots-Tag "noindex, nofollow" always;
        # reste de la config...
    }
}
```

### Contenu à durée limitée

```php
// Conférence en ligne disponible jusqu'au 31 décembre 2026
header('X-Robots-Tag: unavailable_after: Thu, 31 Dec 2026 23:59:59 GMT');
```

---

## X-Robots-Tag vs Meta Robots : quand utiliser quoi ?

| Critère | Meta Robots | X-Robots-Tag |
|---------|:-----------:|:------------:|
| Pages HTML | ✅ Idéal | ✅ Possible |
| PDFs | ❌ Impossible | ✅ Idéal |
| Images (JPG, PNG, WebP…) | ❌ Impossible | ✅ Idéal |
| Vidéos | ❌ Impossible | ✅ Idéal |
| Fichiers Office (XLS, DOCX) | ❌ Impossible | ✅ Idéal |
| Règles en masse par type de fichier | ❌ Page par page | ✅ Regex serveur |
| Environnement staging global | ❌ Laborieux | ✅ 1 règle serveur |
| CMS sans accès serveur | ✅ Accessible | ❌ Peut être bloqué |

**Règle pratique** :
- Fichiers non-HTML → **X-Robots-Tag**
- Pages HTML avec contrôle CMS → **meta robots**
- Les deux peuvent coexister sur une page HTML (la directive la plus restrictive s'applique)

---

## Vérification

### Via curl
```bash
# Vérifier les headers d'un PDF
curl -I https://exemple.com/document.pdf | grep -i "x-robots"

# Vérifier une image
curl -I https://exemple.com/image.jpg | grep -i "x-robots"

# Sortie attendue :
# x-robots-tag: noindex, noarchive
```

### Via Chrome DevTools
1. Ouvrir DevTools → Onglet **Network**
2. Cliquer sur la ressource concernée
3. Vérifier les **Response Headers** → `x-robots-tag`

### Google Search Console
- **Inspection d'URL** → Affiche les directives lues par Google (pour les pages HTML)
- Pour les PDFs : utiliser l'outil d'inspection sur l'URL du PDF

---

## Voir aussi

- [Robots Meta Tag](./Robots_Meta_Tag.md)
- [Robots.txt](./Robots_txt.md)
- [Crawl Budget](./Crawl_Budget.md)
- [4XX HTTP Response Codes](./4XX_HTTP_Response_Codes.md)
- [Key Locations SEO](./Key_Locations_SEO.md)
