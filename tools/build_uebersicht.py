#!/usr/bin/env python3
"""Erzeugt die Übersichtsseite (Momentaufnahme) aus zwei Notion-Abfrageergebnissen.

Aufruf:
  python3 tools/build_uebersicht.py TAGE.json GEDANKEN.json [--today YYYY-MM-DD]

TAGE.json     Ergebnis der Notion-Ansicht "Verlauf" (Meine Recovery Zone), {"results": [...]}
GEDANKEN.json Ergebnis der Notion-Ansicht "Wie oft pro Gedanke" (Gedanken-Statistik), {"results": [...]}

Ausgabe: u/0b2fd134a6c639ab/index.html. Heute und spätere Tage zählen nicht mit.
Bewusst nicht enthalten: Notizen, Uhrzeiten, Orte, Stärke der Urges und die Wahrheiten.
"""
import json, re, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "u" / "0b2fd134a6c639ab" / "index.html"
TEMPLATE = ROOT / "tools" / "uebersicht_template.html"
ITEMS = ["Bilder", "Edging", "Pornografie", "Masturbation", "Lüstern", "Scrollen",
         "Fantasien", "Chaos in mir", "Zeit mit Gott", "Lesen", "Zeit draußen"]
TOP_GEDANKEN = 6


def load(p):
    d = json.load(open(p, encoding="utf-8"))
    return d["results"] if isinstance(d, dict) else d


def main():
    argv = sys.argv[1:]
    today = datetime.date.today().isoformat()
    if "--today" in argv:
        i = argv.index("--today")
        today = argv[i + 1]
        del argv[i:i + 2]
    args = argv
    if len(args) != 2:
        sys.exit(__doc__)
    tage_rows, gedanken_rows = load(args[0]), load(args[1])

    tage, urges = {}, {}
    for r in tage_rows:
        d = r.get("date:Datum:start")
        if not d or d >= today:
            continue
        tage[d] = [i for i in ITEMS if "❌" in str(r.get(i, ""))]
        n = len(re.findall(r"Urge ausgehalten", str(r.get("Notiz", ""))))
        if n:
            urges[d] = n
    if not tage:
        sys.exit("Keine Tage gefunden, Abbruch.")

    gedanken = []
    for r in gedanken_rows:
        name = (r.get("Gedanke") or "").strip()
        try:
            n = len(json.loads(r.get("Einträge") or "[]"))
        except ValueError:
            n = 0
        if name and n:
            gedanken.append([name, n])
    gedanken.sort(key=lambda x: -x[1])

    data = {"stand": today, "tage": dict(sorted(tage.items())),
            "urges": dict(sorted(urges.items())), "gedanken": gedanken[:TOP_GEDANKEN]}
    html = TEMPLATE.read_text(encoding="utf-8").replace(
        "__DATA__", json.dumps(data, ensure_ascii=False))
    OUT.write_text(html, encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: {len(tage)} Tage, {sum(urges.values())} Urges, {len(data['gedanken'])} Gedanken, Stand {today}")


main()
