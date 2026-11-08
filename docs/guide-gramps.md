# Guide Gramps — arbre de la famille Tanguy

Ce guide explique comment utiliser **Gramps** (logiciel libre de généalogie) pour **consulter**
et **faire vivre** les données de l'arbre Tanguy, et comment publier les mises à jour sur le site
https://ronant99-lgtm.github.io/arbre-tanguy.

> Les intitulés de menus ci-dessous correspondent à Gramps 5.x en français ; ils peuvent varier
> légèrement selon la version. Les recherches de 2024 ont été saisies avec **Gramps 5.1.6**.

---

## Sommaire

1. [Avant tout : sauvegarder et récupérer la version à jour](#1-avant-tout--sauvegarder-et-récupérer-la-version-à-jour)
2. [Se repérer dans Gramps](#2-se-repérer-dans-gramps)
3. [Visualiser l'arbre](#3-visualiser-larbre)
4. [Gérer les données](#4-gérer-les-données)
5. [Rattacher les actes PDF (sources)](#5-rattacher-les-actes-pdf-sources)
6. [Contrôler la cohérence](#6-contrôler-la-cohérence)
7. [Publier sur le site](#7-publier-sur-le-site)
8. [Aide-mémoire](#8-aide-mémoire)

---

## 1. Avant tout : sauvegarder et récupérer la version à jour

Le fichier `gedcom/Tanguy.ged` du dépôt GitHub contient des **ajouts qui ne sont pas encore dans
la base Gramps** de l'ordinateur où les recherches ont été faites :

- la **génération 6** (30 ancêtres, chacun avec une note « à confirmer ») ;
- les **professions** de 29 personnes ;
- la correction du mariage **Lautout – Thoraval : 1829** (et non 1839) ;
- l'**implexe Thoraval – Thépot** (un même couple d'ancêtres par le père et par la mère).

Pour ne rien perdre, il faut repartir de ce fichier :

1. **Sauvegarder la base actuelle** : *Arbre familial → Faire une sauvegarde…*
   (crée un fichier `.gramps` complet ; le garder précieusement, par exemple sur le Drive).
2. **Télécharger** `Tanguy.ged` depuis GitHub : ouvrir
   https://github.com/ronant99-lgtm/arbre-tanguy/blob/main/gedcom/Tanguy.ged
   puis le bouton **⬇ (Download raw file)**.
3. **Créer un nouvel arbre** : *Arbre familial → Gérer les arbres familiaux… → Nouveau*,
   le nommer par exemple « Tanguy 2026 », puis **Charger l'arbre**.
4. **Importer** : *Arbre familial → Importer…* → choisir `Tanguy.ged`.
5. Vérifier rapidement (vue *Personnes* : 62 personnes) puis **travailler désormais dans ce
   nouvel arbre**. L'ancien reste disponible en cas de besoin.

> Pourquoi un nouvel arbre ? Importer dans l'ancien créerait des **doublons** de chaque personne.

---

## 2. Se repérer dans Gramps

La colonne de gauche (le *navigateur*) donne accès aux vues. Les plus utiles ici :

| Vue | À quoi elle sert |
|---|---|
| **Personnes** | liste de tous les individus, regroupés par nom ; double-clic = fiche complète |
| **Relations** | la personne active avec ses parents, conjoints, enfants : idéal pour naviguer de proche en proche |
| **Familles** | les couples, avec date et lieu du mariage |
| **Graphiques** | arbre d'ascendance et éventails (voir § 3) |
| **Événements** | naissances, mariages, décès, professions… avec leurs dates et lieux |
| **Lieux** | les communes (Kerpert, St Gilles Pligeaux, Canihuel, Lanrivain…) |
| **Sources / Citations** | les registres et les actes qui prouvent chaque information |
| **Médias** | les fichiers rattachés (actes PDF, photos) |
| **Notes** | toutes les notes de dépouillement des actes |

**Personne active** : la plupart des vues sont centrées sur elle. Pour repartir de Jean :
sélectionner *Jean Gustave Marie TANGUY* puis *Édition → Définir la personne de référence*
(la petite maison 🏠 de la barre d'outils y ramène ensuite en un clic).

---

## 3. Visualiser l'arbre

### À l'écran

- **Graphiques → Arborescence** (vue « pédigrée ») : l'arbre d'ascendance classique.
  Clic droit sur le fond pour choisir le nombre de générations affichées (mettre 6 ou plus).
  Double-clic sur une case pour ouvrir la fiche.
- **Graphiques → Graphique en éventail** : la roue des ascendants, très lisible jusqu'à
  6 générations ; les cases vides montrent immédiatement **où il reste à chercher**.
- **Graphiques → Éventail à 2 voies** : ascendants et descendants autour de la personne active.
- **Relations** : la meilleure vue pour vérifier une famille (frères et sœurs, remariages).

### Sur papier ou en PDF

Menu **Rapports** :

- *Rapports graphiques → Arbre des ascendants* : un grand arbre imprimable (choisir PDF,
  6 générations, une ou plusieurs pages).
- *Rapports graphiques → Graphique en éventail* : l'éventail imprimable.
- *Rapports textuels → Rapport détaillé des ascendants* : c'est le rapport « Liste détaillée des
  ascendants » déjà présent dans le Drive (*Rapport d'ascendance de Jean Tanguy.pdf*) ;
  le relancer après chaque mise à jour pour le tenir à jour.

### Sur une carte

- Vue **Géographie** : affiche les lieux sur une carte, à condition d'avoir saisi leurs
  **coordonnées** (vue *Lieux* → double-clic sur la commune → champs *Latitude / Longitude*).
  Toutes les communes de l'arbre sont dans un rayon d'environ 20 km autour de Kerpert.

---

## 4. Gérer les données

### Ajouter ou corriger une personne

- **Ajouter un parent** : vue *Relations*, personne sélectionnée → bouton
  *Ajouter un nouveau parent* (ou *Ajouter les parents*), puis remplir le père et/ou la mère.
- **Corriger une date, un lieu** : double-clic sur la personne → onglet *Événements* →
  double-clic sur l'événement (Naissance, Décès…).
- **Fusionner deux doublons** : vue *Personnes*, sélectionner les deux (Ctrl + clic) →
  *Édition → Fusionner…*.

### Écrire les dates

Gramps comprend les dates saisies en français. Exemples utiles pour cet arbre :

| Ce que dit l'acte | À saisir | Affiché sur le site |
|---|---|---|
| date exacte | `17 novembre 1875` | 17 novembre 1875 |
| âge seulement (« 38 ans en 1820 ») | `vers 1782` | vers 1782 |
| « feu » au mariage de 1829 | `avant 6 février 1829` | avant 6 février 1829 |
| vivant en 1898, décès introuvable | `après 1898` | après 1898 |
| calendrier républicain | bouton à droite du champ date → *Calendrier : Républicain français*, puis jour / mois / an (ex. 4 germinal an V) | 24 mars 1797 (4 germinal an V) |

### Professions

Une profession est un **événement « Profession »** : fiche de la personne → onglet *Événements*
→ **+** → type *Profession* → texte dans le champ **Description** (ex. « Laboureur »).
C'est ce texte qui apparaît sur le site.

### Notes

Les notes de dépouillement sont le cœur du travail. Convention à conserver :
**une ligne par information**, commençant par `/` (c'est ainsi que les notes de 2024 sont écrites).
Sur le site, **chaque ligne devient un paragraphe**.

- note sur une **personne** → onglet *Notes* de la personne ;
- note sur un **mariage** (témoins, signatures) → fiche de la famille, onglet *Notes* ;
  elle s'affiche sur le site dans « Acte de mariage (témoins, détails) ».

### Implexe (ancêtres présents plusieurs fois)

Quand on découvre que deux ancêtres sont frère et sœur, **ne pas recréer leurs parents** :
fiche de l'enfant → onglet *Références / Parents* → *Ajouter la personne comme enfant
d'une famille existante* (icône de partage), et choisir la famille déjà créée.
C'est ce qui a été fait pour Yves THORAVAL (1810) et Anne THORAVAL (1808), enfants de
Jean THORAVAL et Marie Anne THÉPOT. Le site le signale par le symbole **∞**.

Outil pratique : *Outils → Utilitaires → Calculateur de relation* indique le lien de parenté
entre deux personnes, même par plusieurs chemins.

### Étiquettes « à vérifier »

Les **étiquettes** permettent de suivre le travail restant :
*Édition → Étiquette → Nouvelle étiquette…* (ex. « À confirmer », couleur orange),
puis sélectionner des personnes et *Édition → Étiquette → À confirmer*.
Suggestion : étiqueter les 30 personnes de la génération 6 et retirer l'étiquette
au fur et à mesure que leurs propres actes sont trouvés. Le filtre de la barre latérale
(*Affichage → Barre latérale*) permet ensuite de ne lister que les fiches étiquetées.

---

## 5. Rattacher les actes PDF (sources)

Aujourd'hui, les ~60 actes du dossier Drive *Corpus actes en pdf* ne sont reliés à aucune fiche.
Les rattacher permet de retrouver la preuve de chaque date en un clic. Gramps distingue :

- **Source** = le registre (ex. « État civil de Kerpert, naissances, AD 22 ») ;
- **Citation** = l'acte précis dans ce registre (ex. « acte n° 23, vue 12 ») ;
- **Média** = le fichier (le PDF de l'acte).

Marche à suivre, une fois par acte :

1. Ouvrir l'événement concerné (ex. Naissance de Guillaume TANGUY) → onglet *Citations* → **+**.
2. *Source* : choisir ou créer la source (ex. « État civil de Kerpert — AD des Côtes-d'Armor »).
3. *Volume/Page* : le numéro d'acte ou de vue.
4. Dans la citation, onglet *Galerie* → **+** → choisir le PDF (ex. `AN_Tanguy_G_1905.pdf`).

Les noms de fichiers du corpus suivent déjà une convention claire, à garder :
`AN_` naissance · `AM_` mariage · `DC_` décès, puis NOM_initiales_année.
Deux fichiers sont mal datés et gagneraient à être renommés :
`AM_Thoraval-Le Provost_1818` → **1838**, `DC_Le Pape_J_1817` → **1897**.

> Conseil : rassembler les PDF dans un seul dossier sur l'ordinateur et indiquer ce dossier
> dans *Édition → Préférences → Général → Chemin de base pour les médias relatifs*.
> Ainsi, la base reste valable si le dossier est déplacé ou copié sur un autre ordinateur.

---

## 6. Contrôler la cohérence

- **Dans Gramps** : *Outils → Utilitaires → Vérifier les données…* signale les âges
  improbables (mère trop jeune ou trop âgée, mariage après le décès, etc.).
- **Sur GitHub** : à chaque dépôt du GEDCOM, l'onglet **Actions** du dépôt affiche un résumé
  avec les **points à vérifier** détectés par le script (c'est ainsi qu'a été repérée
  l'erreur 1839 / 1829).

---

## 7. Publier sur le site

1. **Exporter** : *Arbre familial → Exporter…* → format **GEDCOM** → *Suivant*.
2. Options de l'assistant :
   - Filtre : *Toute la base* ;
   - **Personnes vivantes : les exclure** (le site est public) ;
   - cocher l'export des notes.
3. Nommer le fichier **`Tanguy.ged`**.
4. Sur GitHub : ouvrir le dossier
   https://github.com/ronant99-lgtm/arbre-tanguy/tree/main/gedcom →
   *Add file → Upload files* → déposer `Tanguy.ged` → **Commit changes**.
5. Après 1 à 2 minutes, le site est à jour. Le résumé de l'onglet *Actions* indique le nombre
   de fiches générées et les éventuels points à vérifier.

> Le site ne lit **que** le GEDCOM (plus les photos et compléments ajoutés via le site).
> Toute correction de nom, date, lieu ou note se fait donc dans Gramps, puis s'exporte.

---

## 8. Aide-mémoire

| Je veux… | Où |
|---|---|
| voir l'arbre | *Graphiques → Arborescence* ou *Graphique en éventail* |
| imprimer l'arbre | *Rapports → Rapports graphiques → Arbre des ascendants* |
| refaire le rapport détaillé | *Rapports → Rapports textuels → Rapport détaillé des ascendants* |
| ajouter des parents | vue *Relations* → *Ajouter un nouveau parent* |
| saisir une profession | fiche → *Événements* → **+** → type *Profession* (texte en *Description*) |
| relier un acte PDF | événement → *Citations* → **+** → source, page, puis *Galerie* → PDF |
| marquer « à vérifier » | *Édition → Étiquette* |
| contrôler les dates | *Outils → Utilitaires → Vérifier les données…* |
| connaître un lien de parenté | *Outils → Utilitaires → Calculateur de relation* |
| sauvegarder | *Arbre familial → Faire une sauvegarde…* |
| publier sur le site | *Arbre familial → Exporter… → GEDCOM*, puis dépôt dans `gedcom/` sur GitHub |

Documentation officielle : https://gramps-project.org (rubrique *Wiki*, manuel disponible en
français ; depuis Gramps, la touche **F1** ouvre l'aide de la fenêtre en cours).
