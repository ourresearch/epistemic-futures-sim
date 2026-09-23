"""The summit's published schedule (summit/website/schedule.md, captured 2026-08-15), as the turn-taking skeleton.
Session descriptions are verbatim from the page. People are in the page's order; the page does not label leads,
so the first name in each session is treated as the lead (the design's assumption, recorded in RUN.md)."""

UNCONFERENCE_TOPICS = [
    # Titles only, copied from the organizers' sign-up sheet as of 2026-08-23 (proposer names omitted).
    "Cognitive atrophy: real phenomenon or not?",
    "Who pays, and who gets paid?",
    "When books can converse (books with an AI model including the author's other writings, with permission)",
    "The role of knowledge in the age of LLMs",
    "AI and the Reproduction of Epistemic Worlds (citation justice, whose genealogies)",
]

OPENING = {
    "id": "opening",
    "title": "Why are we all here?",
    "description": "Opening remarks and brief introductions around the room. Conveners set the arc of the day.",
    "people": ["blaise-aguera-y-arcas", "geoffrey-bilder", "david-krakauer"],
}

SESSIONS = [
    {"id": "s1", "title": "Session 1: The Epistemic Landscape",
     "description": ("We need a shared diagnosis to start. How is AI impacting knowledge production, and what was already "
                     "breaking before AI? How can we distinguish among genuine AI-driven disruption, pre-existing structural "
                     "failures accelerating under new pressure, and moral panic? We'll also ask whether cognitive surrender and "
                     "atrophy belong in scope. The goal: a clear-eyed diagnosis that resists both complacency and techno-doom."),
     "people": ["henry-farrell", "leslie-chan", "selena-deckelmann", "katherine-maher", "peter-pomerantsev"]},
    {"id": "s2", "title": "Session 2: AI as Epistemic Actor: Risks, Capabilities, and Governance",
     "description": ("AI increasingly produces, synthesizes, and mediates knowledge, opening opportunities alongside risks. What "
                     "does this shift mean for veracity, trust, and human cognition? This session examines the forces that will "
                     "decide whether AI strengthens or erodes our knowledge systems: power, incentives, the concentration of "
                     "epistemic infrastructure, and the black-box problem. The goal: a governance vision that harnesses AI's "
                     "potential while keeping trust and transparency intact."),
     "people": ["esther-dyson", "ramon-alvarado", "james-evans", "peter-salib", "sherry-turkle"]},
    {"id": "marketplace", "title": "What might a well-designed AI-mediated knowledge marketplace look like?",
     "description": "Three 7-minute talks, followed by discussion.",
     "people": ["tim-oreilly", "alex-springer", "nick-vincent"], "format": "talks", "floor_turns": 12},
    {"id": "s3", "title": "Session 3: Knowledge Infrastructure and Tools: Commons, Enclosure, and Sovereignty",
     "description": ("The datasets, corpora, and scholarly record that underpin human knowledge face new extractive pressures. "
                     "How do we safeguard this infrastructure for the future? This session explores questions of ownership, "
                     "access, and sovereignty, with an eye toward building durable foundations that serve the public good."),
     "people": ["adrian-johns", "adam-bly", "benjamin-bratton", "jason-priem", "david-weinberger"]},
    {"id": "s4", "title": "Session 4: Epistemic Authority — Credibility in an Age of Infinite Scale",
     "description": ("When knowledge production can be scaled infinitely, what gives a claim credibility? This session examines "
                     "the evolving nature of scholarly authority: the role of credentials and institutions, and how we "
                     "distinguish earned authority from mere gatekeeping. The goal is a renewed model of trust."),
     "people": ["tamar-gendler", "mahzarin-banaji", "adam-becker", "mike-caulfield", "steven-sloman"]},
    {"id": "s5", "title": "Session 5: Interventions and Futures",
     "description": ("What do we need to do next and what should go into the summit outputs? (1) What are the three most "
                     "important interventions we can name? (2) What are the open questions we can't yet answer? (3) Who isn't "
                     "in this room who needs to be in the next EFS convening?"),
     "people": ["geoffrey-bilder", "tui-shaub", "anil-dash", "brent-hecht", "ivan-oransky"], "format": "interventions"},
    {"id": "s6", "title": "Session 6: Closing Synthesis",
     "description": ("Sensemaker synthesis: 15-20 min. integration of the day: what emerged, what remains contested, what "
                     "demands action. Followed by open floor for any input from the group."),
     "people": ["kenneth-cukier", "kara-miller"], "format": "synthesis", "floor_turns": 12},
]

SESSION_FORMAT = ("Each session consists of a short provocation (5–10 min), followed by a moderated roundtable (45 min), "
                  "and harvest of key takeaways (5 min): capture 3–5 key claims, takeaways, or unresolved questions.")

# The concept note's own arguments, for grounding session leads' provocations (the organizers pre-published them).
CONCEPT_NOTE_FOR = {
    "s1": ["What was broken, what was breaking, and what threatens to break?", "Why is it so hard to think clearly about AI?",
           "Why is it so hard to talk clearly about AI?"],
    "s2": ["Why is it so hard to talk clearly about AI?", "What will the Summit work through?"],
    "s3": ["What will the Summit work through?"],
    "s4": ["What will the Summit work through?"],
    "s5": ["Where this leads"],
    "s6": ["Where this leads"],
    "opening": ["What was broken, what was breaking, and what threatens to break?", "Where this leads"],
    "marketplace": ["What will the Summit work through?"],
}
