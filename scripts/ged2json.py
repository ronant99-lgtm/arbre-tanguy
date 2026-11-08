#!/usr/bin/env python3
"""Convertit l'export Gramps (GEDCOM 5.5.1) en data.json pour l'arbre interactif.

Usage :
    python3 scripts/ged2json.py                      # valeurs par défaut
    python3 scripts/ged2json.py --ged gedcom/Tanguy.ged --root I0000 \
        --complements complements.json --out data.json

- Le GEDCOM est la source de référence (dates, lieux, unions, notes, professions).
- complements.json (facultatif) ajoute ou remplace des champs par personne
  (photo, profession, bio complémentaire...) : {"I0001": {"photo": "photos/x.jpg"}}.
- data.json est un arbre d'ascendance : "children" = [père, mère].

Aucune dépendance externe : bibliothèque standard Python 3.8+.
"""
import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

MONTHS_EN = {m: i for i, m in enumerate(
    "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split(), 1)}
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
             "août", "septembre", "octobre", "novembre", "décembre"]

# Calendrier républicain : mois GEDCOM -> nom, et 1er vendémiaire de chaque an.
REP_MONTHS = ["VEND", "BRUM", "FRIM", "NIVO", "PLUV", "VENT", "GERM",
              "FLOR", "PRAI", "MESS", "THER", "FRUC", "COMP"]
REP_MONTHS_FR = ["vendémiaire", "brumaire", "frimaire", "nivôse", "pluviôse",
                 "ventôse", "germinal", "floréal", "prairial", "messidor",
                 "thermidor", "fructidor", "jour complémentaire"]
REP_YEAR_START = {  # an -> date grégorienne du 1er vendémiaire
    1: (1792, 9, 22), 2: (1793, 9, 22), 3: (1794, 9, 22), 4: (1795, 9, 23),
    5: (1796, 9, 22), 6: (1797, 9, 22), 7: (1798, 9, 22), 8: (1799, 9, 23),
    9: (1800, 9, 23), 10: (1801, 9, 23), 11: (1802, 9, 23), 12: (1803, 9, 24),
    13: (1804, 9, 23), 14: (1805, 9, 23),
}
QUALIFIERS = {"ABT": ("vers", "v."), "EST": ("vers", "v."), "CAL": ("vers", "v."),
              "BEF": ("avant", "av."), "AFT": ("après", "ap.")}


def roman(n):
    vals = [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


# ─── Lecture du GEDCOM ──────────────────────────────────────────────────
class Node:
    __slots__ = ("level", "xref", "tag", "value", "children")

    def __init__(self, level, xref, tag, value):
        self.level, self.xref, self.tag, self.value = level, xref, tag, value
        self.children = []

    def first(self, tag):
        return next((c for c in self.children if c.tag == tag), None)

    def all(self, tag):
        return [c for c in self.children if c.tag == tag]

    def text(self):
        """Valeur avec ses CONC/CONT."""
        s = self.value or ""
        for c in self.children:
            if c.tag == "CONC":
                s += c.value or ""
            elif c.tag == "CONT":
                s += "\n" + (c.value or "")
        return s


LINE_RE = re.compile(r"^\s*(\d+)\s+(?:(@[^@]+@)\s+)?(\S+)(?:\s(.*))?$")


def parse_gedcom(path):
    records, stack = [], []
    with open(path, encoding="utf-8-sig") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            if not line.strip():
                continue
            m = LINE_RE.match(line)
            if not m:
                raise ValueError(f"Ligne GEDCOM illisible : {line!r}")
            lvl, xref, tag, val = int(m[1]), m[2], m[3], m[4]
            node = Node(lvl, xref, tag, val)
            while stack and stack[-1].level >= lvl:
                stack.pop()
            if stack:
                stack[-1].children.append(node)
            else:
                records.append(node)
            stack.append(node)
    return records


# ─── Dates ──────────────────────────────────────────────────────────────
def parse_date(value):
    """Retourne {'texte': str complet FR, 'court': str pour la vignette, 'annee': int|None}."""
    if not value:
        return None
    v = value.strip()
    qual = None
    parts = v.split()
    if parts and parts[0] in QUALIFIERS:
        qual, v = parts[0], " ".join(parts[1:])

    texte, annee = v, None
    m = re.match(r"@#DFRENCH R@\s+(?:(\d+)\s+)?(?:([A-Z]{4})\s+)?(\d+)$", v)
    if m:
        day, mon, an = int(m[1] or 1), m[2], int(m[3])
        rep = f"an {roman(an)}"
        if mon:
            rep = f"{mon and REP_MONTHS_FR[REP_MONTHS.index(mon)]} {rep}"
        if m[1]:
            rep = f"{int(m[1])} {rep}"
        if an in REP_YEAR_START and mon:
            start = dt.date(*REP_YEAR_START[an])
            g = start + dt.timedelta(days=REP_MONTHS.index(mon) * 30 + day - 1)
            annee = g.year
            greg = f"{g.day} {MONTHS_FR[g.month - 1]} {g.year}" if m[1] else \
                f"{MONTHS_FR[g.month - 1]} {g.year}"
            texte = f"{greg} ({rep})"
        else:
            texte = rep
    else:
        m = re.match(r"(?:(\d{1,2})\s+)?(?:([A-Z]{3})\s+)?(\d{3,4})$", v)
        if m:
            annee = int(m[3])
            texte = str(annee)
            if m[2] in MONTHS_EN:
                texte = f"{MONTHS_FR[MONTHS_EN[m[2]] - 1]} {annee}"
                if m[1]:
                    texte = f"{int(m[1])} {texte}"

    court = str(annee) if annee else texte
    if qual:
        long_q, short_q = QUALIFIERS[qual]
        texte, court = f"{long_q} {texte}", f"{short_q} {court}"
    return {"texte": texte, "court": court, "annee": annee}


def short_place(plac):
    """'Kerpert, 22092, France' -> 'Kerpert'."""
    return (plac or "").split(",")[0].strip()


# ─── Notes ──────────────────────────────────────────────────────────────
def note_text(node, notes):
    """Texte d'une NOTE (en ligne ou référence @N..@)."""
    if node.value and re.fullmatch(r"@[^@]+@", node.value.strip()):
        ref = notes.get(node.value.strip())
        return ref.text() if ref else ""
    return node.text()


def note_html(texts):
    """Notes Gramps (lignes commençant par '/') -> paragraphes HTML."""
    paras = []
    for t in texts:
        for line in t.split("\n"):
            line = line.strip()
            if line.startswith("/"):
                line = line[1:].strip()
            if line:
                paras.append(f"<p>{html.escape(line, quote=False)}</p>")
    return "".join(paras)


# ─── Construction ───────────────────────────────────────────────────────
def build(records, root_id, complements):
    indis = {r.xref: r for r in records if r.tag == "INDI"}
    fams = {r.xref: r for r in records if r.tag == "FAM"}
    notes = {r.xref: r for r in records if r.tag == "NOTE"}

    def pid(xref):
        return xref.strip("@")

    def event(indi, tag):
        ev = indi.first(tag)
        if not ev:
            return None, "", []
        d = ev.first("DATE")
        evnotes = [note_text(n, notes) for n in ev.all("NOTE")]
        return (parse_date(d.value) if d else None,
                short_place(ev.first("PLAC").value) if ev.first("PLAC") else "",
                evnotes)

    def name_parts(indi):
        n = indi.first("NAME")
        given = surname = ""
        if n:
            g, s = n.first("GIVN"), n.first("SURN")
            given = g.value if g else (n.value or "").split("/")[0].strip()
            surname = s.value if s else (re.findall(r"/([^/]*)/", n.value or "") or [""])[0]
        return (given or "").strip(), (surname or "").strip()

    def label(xref):
        indi = indis.get(xref)
        if not indi:
            return ""
        g, s = name_parts(indi)
        b, _, _ = event(indi, "BIRT")
        d, _, _ = event(indi, "DEAT")
        yrs = f" ({b['court'] if b else '?'} – {d['court'] if d else '?'})" if (b or d) else ""
        return f"{g} {s}{yrs}".strip()

    # Nombre d'apparitions de chaque personne dans l'ascendance (implexe).
    seen = {}

    def count(xref, depth=0):
        if depth > 40:
            return
        seen[xref] = seen.get(xref, 0) + 1
        fam = parent_family(xref)
        if fam:
            for t in ("HUSB", "WIFE"):
                p = fam.first(t)
                if p:
                    count(p.value, depth + 1)

    def parent_family(xref):
        indi = indis.get(xref)
        famc = indi.first("FAMC") if indi else None
        return fams.get(famc.value) if famc else None

    count(root_id)

    def person(xref, depth=0, path=()):
        indi = indis[xref]
        given, surname = name_parts(indi)
        sex = (indi.first("SEX").value if indi.first("SEX") else "U") or "U"
        b, bplace, bnotes = event(indi, "BIRT")
        d, dplace, dnotes = event(indi, "DEAT")
        occu = indi.first("OCCU")

        texts = [note_text(n, notes) for n in indi.all("NOTE")]
        texts += [f"/Naissance : {t.lstrip('/')}" for t in bnotes if t.strip()]
        texts += [f"/Décès : {t.lstrip('/')}" for t in dnotes if t.strip()]

        p = {
            "id": pid(xref),
            "given": given,
            "surname": surname,
            "name": f"{given.split(' ')[0] if given else ''}\n{surname}",
            "gender": sex if sex in ("M", "F") else "U",
            "born": b["court"] if b else None,
            "died": d["court"] if d else None,
            "date_naissance": b["texte"] if b else "",
            "date_deces": d["texte"] if d else "",
            "lieu_naissance": bplace,
            "lieu_deces": dplace,
            "profession": (occu.text() if occu else "").strip(),
            "photo": None,
            "bio": note_html(texts),
        }

        # Unions (en tant que conjoint)
        unions = []
        for fs in indi.all("FAMS"):
            fam = fams.get(fs.value)
            if not fam:
                continue
            other = fam.first("WIFE" if sex == "M" else "HUSB")
            marr = fam.first("MARR")
            md = parse_date(marr.first("DATE").value) if marr and marr.first("DATE") else None
            mplace = short_place(marr.first("PLAC").value) if marr and marr.first("PLAC") else ""
            ftexts = [note_text(n, notes) for n in fam.all("NOTE")]
            if marr:
                ftexts += [note_text(n, notes) for n in marr.all("NOTE")]
            unions.append({
                "conjoint": label(other.value) if other else "",
                "date": md["texte"] if md else "",
                "lieu": mplace,
                "notes": note_html(ftexts),
            })
        if unions:
            p["unions"] = unions

        # Fratrie (autres enfants de la famille d'origine)
        fam = parent_family(xref)
        if fam:
            sibs = [label(c.value) for c in fam.all("CHIL") if c.value != xref]
            if sibs:
                p["fratrie"] = sibs

        if seen.get(xref, 0) > 1:
            p["implexe"] = seen[xref]

        # Compléments manuels (photo, profession, bio ajoutée...)
        extra = complements.get(p["id"], {})
        for k, v in extra.items():
            if k == "bio_ajout":
                p["bio"] = (p["bio"] or "") + v
            else:
                p[k] = v

        # Ascendants : père puis mère
        kids = []
        if fam and depth < 40 and xref not in path:
            for t in ("HUSB", "WIFE"):
                par = fam.first(t)
                if par and par.value in indis:
                    kids.append(person(par.value, depth + 1, path + (xref,)))
        p["children"] = kids
        return p

    return person(root_id)


def _year(s):
    m = re.search(r"\d{4}", s or "")
    return int(m.group()) if m else None


def check(tree):
    """Contrôles de cohérence simples ; retourne une liste d'alertes (texte)."""
    alerts = []

    def nm(p):
        return f"{p['given']} {p['surname']} ({p['id']})"

    def exact(s):  # année uniquement si la date n'est pas approximative
        return None if re.match(r"(vers|avant|après)", s or "") else _year(s)

    def walk(p):
        b, d = exact(p["date_naissance"]), exact(p["date_deces"])
        if b and d and d < b:
            alerts.append(f"{nm(p)} : décès ({d}) avant la naissance ({b})")
        if b and d and d - b > 105:
            alerts.append(f"{nm(p)} : âge au décès improbable ({d - b} ans)")
        for u in p.get("unions", []):
            m = exact(u["date"])
            if m and d and m > d:
                alerts.append(f"{nm(p)} : mariage ({m}) après son décès ({d})")
            if m and b and m - b < 14:
                alerts.append(f"{nm(p)} : marié(e) à {m - b} ans")
        for par in p["children"]:
            pb, pd = exact(par["date_naissance"]), exact(par["date_deces"])
            if b and pb:
                ecart = b - pb
                if ecart < 14:
                    alerts.append(f"{nm(par)} : avait {ecart} ans à la naissance de {nm(p)}")
                elif par["gender"] == "F" and ecart > 50:
                    alerts.append(f"{nm(par)} : mère à {ecart} ans de {nm(p)}")
            if b and pd:
                limite = pd + (1 if par["gender"] == "M" else 0)
                if b > limite:
                    alerts.append(f"{nm(p)} : né(e) en {b}, après le décès de {nm(par)} ({pd})")
            walk(par)

    walk(tree)
    return sorted(set(alerts))


def main(argv=None):
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ged", default=str(here / "gedcom" / "Tanguy.ged"))
    ap.add_argument("--root", default="I0000", help="identifiant Gramps du sujet (sans @)")
    ap.add_argument("--complements", default=str(here / "complements.json"))
    ap.add_argument("--out", default=str(here / "data.json"))
    ap.add_argument("--strict", action="store_true",
                    help="échoue si des incohérences sont détectées")
    args = ap.parse_args(argv)

    records = parse_gedcom(args.ged)
    comp_path = Path(args.complements)
    complements = json.loads(comp_path.read_text(encoding="utf-8")) if comp_path.exists() else {}
    complements = {k: v for k, v in complements.items() if not k.startswith("_")}

    root = f"@{args.root.strip('@')}@"
    if root not in {r.xref for r in records if r.tag == "INDI"}:
        sys.exit(f"Personne {root} introuvable dans {args.ged}")

    tree = build(records, root, complements)
    out = json.dumps(tree, ensure_ascii=False, indent=2) + "\n"
    Path(args.out).write_text(out, encoding="utf-8")

    n = 0
    stack = [tree]
    while stack:
        x = stack.pop()
        n += 1
        stack.extend(x["children"])
    print(f"{args.out} : {n} fiches générées depuis {args.ged}")

    alerts = check(tree)
    if alerts:
        print(f"\n{len(alerts)} point(s) à vérifier :")
        for a in alerts:
            print(f"  - {a}")
        if args.strict:
            sys.exit(1)


if __name__ == "__main__":
    main()
