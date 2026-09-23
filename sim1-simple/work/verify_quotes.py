"""Check that key quotes attributed in the manifesto appear in each attendee's dossier."""
import pathlib, sys

ROOT = pathlib.Path("/Users/jasonpriem/ox/epistemic-futures-corpus/dossiers")
CHECKS = [
    ("blaise-aguera-y-arcas", "not delusional or"),
    ("benjamin-bratton", "Reflectionism"),
    ("benjamin-bratton", "ripping me off"),
    ("steven-sloman", "Ignorance is our natural state"),
    ("jason-priem", "evangelist"),
    ("amy-brand", "defaulting to the opt-in model"),
    ("selena-deckelmann", "pay per article"),
    ("henry-farrell", "obligate complement"),
    ("ivan-oransky", "flood insurance"),
    ("sherry-turkle", "There is no I there"),
    ("adam-becker", "fruit of the poisoned tree"),
    ("peter-salib", "AGI-denialist"),
    ("mahzarin-banaji", "not merely a mirror"),
    ("leslie-chan", "change the regime"),
    ("adrian-johns", "constant policing"),
    ("mike-caulfield", "no answers from nowhere"),
    ("david-krakauer", "competence collapse"),
    ("geoffrey-bilder", "context analysis, not content analysis"),
    ("nick-vincent", "quasi-enclosure"),
    ("tim-oreilly", "Pay for the output, not the training"),
    ("katherine-maher", "surfaced fissures"),
    ("esther-dyson", "suffer"),
    ("ramon-alvarado", "make them feral"),
    ("david-weinberger", "degrade the loop"),
    ("james-evans", "benefit from human grounding"),
    ("peter-pomerantsev", "censorship through noise"),
    ("anil-dash", "majority AI view"),
    ("brent-hecht", "Grand Bargain"),
    ("kenneth-cukier", "not about intelligence and not artificial"),
    ("alex-springer", "free raw material"),
    ("tamar-gendler", "brain is like chatGPT"),
    ("adam-bly", "audit-trail"),
    ("kara-miller", "hard to read long"),
] + [tuple(a.split("|", 1)) for a in sys.argv[1:]]

for slug, q in CHECKS:
    hits = []
    for p in (ROOT / slug).rglob("*"):
        if p.is_file() and p.suffix in (".md", ".jsonl", ".tsv"):
            try:
                if q.lower() in p.read_text(errors="ignore").lower():
                    hits.append(str(p.relative_to(ROOT)))
            except Exception:
                pass
    print(f"{'OK ' if hits else 'MISS'} {slug:24} {q[:40]:40} {hits[:2]}")
