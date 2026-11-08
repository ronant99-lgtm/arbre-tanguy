# Arbre généalogique — Familles Tanguy et Beauchesne

Arbres interactifs hébergés sur GitHub Pages :

- **Famille Tanguy** — ascendants de Jean Gustave Marie Tanguy :
  https://ronant99-lgtm.github.io/arbre-tanguy/#tanguy
- **Famille Beauchesne** — ascendants de Françoise Beauchesne :
  https://ronant99-lgtm.github.io/arbre-tanguy/#beauchesne

---

## 📁 Structure du dépôt

```
arbre-tanguy/
├── arbres.json                ← liste des arbres du site (titre, GEDCOM, personne de départ…)
├── gedcom/Tanguy.ged          ← SOURCE DE RÉFÉRENCE : export GEDCOM de Gramps
├── gedcom/Beauchesne.ged      ← extrait PUBLIC de la base Beauchesne (voir plus bas)
├── complements*.json          ← photos, professions, textes ajoutés via le site (un par arbre)
├── data.json, data_beauchesne.json ← GÉNÉRÉS automatiquement (ne pas modifier à la main)
├── index.html                 ← l'arbre interactif
├── photos/                    ← portraits et images (à créer au besoin)
├── scripts/ged2json.py        ← conversion GEDCOM → data*.json + contrôles de cohérence
├── scripts/extraire_ascendants.py ← base complète privée → extrait publiable
└── .github/workflows/         ← régénération automatique des données
```

Le principe : **on ne saisit les données qu'une seule fois, dans Gramps.**
Le site se reconstruit tout seul à partir du fichier GEDCOM.

```
Gramps ──export──► gedcom/Tanguy.ged ─┐
                                      ├──► (GitHub Actions) ──► data.json ──► site
Site « Exporter » ► complements.json ─┘
```

---

## ✏️ Mettre à jour l'arbre depuis Gramps (dates, lieux, personnes, notes)

📘 Guide complet d'utilisation de Gramps pour cet arbre (visualisation, saisie, sources,
publication) : [docs/guide-gramps.md](docs/guide-gramps.md)

1. Dans Gramps : **Arbre familial → Exporter… → GEDCOM**, enregistrer sous `Tanguy.ged`
2. Sur GitHub, ouvrir le dossier `gedcom/` → **Add file → Upload files** → déposer `Tanguy.ged` (remplace l'ancien)
3. Valider (**Commit changes**)
4. Patienter 1 à 2 minutes : l'action « Générer l'arbre depuis Gramps » régénère `data.json`,
   puis le site se met à jour. Son résumé (onglet **Actions**) liste aussi les **points à vérifier**
   (dates incohérentes, mariage après un décès, etc.).

> ⚠️ **Avant de continuer à travailler dans Gramps**, importez-y la version du GEDCOM présente
> dans ce dépôt (**Arbre familial → Importer…**, dans un nouvel arbre) : elle contient des
> corrections et la génération 6 ajoutées directement dans le fichier. Sinon, votre prochain
> export les effacerait.

---

## 🌳 Arbre Beauchesne : base privée, extrait public

La base Beauchesne complète (`Bauchesne.ged`, ~2 000 personnes, dont des personnes vivantes,
des adresses et des courriels) est conservée dans le dépôt **privé** `genealogie-sources`.
Le site n'en publie qu'un **extrait** : `gedcom/Beauchesne.ged`, produit par

```bash
python3 scripts/extraire_ascendants.py ../genealogie-sources/Bauchesne.ged I0022 gedcom/Beauchesne.ged \
    gedcom/corrections_beauchesne.json
```

Cet extrait contient l'ascendance de Françoise Beauchesne (I0022) avec notes et sources, plus
les frères, sœurs et conjoints **décédés** (fiche réduite). Il retire les personnes possiblement
vivantes, les résidences et adresses, et dans les textes les courriels, téléphones et contacts.

Pour mettre à jour l'arbre Beauchesne :
1. exporter la base complète depuis Gramps (GEDCOM) et la déposer dans `genealogie-sources` ;
2. relancer la commande ci-dessus (ou demander à Claude de le faire) et déposer le nouvel
   `gedcom/Beauchesne.ged` dans ce dépôt : le site se met à jour seul.

`gedcom/corrections_beauchesne.json` liste les corrections appliquées à chaque extraction tant
qu'elles ne sont pas faites dans la base Gramps (aujourd'hui : naissance de Jean Gustave Marie
TANGUY le **31 octobre 1946**, la base indiquant 6 octobre 1945).

> ⚠️ Déposer dans `genealogie-sources` l'export de la **base complète** (celle de l'oncle).
> Un export fait après import de l'extrait public ne contient que cet extrait.

---

## 🖼️ Ajouter une photo, une profession ou un texte (depuis le site)

1. Ouvrir l'arbre, cliquer sur un ancêtre → **✎ Modifier**
2. Renseigner la photo, la profession et/ou des compléments biographiques → **Enregistrer**
3. Cliquer **⬇ Exporter** → télécharge `complements.json` (arbre Tanguy) ou
   `complements_beauchesne.json` (arbre Beauchesne)
4. Déposer ce fichier à la racine du dépôt GitHub (remplace l'ancien)
5. L'arbre se met à jour automatiquement en 1 à 2 minutes

Les noms, dates, lieux, unions et notes d'archives ne se modifient **que dans Gramps**.

### Photos

- **Dans le dépôt (recommandé)** : JPG ou PNG, ~400×500 px, < 300 Ko, nommée clairement
  (`jean_tanguy_1875.jpg`), déposée dans `photos/` ; renseigner `photos/jean_tanguy_1875.jpg`.
- **URL externe** : coller un lien direct vers l'image.

---

## 🧩 Ce qu'affiche chaque fiche

- dates complètes (y compris calendrier républicain converti : « 24 mars 1797 (4 germinal an V) »)
  et dates approximatives (« vers 1785 », « avant 1829 », « après 1898 ») ;
- profession, lieux de naissance et de décès ;
- union(s) : conjoint, date et lieu du mariage, détail de l'acte (témoins…) ;
- frères et sœurs connus dans Gramps ;
- **implexe (∞)** : ancêtre présent plusieurs fois dans l'arbre ;
- notes d'archives (depuis Gramps) suivies des compléments ajoutés via le site.

---

## 🛠️ Générer data.json à la main (facultatif)

```bash
python3 scripts/ged2json.py            # régénère tous les arbres de arbres.json + points à vérifier
python3 scripts/ged2json.py --root I0001 --out test.json   # autre personne de départ
```

Aucune installation nécessaire au-delà de Python 3.

---

## 🔒 Confidentialité

Le dépôt et le site sont **publics**. N'y mettre **que des personnes décédées** (les bases
complètes restent dans le dépôt privé `genealogie-sources`) :
pas de personnes vivantes, ni de coordonnées (téléphones, adresses, courriels)
de correspondants. Les notes de recherche personnelles restent dans Google Drive.

---

## 👥 Contribuer en famille

Chacun peut proposer des corrections ou ajouts en envoyant un email avec le nom de l'ancêtre
concerné, la modification souhaitée et une photo éventuelle. La personne qui gère le dépôt
les intègre dans Gramps (données) ou via le site (photos, souvenirs).
