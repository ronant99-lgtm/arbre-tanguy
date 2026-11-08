#!/usr/bin/env python3
"""Extrait d'un GEDCOM complet (privé) un GEDCOM publiable : l'ascendance d'une personne.

    python3 scripts/extraire_ascendants.py BASE_COMPLETE.ged I0022 gedcom/Beauchesne.ged \
        [gedcom/corrections_beauchesne.json]

Le fichier de corrections (facultatif) remplace des valeurs d'événements tant qu'elles
ne sont pas corrigées dans la base Gramps : {"I0038": {"BIRT": {"DATE": "31 OCT 1946"}}}.

Contenu du fichier produit :
- la personne de départ et tous ses ascendants, avec leurs événements, notes et sources ;
- leurs conjoints et enfants (frères et sœurs des ascendants) en fiche réduite
  (nom, sexe, naissance, décès), uniquement s'ils ne sont pas susceptibles d'être vivants ;
- les familles qui relient ces personnes.

Sont retirés : résidences et adresses (RESI, ADDR, EMAIL, PHON...), objets médias,
coordonnées de l'auteur, et dans les notes courriels, téléphones et contacts.
Personne « susceptible d'être vivante » : sans décès connu et née il y a moins de
100 ans, ou sans date de naissance avec un parent né il y a moins de 130 ans.
"""
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ged2json as g  # noqa: E402

RETIRER = {"RESI", "ADDR", "EMAIL", "PHON", "FAX", "WWW", "OBJE", "CHAN", "_UID", "SSN", "RIN", "REFN"}
GARDER_REDUIT = {"NAME", "SEX", "BIRT", "BAPM", "CHR", "DEAT", "BURI"}


CALENDRIER_RE = re.compile(r"(@#D[A-Z ]+@)")  # ex. @#DFRENCH R@ (calendrier républicain)


def propre(texte):
    """Texte nettoyé (courriels, téléphones, contacts), avec les @ ré-échappés pour GEDCOM
    (sauf les marqueurs de calendrier comme @#DFRENCH R@, qui doivent rester simples)."""
    morceaux = CALENDRIER_RE.split(g.nettoyer(texte))
    return "".join(m if CALENDRIER_RE.fullmatch(m) else m.replace("@", "@@") for m in morceaux)


def note_lines(level, tag, xref, text):
    """Réécrit un texte en lignes GEDCOM (CONT pour les retours, CONC au-delà de 200 car.)."""
    out = []
    for k, para in enumerate(propre(text).split("\n")):
        chunks = [para[i:i + 200] for i in range(0, len(para), 200)] or [""]
        if k == 0:
            head = f"{level} {xref + ' ' if xref else ''}{tag}"
            out.append(f"{head} {chunks[0]}".rstrip())
        else:
            out.append(f"{level + 1} CONT {chunks[0]}".rstrip())
        out += [f"{level + 1} CONC {c}" for c in chunks[1:]]
    return out


def is_pointer(v):
    return bool(v) and v.strip().startswith("@") and v.strip().endswith("@") and "@@" not in v


def serialize(node, keep, out, reduced=False):
    if node.tag in RETIRER:
        return
    if reduced and node.level == 1 and node.tag not in GARDER_REDUIT | {"FAMC", "FAMS"}:
        return
    if node.tag in ("FAMC", "FAMS", "HUSB", "WIFE", "CHIL") and node.value not in keep:
        return
    if is_pointer(node.value):
        out.append(f"{node.level} {node.tag} {node.value.strip()}")
        for c in node.children:
            serialize(c, keep, out, reduced)
        return
    texte = node.text() if node.value is not None or node.children else ""
    if texte:
        out += note_lines(node.level, node.tag, node.xref, texte)
    else:
        out.append(f"{node.level} {node.xref + ' ' if node.xref else ''}{node.tag}")
    for c in node.children:
        if c.tag not in ("CONC", "CONT"):
            serialize(c, keep, out, reduced)


def appliquer_corrections(recs, chemin):
    import json
    corr = json.loads(Path(chemin).read_text(encoding="utf-8"))
    indis = {r.xref: r for r in recs if r.tag == "INDI"}
    for pid, events in corr.items():
        if pid.startswith("_"):
            continue
        indi = indis.get(f"@{pid}@")
        if not indi:
            print(f"Correction ignorée : {pid} introuvable")
            continue
        for ev_tag, champs in events.items():
            if ev_tag.startswith("_"):
                continue
            ev = indi.first(ev_tag)
            if not ev:
                ev = g.Node(1, None, ev_tag, None)
                indi.children.append(ev)
            for tag, val in champs.items():
                n = ev.first(tag)
                if n:
                    if n.value != val:
                        print(f"Correction {pid} {ev_tag} {tag} : {n.value} -> {val}")
                    n.value = val
                else:
                    ev.children.append(g.Node(2, None, tag, val))
                    print(f"Correction {pid} {ev_tag} {tag} : (vide) -> {val}")


def main(src, root, dest, corrections=None):
    recs = g.parse_gedcom(src)
    if corrections:
        appliquer_corrections(recs, corrections)
    I = {r.xref: r for r in recs if r.tag == "INDI"}
    F = {r.xref: r for r in recs if r.tag == "FAM"}
    N = {r.xref: r for r in recs if r.tag == "NOTE"}
    S = {r.xref: r for r in recs if r.tag == "SOUR"}
    root = f"@{root.strip('@')}@"
    annee = dt.date.today().year

    # 1. Ascendants
    asc, pile = set(), [root]
    while pile:
        x = pile.pop()
        if x in asc or x not in I:
            continue
        asc.add(x)
        for fc in I[x].all("FAMC"):
            fam = F.get(fc.value)
            if fam:
                pile += [p.value for p in fam.all("HUSB") + fam.all("WIFE")]

    def parents_recents(x):
        for fc in I[x].all("FAMC"):
            fam = F.get(fc.value)
            for p in (fam.all("HUSB") + fam.all("WIFE")) if fam else []:
                a = g.annee_naissance(I[p.value]) if p.value in I else None
                if a and a >= annee - 130:
                    return True
        return False

    def peut_etre_vivant(x):
        indi = I[x]
        if indi.first("DEAT") or indi.first("BURI"):
            return False
        a = g.annee_naissance(indi)
        return (a >= annee - 100) if a else parents_recents(x)

    # 2. Familles des ascendants, conjoints et enfants
    fams, autres, exclus = set(), set(), set()
    for x in asc:
        for fs in I[x].all("FAMS"):
            fam = F.get(fs.value)
            if not fam:
                continue
            fams.add(fs.value)
            for m in fam.all("HUSB") + fam.all("WIFE") + fam.all("CHIL"):
                if m.value in I and m.value not in asc:
                    (exclus if peut_etre_vivant(m.value) else autres).add(m.value)
    keep = asc | autres | fams

    # 3. Notes et sources référencées par les ascendants et leurs familles
    def refs(node, acc):
        if node.tag in ("NOTE", "SOUR") and (node.value or "").startswith("@"):
            acc.add(node.value.strip())
        for c in node.children:
            refs(c, acc)
    used = set()
    for x in asc:
        refs(I[x], used)
    for f in fams:
        refs(F[f], used)
    for s in [u for u in used if u in S]:
        refs(S[s], used)
    keep |= used

    out = ["0 HEAD", "1 SOUR Gramps", "2 NAME Gramps", "1 SUBM @SUBM@", "1 GEDC", "2 VERS 5.5.1",
           "2 FORM LINEAGE-LINKED", "1 CHAR UTF-8", "1 LANG French",
           f"1 NOTE Extrait public : ascendance de {root} (généré par extraire_ascendants.py)",
           "0 @SUBM@ SUBM", "1 NAME Famille Tanguy"]
    for r in recs:
        if r.tag == "INDI" and r.xref in keep:
            serialize(r, keep, out, reduced=r.xref not in asc)
        elif r.tag == "FAM" and r.xref in keep:
            serialize(r, keep, out)
        elif r.tag == "NOTE" and r.xref in keep:
            out += note_lines(0, "NOTE", r.xref, r.text())
        elif r.tag == "SOUR" and r.xref in keep:
            serialize(r, keep, out)
    out.append("0 TRLR")
    Path(dest).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{dest} : {len(asc)} ascendants, {len(autres)} conjoints/frères/sœurs, "
          f"{len(fams)} familles, {len(used & set(N))} notes, {len(used & set(S))} sources ; "
          f"{len(exclus)} personne(s) possiblement vivante(s) exclue(s)")


if __name__ == "__main__":
    if len(sys.argv) not in (4, 5):
        sys.exit(__doc__)
    main(*sys.argv[1:])
