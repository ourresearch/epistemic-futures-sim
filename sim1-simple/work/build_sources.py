"""Build sources.md from the position cards' key-file sections plus extra files cited in the manifesto/process notes."""
import pathlib, re

DOSS = pathlib.Path("/Users/jasonpriem/ox/epistemic-futures-corpus/dossiers")
CARDS = pathlib.Path("/Users/jasonpriem/ox/epistemic-futures-sim/sim1-simple/work/cards")
OUT = pathlib.Path("/Users/jasonpriem/ox/epistemic-futures-sim/sim1-simple/sources.md")

roster = [l.split("`")[1] for l in (DOSS / "00-roster.md").read_text().splitlines()
          if l.startswith("| ") and "`" in l and "/INDEX.md" in l]
names = {}
for l in (DOSS / "00-roster.md").read_text().splitlines():
    m = re.match(r"\| ([^|]+) \| \[`([a-z-]+)`\]", l)
    if m:
        names[m.group(2)] = m.group(1).strip()

EXTRA = {
    "nick-vincent": ["nick-vincent/by/2026--the-paradox-of-reuse-in-2026-a-case.md"],
    "esther-dyson": ["esther-dyson/by/2026--substack-know-your-agent.md"],
    "benjamin-bratton": ["benjamin-bratton/by/2025--a-philosophy-of-planetary-computation-long-now.md"],
}

path_re = re.compile(r"`?([a-z-]+/(?:by|av|social)/[^`\s)]+\.(?:md|jsonl))`?")
out = ["# Sources", "",
       "Corpus files this simulation relied on, grouped by attendee. Paths are relative to `dossiers/`, except the summit website files, which are relative to the corpus root.",
       "Each path was checked to exist on disk. Files are listed roughly by how much weight they carried (most important first); the per-attendee position cards in `work/cards/` give the quotes taken from each.", "",
       "## Summit framing (corpus root)", "",
       "- `summit/website/concept-note.md`", "- `summit/website/schedule.md`", "- `summit/website/attendees.md`", "- `summit/website/home.md`", "- `dossiers/00-roster.md`", ""]
missing = []
for slug in sorted(names, key=lambda s: names[s].split()[-1]):
    card = CARDS / f"{slug}.md"
    if not card.exists():
        continue
    text = card.read_text()
    sec = text.split("## 9.", 1)[-1] if "## 9." in text else text
    paths = []
    for m in path_re.finditer(sec):
        p = m.group(1)
        if not p.startswith(slug) and p.split("/")[0] not in names:
            p = f"{slug}/{p}"
        if p not in paths:
            paths.append(p)
    for p in EXTRA.get(slug, []):
        if p not in paths:
            paths.append(p)
    out.append(f"## {names[slug]}")
    out.append("")
    out.append(f"- `{slug}/INDEX.md`")
    for p in paths:
        if (DOSS / p).exists():
            out.append(f"- `{p}`")
        else:
            missing.append(p)
    out.append("")
OUT.write_text("\n".join(out))
print("written", OUT, "missing:", len(missing))
for m in missing:
    print("  MISSING", m)
