# Hreflang

> **Catégorie** : SEO International / Multilinguisme / Indexation  
> **Dernière mise à jour** : 2026

---

## Définition

**Hreflang** est un attribut HTML introduit par Google en 2011 pour signaler aux moteurs de recherche la langue et, optionnellement, la zone géographique ciblée par une page web. Il permet de servir la bonne version linguistique d'une page à l'utilisateur selon sa langue et sa localisation, évitant ainsi des problèmes de contenu dupliqué international et améliorant la pertinence des résultats de recherche.

> Hreflang est utilisé par **Google** et **Yandex**. Bing utilise une approche différente basée sur le header `Content-Language` et les balises meta.

---

## Syntaxe de base

```html
<link rel="alternate" hreflang="[code-langue]" href="[URL]">
<!-- ou avec région -->
<link rel="alternate" hreflang="[code-langue]-[code-pays]" href="[URL]">
```

### Codes de langue (ISO 639-1)
| Code | Langue |
|------|--------|
| `fr` | Français (toutes régions) |
| `en` | Anglais (toutes régions) |
| `es` | Espagnol |
| `de` | Allemand |
| `zh` | Chinois |
| `ar` | Arabe |
| `pt` | Portugais |

### Codes de pays (ISO 3166-1 alpha-2)
| Code | Pays |
|------|------|
| `FR` | France |
| `BE` | Belgique |
| `CA` | Canada |
| `US` | États-Unis |
| `GB` | Royaume-Uni |
| `CH` | Suisse |

### Combinaisons langue-pays courantes
```
fr-FR  → Français pour la France
fr-BE  → Français pour la Belgique
fr-CA  → Français pour le Canada
fr-CH  → Français pour la Suisse
en-US  → Anglais américain
en-GB  → Anglais britannique
pt-BR  → Portugais brésilien
pt-PT  → Portugais européen
zh-Hans → Chinois simplifié
zh-Hant → Chinois traditionnel
```

---

## Implémentation

### Méthode 1 : Balises `<link>` dans le `<head>` (recommandée)

```html
<!-- Page française (france) -->
<head>
  <link rel="alternate" hreflang="fr-FR" href="https://exemple.com/fr-fr/article">
  <link rel="alternate" hreflang="fr-BE" href="https://exemple.com/fr-be/article">
  <link rel="alternate" hreflang="en-US" href="https://exemple.com/en-us/article">
  <link rel="alternate" hreflang="en-GB" href="https://exemple.com/en-gb/article">
  <link rel="alternate" hreflang="x-default" href="https://exemple.com/article">
  <!-- Auto-référencement obligatoire -->
  <link rel="canonical" href="https://exemple.com/fr-fr/article">
</head>
```

> ⚠️ **Chaque page doit se référencer elle-même** dans le groupe hreflang.

### Méthode 2 : Sitemap XML (recommandée pour les grands sites)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://exemple.com/fr-fr/article</loc>
    <xhtml:link rel="alternate" hreflang="fr-FR" href="https://exemple.com/fr-fr/article"/>
    <xhtml:link rel="alternate" hreflang="fr-BE" href="https://exemple.com/fr-be/article"/>
    <xhtml:link rel="alternate" hreflang="en-US" href="https://exemple.com/en-us/article"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://exemple.com/article"/>
  </url>
  <!-- Répéter pour chaque URL du groupe -->
</urlset>
```

### Méthode 3 : Header HTTP (pour ressources non-HTML)

```http
Link: <https://exemple.com/fr-fr/document.pdf>; rel="alternate"; hreflang="fr-FR",
      <https://exemple.com/en-us/document.pdf>; rel="alternate"; hreflang="en-US"
```

---

## Le tag `x-default`

Le tag **`x-default`** est l'URL de fallback présentée aux utilisateurs dont la langue ne correspond à aucune version disponible. Il est fortement recommandé.

```html
<link rel="alternate" hreflang="x-default" href="https://exemple.com/en/article">
```

**Usage courants de `x-default`** :
- Page de sélection de pays/langue
- Version anglaise internationale par défaut
- Page d'accueil internationale

---

## Structures d'URL pour l'international

| Structure | Exemple | Avantages | Inconvénients |
|-----------|---------|-----------|---------------|
| **ccTLD** | `.fr`, `.de`, `.es` | Signal géo fort | Coût, maintenance multiple |
| **Sous-domaine** | `fr.exemple.com` | Séparation technique | Dilution de l'autorité |
| **Sous-répertoire** | `exemple.com/fr/` | Autorité centralisée | Moins fort en signal géo |
| **Paramètre** | `exemple.com?lang=fr` | Simple à implémenter | ❌ Mauvaise pratique SEO |

**Recommandation 2026** : Les **sous-répertoires** (`/fr/`, `/en/`, `/de/`) offrent le meilleur équilibre entre signal géographique, autorité centralisée et facilité de maintenance pour la plupart des sites.

---

## Règles et contraintes obligatoires

### 1. Réciprocité (règle critique)
Chaque version doit référencer **toutes les autres versions**, y compris elle-même. Si la page FR pointe vers EN mais que EN ne pointe pas vers FR, Google peut ignorer le signal.

```
FR → EN ✅
EN → FR ✅ (obligatoire)
```

### 2. URLs absolues uniquement
```html
<!-- ❌ INCORRECT -->
<link rel="alternate" hreflang="fr" href="/fr/article">

<!-- ✅ CORRECT -->
<link rel="alternate" hreflang="fr" href="https://exemple.com/fr/article">
```

### 3. Les URLs doivent être indexables
Une URL hreflang en `noindex` ou bloquée par `robots.txt` provoque des erreurs dans GSC.

### 4. Cohérence avec le canonical
Chaque URL hreflang doit avoir son propre `rel="canonical"` pointant vers elle-même (ou la version canonique de sa langue).

### 5. Contenu réellement différent
Hreflang ne résout pas le contenu dupliqué entre deux versions quasi-identiques (ex : EN-US et EN-GB avec seulement quelques mots différents). Google peut détecter et ignorer des variations trop légères.

---

## Erreurs courantes et leurs conséquences

| Erreur | Conséquence | Solution |
|--------|------------|----------|
| Pas de réciprocité | Google ignore le signal | Vérifier les deux sens |
| URL relative au lieu d'absolue | Signal invalide | Toujours utiliser des URLs absolues |
| Codes de langue incorrects | Non reconnu par Google | Utiliser ISO 639-1 strictement |
| Hreflang vers une page 404 | Erreur GSC | Corriger ou retirer l'URL |
| Pas de x-default | Comportement imprévisible pour autres régions | Ajouter x-default |
| Hreflang et canonical contradictoires | Signaux confus | Aligner canonical et hreflang |
| Pages trop similaires | Ignoré par Google | S'assurer d'une vraie localisation |

---

## Hreflang et les moteurs IA (2025-2026)

L'émergence des **AI Overviews** (Google SGE) et des moteurs de recherche IA (Perplexity, Bing Copilot) pose de nouvelles questions sur la gestion de l'international :

- Les réponses IA peuvent agréger du contenu multilingue sans respect strict des hreflang
- La géolocalisation des réponses IA reste moins précise que les SERPs classiques
- **Recommandation** : Maintenir les hreflang pour les SERPs classiques + s'assurer que la langue est clairement signalée dans le contenu (`lang` attribute sur `<html>`)

---

## Monitoring et audit

### Google Search Console
- **Rapport International** : Affiche les erreurs hreflang détectées (réciprocité manquante, URLs invalides, etc.)
- Navigation : GSC → Index → Règles d'internationalisation

### Screaming Frog
- Export de tous les tags hreflang
- Vérification des URLs de destination (200 vs 404)
- Détection des manques de réciprocité

### Hreftang.com / Merkle Hreflang Testing Tool
Outils en ligne pour valider les annotations hreflang d'une page.

### Commande manuelle
```bash
# Vérifier les hreflang d'une page
curl -s https://exemple.com/fr/page | grep -i 'hreflang'
```

---

## Voir aussi

- [Canonical](./Canonical.md)
- [XML Sitemap](./XML_Sitemap.md)
- [CDN](./CDN.md)
- [Robots Meta Tag](./Robots_Meta_Tag.md)
