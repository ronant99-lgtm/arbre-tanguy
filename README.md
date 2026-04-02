# Arbre généalogique — Famille Tanguy

Arbre interactif des ascendants de Jean Gustave Marie Tanguy, hébergé sur GitHub Pages.

## 🌐 Accès

**URL publique :** `https://ronant99-lgtm.github.io/arbre-tanguy`

---

## 📁 Structure du dépôt

```
arbre-tanguy/
├── index.html          ← l'arbre interactif (ne pas modifier)
├── data.json           ← les données de la famille (à éditer)
├── photos/             ← les portraits et images
│   ├── exemple.jpg
│   └── ...
└── README.md           ← ce fichier
```

---

## ✏️ Modifier une fiche (biographie, dates, profession…)

1. Ouvrir l'arbre sur `https://ronant99-lgtm.github.io/arbre-tanguy`
2. Cliquer sur un ancêtre → **✎ Modifier**
3. Remplir les champs, cliquer **Enregistrer**
4. Répéter pour d'autres fiches si besoin
5. Cliquer **⬇ Exporter JSON** → télécharge `data_tanguy.json`
6. Renommer ce fichier en `data.json`
7. Le déposer dans ce dépôt GitHub (remplace l'ancien)
8. Attendre ~30 secondes → l'arbre est mis à jour pour tout le monde

---

## 🖼️ Ajouter une photo

### Option A — URL externe (la plus simple)

Héberger la photo sur n'importe quel service (Google Photos, Imgur, etc.)
et coller le lien direct dans le champ **Photo** de l'éditeur.

Exemple : `https://i.imgur.com/abc123.jpg`

### Option B — Photo dans le dépôt (recommandé pour la pérennité)

1. Préparer la photo : format JPG ou PNG, idéalement **400×500 px**, moins de **300 Ko**
2. La nommer de façon claire : `jean_tanguy_1875.jpg`
3. La déposer dans le dossier `photos/` de ce dépôt
4. Dans l'éditeur, renseigner le chemin : `photos/jean_tanguy_1875.jpg`
5. Exporter et redéposer `data.json` comme décrit ci-dessus

> **Conseil qualité photo :** une image en noir et blanc avec un léger traitement sépia
> s'intègre particulièrement bien dans l'interface.

---

## 🔄 Ajouter ou modifier des ancêtres (avancé)

Le fichier `data.json` peut aussi être édité directement dans un éditeur de texte
(VS Code, Notepad++…). La structure est la suivante :

```json
{
  "id": "identifiant-unique",
  "given": "Jean Gustave Marie",
  "surname": "TANGUY",
  "born": 1946,
  "died": 1985,
  "gender": "M",
  "lieu_naissance": "Kerpert",
  "lieu_deces": "Nantes",
  "profession": "Cultivateur",
  "photo": "photos/jean_tanguy.jpg",
  "bio": "<p>Texte biographique libre.</p>",
  "children": [ ... ]
}
```

Les `children` sont les **ancêtres directs** (père et mère), pas les descendants.

---

## 🚀 Mise en place initiale (une seule fois)

### 1. Créer le dépôt GitHub

- Aller sur [github.com/new](https://github.com/new)
- Nom du dépôt : `arbre-tanguy`
- Cocher **Public** (obligatoire pour GitHub Pages gratuit)
- Cliquer **Create repository**

### 2. Déposer les fichiers

Depuis la page du dépôt, cliquer **uploading an existing file** et déposer :
- `index.html`
- `data.json`
- Le dossier `photos/` (avec ses fichiers)

### 3. Activer GitHub Pages

- Aller dans **Settings** → **Pages**
- Source : **Deploy from a branch**
- Branch : **main**, dossier **/ (root)**
- Cliquer **Save**
- L'URL apparaît en haut de la page en quelques minutes

### 4. Partager

Envoyer l'URL `https://ronant99-lgtm.github.io/arbre-tanguy` à la famille.

---

## 👥 Contribuer en famille

Chacun peut proposer des corrections ou ajouts en envoyant un email avec :
- Le nom de l'ancêtre concerné
- La modification souhaitée
- Une photo éventuelle (en pièce jointe)

La personne qui gère le dépôt intègre les modifications via l'éditeur.
