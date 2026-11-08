# Arbre généalogique — Famille Tanguy

Arbre interactif des ascendants de Jean Gustave Marie Tanguy, hébergé sur GitHub Pages.

**URL publique :** https://ronant99-lgtm.github.io/arbre-tanguy

---

## 📁 Structure du dépôt

```
arbre-tanguy/
├── gedcom/Tanguy.ged          ← SOURCE DE RÉFÉRENCE : export GEDCOM de Gramps
├── complements.json           ← photos, professions, textes ajoutés via le site
├── data.json                  ← GÉNÉRÉ automatiquement (ne pas modifier à la main)
├── index.html                 ← l'arbre interactif
├── photos/                    ← portraits et images (à créer au besoin)
├── scripts/ged2json.py        ← conversion GEDCOM → data.json + contrôles de cohérence
└── .github/workflows/         ← régénération automatique de data.json
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

## 🖼️ Ajouter une photo, une profession ou un texte (depuis le site)

1. Ouvrir l'arbre, cliquer sur un ancêtre → **✎ Modifier**
2. Renseigner la photo, la profession et/ou des compléments biographiques → **Enregistrer**
3. Cliquer **⬇ Exporter** → télécharge `complements.json`
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
python3 scripts/ged2json.py            # écrit data.json et affiche les points à vérifier
python3 scripts/ged2json.py --root I0001 --out test.json   # autre personne de départ
```

Aucune installation nécessaire au-delà de Python 3.

---

## 🔒 Confidentialité

Le dépôt et le site sont **publics**. N'y mettre **que des personnes décédées** :
pas de personnes vivantes, ni de coordonnées (téléphones, adresses, courriels)
de correspondants. Les notes de recherche personnelles restent dans Google Drive.

---

## 👥 Contribuer en famille

Chacun peut proposer des corrections ou ajouts en envoyant un email avec le nom de l'ancêtre
concerné, la modification souhaitée et une photo éventuelle. La personne qui gère le dépôt
les intègre dans Gramps (données) ou via le site (photos, souvenirs).
