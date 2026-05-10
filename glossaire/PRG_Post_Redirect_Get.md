# PRG (Post-Redirect-Get)

> **Catégorie** : Développement Web / Patterns HTTP / UX  
> **Dernière mise à jour** : 2026

---

## Définition

Le **PRG (Post-Redirect-Get)** est un design pattern web qui résout le problème de la **double soumission de formulaire**. Il repose sur trois étapes HTTP successives :

1. **POST** : L'utilisateur soumet un formulaire → Le serveur traite les données
2. **Redirect** : Le serveur renvoie une réponse de redirection (303 ou 302) vers une nouvelle URL
3. **GET** : Le navigateur suit la redirection et charge la page de confirmation via GET

Sans ce pattern, un rafraîchissement (F5) ou un retour arrière sur la page de confirmation provoquerait une re-soumission du formulaire original.

---

## Le problème que PRG résout

### Scénario sans PRG

```
1. Utilisateur remplit formulaire de commande
2. Clic "Commander"
   → POST /checkout → Traitement commande → Réponse 200 "Merci!"
3. L'URL du navigateur est toujours /checkout
4. Utilisateur appuie sur F5 (refresh)
   → Le navigateur propose "Renvoyer les données de formulaire ?"
   → Si l'utilisateur confirme : DOUBLE COMMANDE 🚨
```

### Même scénario avec PRG

```
1. Utilisateur remplit formulaire de commande
2. Clic "Commander"
   → POST /checkout → Traitement commande → Réponse 303 → /confirmation?id=12345
3. Navigateur suit la redirection → GET /confirmation?id=12345 → 200 "Merci!"
4. L'URL du navigateur est maintenant /confirmation?id=12345
5. Utilisateur appuie sur F5
   → GET /confirmation?id=12345 → Affiche la confirmation sans re-soumettre ✅
```

---

## Flux HTTP détaillé

```http
POST /checkout HTTP/1.1
Host: shop.exemple.com
Content-Type: application/x-www-form-urlencoded

product_id=42&quantity=2&payment_token=tok_abc123
```

```http
HTTP/1.1 303 See Other
Location: /confirmation?order=ORD-78542
```

```http
GET /confirmation?order=ORD-78542 HTTP/1.1
Host: shop.exemple.com
```

```http
HTTP/1.1 200 OK
Content-Type: text/html

<html>...Votre commande ORD-78542 a été confirmée !...</html>
```

---

## Quel code de redirection utiliser ?

| Code | Usage recommandé avec PRG | Méthode résultante |
|:----:|---------------------------|:-----------------:|
| **303** | ✅ Standard PRG — la méthode **devient toujours GET** | GET |
| **302** | ✅ Acceptable en pratique (même comportement dans les navigateurs modernes) | GET (dans les faits) |
| **307** | ❌ Préserve la méthode POST → re-soumission du formulaire ! | POST (conservé) |
| **301** | ⚠️ Possible mais non recommandé (cache permanent de la redirection) | GET |

**Recommandation** : Utiliser **303 See Other** est la pratique la plus sémantiquement correcte selon la RFC 9110 (HTTP Semantics, 2022).

---

## Implémentations par langage/framework

### PHP
```php
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Traitement du formulaire
    $orderId = processOrder($_POST);
    
    // PRG : redirection après traitement
    header('HTTP/1.1 303 See Other');
    header('Location: /confirmation.php?order=' . urlencode($orderId));
    exit();
}
?>
```

### Node.js / Express
```javascript
const express = require('express');
const app = express();
app.use(express.urlencoded({ extended: true }));

app.post('/checkout', async (req, res) => {
  try {
    const order = await processOrder(req.body);
    // PRG
    res.redirect(303, `/confirmation?order=${order.id}`);
  } catch (error) {
    res.status(400).render('error', { message: error.message });
  }
});

app.get('/confirmation', (req, res) => {
  const order = getOrder(req.query.order);
  res.render('confirmation', { order });
});
```

### Python / Django
```python
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def checkout(request):
    order = process_order(request.POST)
    # PRG
    return redirect('confirmation', order_id=order.id)  # HTTP 302 par défaut

def confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'confirmation.html', {'order': order})
```

### Ruby on Rails
```ruby
class OrdersController < ApplicationController
  def create
    @order = Order.new(order_params)
    if @order.save
      # PRG : redirect_to génère un 302 par défaut
      redirect_to confirmation_order_path(@order), status: :see_other
    else
      render :new, status: :unprocessable_entity
    end
  end
  
  def confirmation
    @order = Order.find(params[:id])
  end
end
```

### PHP avec sessions Flash (messages post-redirect)

Un défi du PRG est que les données POST disparaissent après la redirection. La solution classique est le **flash message** via session :

```php
<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $orderId = processOrder($_POST);
    
    // Stocker le message en session (flash)
    $_SESSION['flash'] = [
        'type' => 'success',
        'message' => "Commande #{$orderId} confirmée !"
    ];
    
    header('HTTP/1.1 303 See Other');
    header('Location: /confirmation');
    exit();
}

// Page confirmation (GET)
$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']); // Consommer le flash
?>
```

---

## PRG et les APIs REST

Dans les APIs REST modernes, PRG s'applique différemment. Après un POST créant une ressource, la réponse standard est `201 Created` avec un header `Location` pointant vers la nouvelle ressource :

```http
POST /api/articles HTTP/1.1
Content-Type: application/json

{"title": "Mon article", "content": "..."}
```

```http
HTTP/1.1 201 Created
Location: /api/articles/123
Content-Type: application/json

{"id": 123, "title": "Mon article", ...}
```

Ce n'est pas strictement du PRG (pas de redirection automatique côté client), mais le principe de séparer l'action du résultat est similaire.

---

## PRG et les SPAs / JavaScript moderne

Dans les **Single Page Applications** (React, Vue, Angular), le PRG traditionnel est souvent remplacé par une gestion côté JavaScript :

```javascript
async function handleSubmit(formData) {
  try {
    const order = await fetch('/api/checkout', {
      method: 'POST',
      body: JSON.stringify(formData)
    }).then(r => r.json());
    
    // Équivalent PRG via routing côté client
    router.push(`/confirmation/${order.id}`);
    
  } catch (error) {
    setError(error.message);
  }
}
```

**Attention** : Dans ce cas, le problème de double soumission est géré par le state management de l'application (désactiver le bouton après clic, gérer l'idempotence côté API).

---

## Bonnes pratiques complémentaires

### Idempotence côté serveur
Même avec PRG, il est prudent de rendre le traitement du POST **idempotent** via des tokens anti-replay :

```php
<?php
// Générer un token unique dans le formulaire
$_SESSION['form_token'] = bin2hex(random_bytes(32));
?>
<input type="hidden" name="form_token" value="<?= $_SESSION['form_token'] ?>">

<?php
// Côté traitement
if ($_POST['form_token'] !== $_SESSION['form_token']) {
    http_response_code(409); // Conflict
    die('Formulaire déjà soumis');
}
unset($_SESSION['form_token']);
// Traiter la commande...
?>
```

---

## Voir aussi

- [3XX HTTP Response Codes](./3XX_HTTP_Response_Codes.md)
- [4XX HTTP Response Codes](./4XX_HTTP_Response_Codes.md)
- [AJAX](./AJAX.md)
- [Key Locations SEO](./Key_Locations_SEO.md)
