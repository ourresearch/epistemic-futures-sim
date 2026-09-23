> SIMULATED. These are the working notes behind an AI-generated prediction of the Epistemic Futures Summit's manifesto. No attendee wrote or endorsed any of it.

# Process notes

## How I got here

1. **Read the organizers' frame first.** I read the concept note, schedule, home page and attendee list in full, plus `dossiers/00-roster.md`. The concept note is opinionated and has a single voice. Its signature claims are:
   - "Artificial intelligence" is a misnomer for "a vast statistical model reflecting back the intentions" of its training authors.
   - Writing is now cheaper than reading, so effort-as-signal is broken.
   - Fluency was a privilege signal.
   - The scholarly record faces enclosure, and the labor behind it goes unpaid.
   - Human judgment is the scarce ingredient.
   - Cognitive atrophy and model collapse form a vicious circle.
   - Scholars and publishers are the "ultimate annotators".
   - AI is the opening to fix old dysfunctions.
   - "Not another cautious consensus report."
2. **One research agent per group of about three attendees (11 agents, 33 people).** Each agent read the INDEX, the most relevant `by/`, `av/` and `social/` items (2024–26 weighted), and wrote a position card to `work/cards/<slug>.md`. Each card records:
   - verbatim quotes with paths
   - relation to specific concept-note sentences
   - predicted harvest claims and interventions
   - likely dissents with evidence
   - tensions with named attendees
   - confidence

   One of those agents also wrote a separate note on who drafted the concept note (`work/cards/_concept-note-authorship.md`).
3. **Reading the cards.** I read all 33 cards and simulated the day session by session, weighting positions only by content and by how many people hold them, as instructed. No one's personality or charisma was modelled.
4. **Verifying quotes.** Every phrase that anchors a named dissent in the manifesto, and the quotes in these notes, was checked against the corpus with `work/verify_quotes.py`: about 70 phrases, all found. A few matched only after allowing for line breaks or curly apostrophes, and Banaji's "information we should ask not to have" is in Gendler's 2012 interview of her. Two phrases were fixed after checking:
   - Brand's "open to theft" line turned out to be a survey respondent she quoted, so it was removed.
   - Turkle's AI-free domains were narrowed to the ones her corpus supports.
5. **Writing the manifesto.** I wrote it as I predict the writing committee would draft it, then built `sources.md` from the cards' key-file lists. All 436 paths are checked to exist.

**Who wrote the concept note.** The authorship agent's evidence strongly suggests Geoffrey Bilder was the principal drafter, with about 65–70% confidence. The note's language section tracks his 2024 "On AI" board paper (`geoffrey-bilder/by/2024--on-ai.md`) nearly point for point: the misnomer, "parroting the intentionality," "this isn't nitpicking," the predictive-policing contrast, AI detectors, and model collapse. The compensation and human-judgment material looks like Amy Brand's, and the atrophy paragraph looks like David Krakauer's. **Blaise Agüera y Arcas, a co-convener, argues the opposite of the language section.** That is the single most important fact about the room.

**Predicted writing committee: Kenneth Cukier, Kara Miller, Geoffrey Bilder, Henry Farrell.** This is a guess, and it matters.
- Cukier and Miller: the synthesizers carry the day's frame into the draft, and both are professional writers.
- Bilder: the organizer who drafted the concept note and co-led the interventions session.
- Farrell: the Session 1 lead, a prolific writer who bridges the "cultural technology" and "pay the producers" camps.
- Plausible alternatives are David Weinberger (co-author of *The Cluetrain Manifesto*), Anil Dash, and Jason Priem (the *Altmetrics Manifesto*).

The committee shapes tone: Economist-plain, numbered, aphoristic, nonpartisan.

## Wednesday evening (predicted)

The unconference topics come from attendee suggestions after reading the concept note. I expect three rooms:
1. **"Is it intelligence?"** The vocabulary fight: Agüera y Arcas, Bratton, Salib and Priem against Bilder, Becker, Alvarado and Springer.
2. **"Who pays?"** Brand, Vincent, O'Reilly, Hecht, Deckelmann and Priem.
3. **"Slop, paper mills and peer review"** Oransky, Evans and Caulfield.

Most of the room's disagreements surface on Wednesday night. Thursday's sessions then argue about how to word them.

## Opening remarks (Agüera y Arcas, Bilder, Krakauer)

The three conveners disagree in public, and that sets permission for dissent all day.
- **Bilder** gives the concept-note frame: precise language, "context over content," and decoupling evaluation from publication (`geoffrey-bilder/by/2024--on-ai.md`).
- **Krakauer** separates complementary from competitive tools and describes "competence collapse" (`david-krakauer/by/2026--competitive-and-complementary-tools.md`). He says LLMs are "intelligent the way a calculator is."
- **Agüera y Arcas** argues that prediction *is* intelligence and that intelligence is social. He calls for "agent institutions" and names inequality, not machines, as the real risk (`blaise-aguera-y-arcas/by/2025--book-what-is-intelligence.md`, `…/2026--agentic-ai-next-intelligence-explosion.md`).

## Session 1: The Epistemic Landscape

Farrell gives the provocation. Chan, Deckelmann, Maher and Pomerantsev speak, then the room joins in.

**Predicted harvest:**
1. **Most of the "AI crisis" is an old crisis of incentives and institutions, now accelerated.** This is near-unanimous:
   - Maher: "the internet has surfaced fissures"
   - Chan: "full stack enclosure"
   - Pomerantsev: "censorship through noise" predates AI
   - Oransky and Farrell agree from the floor.
2. **Two things are genuinely new.**
   - Cheap fluent text collapses costly signals (Farrell's signalling posts; Caulfield; Vincent, "cost of polish").
   - AI answer engines disintermediate the commons that feed them. Deckelmann has the operational data on falling pageviews, volunteers and donors; Hecht's "paradox of reuse" makes the same point.
3. **The quiet risk is homogenization, not only noise.** Farrell makes the argument ("strain out" novelty), Evans's Nature 2026 paper supplies the data, and it recasts the concept note's model collapse.
4. **Political attacks on knowledge institutions belong in the landscape, not the background.** Maher speaks from NPR's defunding, Pomerantsev from US retreat, Miller from NIH cuts. Maher insists on nonpartisan wording.
5. **Unresolved: is cognitive atrophy in scope?** It is in scope, but the room splits on the frame.
   - Individual capacity: Krakauer, Turkle, Dyson, Miller, Becker.
   - Collective, institutional or agency-based: Farrell, Sloman, Pomerantsev.
   - Overstated: Weinberger, O'Reilly.
   - On moral panic, Johns's "every decade has had its crisis of literacy" and Deckelmann's "impending death of Wikipedia" both land.

## Session 2: AI as Epistemic Actor

Dyson gives the provocation. Alvarado, Evans, Salib and Turkle speak.

**Predicted harvest:**
1. **The black box that matters is the business model and the people behind it.** That is Dyson's "unexplainable humans running the companies." For the model itself, the black box is error opacity (Alvarado: "inner failings" over inner workings). Transparency should target money flows and failure modes.
2. **AI helps scientists and hurts science.** Individual gains come with collective narrowing, and verification, not generation, is the bottleneck (Evans).
3. **Accountability must run to people and organizations that can be held liable.** This comes from Dyson's Know Your Agent registry and her insurance proposal. Salib contests it with A-corps and AI rights for human safety. Alvarado and Dyson both oppose mind-based AI rights, and the room sides with them.
4. **Interface design is governance.** Turkle wants no first-person "I." Evans wants systems that provoke evaluation, not trust. Caulfield, from the floor: "no answers from nowhere."
5. **Unresolved: the capability trajectory.** Salib says "AGI-denialist" governance will be outrun. Becker and Alvarado say most misconceptions come from the hype. This becomes the vocabulary dissent in the manifesto.

## Midday: the knowledge-marketplace talks (O'Reilly, Springer, Vincent)

The three talks converge:
- There can be no market without measurement and attribution (Springer: identity → measurement → value return).
- "Pay for the output, not the training" (O'Reilly).
- Knowledge producers need collective bargaining and a commons backstop (Vincent: "quasi-enclosure," data guilds, the commons-rent tax).
- O'Reilly names Crossref, OpenAlex and Retraction Watch as infrastructure AI labs should fund.

The discussion exposes the room's sharpest substantive split: **consent versus openness.**

| Position | Who |
|---|---|
| Opt-in and consent | Brand; Hecht (consent for commercial training); Dash; Chan (refusal as a legitimate outcome); Becker |
| Pay and reciprocate, but don't gate | Deckelmann ("content being free, but the infrastructure is not"); Maher; Priem ("set the default to open," CC0); Weinberger |
| Copyright and royalties are the wrong tool entirely | Bratton ("training on my books is ripping me off feels ludicrous"); Salib ("copyright isn't… a welfare program") |

The common ground, which becomes manifesto principle 6: attribute, report use, pay for infrastructure and communities, bargain collectively, and never treat "open" as "free to strip."

## Session 3: Knowledge Infrastructure (Commons, Enclosure, Sovereignty)

Johns gives the provocation. Bly, Bratton, Priem and Weinberger speak.

**Predicted provocation (Johns):** there was never a golden age of trusted print. Credibility was built by communities that "grab [printers] by the neck," and it "could only endure with constant policing" (`adrian-johns/by/2008--when-authorship-met-authenticity.md`). The concept note's arc of "cheap signal → panic → durable institutions" is true only if you count the labor and the policing.

**Predicted harvest:**
1. **Credibility is maintained infrastructure.** Someone polices it and someone pays for it.
2. **Open, machine-readable records are the sovereignty move.** Priem: intelligence becomes swappable once data is open. Bilder: open means exit. But openness alone doesn't protect: Chan asks "who benefits from unfettered openness?", and Hecht calls "open" "a tactic, not a value."
3. **The enclosure that matters is concentration:**
   - models captured into hemispheric stacks (Bratton, who proposes open weights)
   - publisher-analytics stacks (Chan)
   - US concentration of scholarly infrastructure (Bilder)
4. **Infrastructure should carry provenance at the level of claims and findings, including retraction status.** Bly's System graph cites and is corrected for retractions via its Retraction Watch integration.
5. **Unresolved: commons versus market.** Bratton: "The Commons as Political Solutionism." Johns: rights-enforcers "may very well be right."

## Session 4: Epistemic Authority

Gendler gives the provocation. Banaji, Becker, Caulfield and Sloman speak.

**Predicted harvest:**
1. **Credibility is a property of communities and methods, not documents.** Sloman: nobody verifies alone. Banaji: methods "keep us honest." Gendler: trust networks can't be "turtles all the way down."
2. **Look for signals that are hard to fake.** Caulfield's test is "how hard would it be to fake that?"; stakes and reputation over time count. Sloman: repetition is not independent evidence, and the trappings of scholarship can be faked.
3. **Knowing a signal is cheap won't stop it feeling credible,** so design situations, not just literacy.
   - Gendler: alief, and the "G. I. Joe Fallacy."
   - Banaji: blinding, "information we should ask not to have."
   - Sloman: skepticism of deficit-model remedies.
4. **Human judgment is not a gold standard.** Humans in the loop absorb model bias, and LLM evaluators prefer their own output. Neither can be the sole arbiter (Banaji 2026).
5. **Wealth, scale and fluency are not authority** (Becker). Machines have no stakes: they can route to authority but never be it (Caulfield).

**Unresolved:** Becker ("That's all they do: hallucinate") against Caulfield ("everything is hallucination" is as wrong as "everything is true"). Can LLMs be used for verification at all?

## Session 5: Interventions and Futures

Bilder and Shaub co-lead, with Dash, Hecht and Oransky.

**The three interventions I expect the room to name:**
1. **Decouple hiring, promotion and funding from publication and citation counts.** Oransky ("flood insurance," "go way upstream"), Bilder ("the final straw"), Chan ("de-authorize rankings"), Krakauer and Evans. This is the widest coalition in the room, and it is also the concept note's "perverse incentives" point.
2. **A reciprocity compact, or "grand bargain," for the knowledge commons.**
   - Hecht: "We need a new Grand Bargain with content producers."
   - Vincent: collective bargaining.
   - Springer: event-level reporting clauses.
   - O'Reilly: labs fund Crossref, OpenAlex and Retraction Watch.
   - Deckelmann, Maher and Dash: pay Wikipedia and public media.
3. **An open provenance-and-correction layer.**
   - Bilder: context over content.
   - Oransky: bounties, fast retractions, public misconduct reports.
   - Caulfield: no answers from nowhere.
   - Evans: a negative-knowledge commons and a funded verification science.
   - Bly and Priem: open finding-level metadata.
   - Banaji: bias audits for tools used in scholarly workflows.

**Runners-up for the roadmap (6–10 items):**
- a shared glossary (Bilder, Alvarado, Becker)
- competence-before-tools education (Krakauer, Miller)
- an anti-anthropomorphic design standard (Turkle)
- Know Your Agent plus liability insurance (Dyson)
- public and open-weight models for scholarship (Vincent, Bratton, Dash)
- POSI for the AI era, with non-US redundancy (Bilder)
- a versioned bias-audit battery (Banaji)
- a "good AI" seal (Dash)
- revived technology assessment (Bly)

**Open questions:**
- Is atrophy real at population scale?
- Can automated review recognize novelty? (Farrell, Evans)
- What does "open" mean when the main reader is a machine?
- Who funds the commons after the traffic goes? (Hecht: "I need some help… on the economics front")
- What is the true misconduct rate? (Oransky: at least 2%)

**Who's missing:**
- Global South and Indigenous knowledge holders (Chan, Shaub, Maher)
- students, teachers and early-career researchers (Miller, Krakauer)
- volunteers, sleuths and maintainers (Dash, Hecht, Oransky)
- economists and labor organizers (Hecht)
- disabled people (Dash)
- funders and policymakers (Oransky, Shaub)
- faith communities (Cukier), which the manifesto leaves out

## Session 6: Closing synthesis (Cukier, Miller)

- **Cukier** frames the day as "pro-AI, pro-human." He argues human framing is the scarce input, "the training data is us," frames must "clash and tussle," and "nothing is inevitable."
- **Miller** asks "We already know X; why don't we act?" and pushes each contested item toward who implements it.
- **What emerged:** old crisis accelerated, cheap signals, reciprocity, incentives.
- **What remained contested:** what these systems are; atrophy; consent versus open; whether AI belongs in evaluation.
- **What demands action:** the three interventions.

## How the concept note's claims fared in the manifesto

| Concept-note claim | Fate | Why |
|---|---|---|
| AI didn't create the crisis; it accelerates it | **Kept, strengthened** | Near-unanimous (Maher, Chan, Pomerantsev, Oransky, Farrell, Brand, Priem) |
| "We have done this before": cheap signal → panic → durable institutions | **Kept but corrected** | Johns's history: trust in print was built and policed, never automatic. Most of the room would accept the correction, so it is absorbed rather than dissented |
| "Artificial intelligence" misnomer; "statistical model… not a knowing mind" | **Softened** to "whatever these systems are, they are made from us," plus precise-language commitments | The organizer bloc (Agüera y Arcas) plus Bratton, Salib, Priem, O'Reilly, Caulfield, Banaji, Gendler and Weinberger would not sign the flat ontological claim. The dissent is recorded |
| Writing is cheaper than reading; fluency was privilege; no AI detectors | **Kept** | Broad agreement (Bilder, Caulfield, Farrell, Vincent, Alvarado, Bratton, Banaji on dialect bias) |
| LLMs useful only where fast deterministic checks exist; science is the opposite | **Softened** to "where errors can't be caught quickly, build the checks first" | Caulfield's method manufactures checkability; Priem and Evans agree |
| Enclosure, extraction, unpaid labor, "who pays" | **Kept, made concrete** (reciprocity, collective bargaining, pay per use) | Brand, O'Reilly, Vincent, Hecht, Springer, Farrell, Deckelmann, Maher, Dash |
| Human judgment is the scarce ingredient | **Kept, qualified** ("pay for it, and structure it") | Banaji: judgment is biased and absorbs model bias. Evans: senior gatekeepers suppress disruptive work |
| Atrophy + model collapse vicious circle | **Split**: atrophy becomes "competence before reliance," with Sloman's dissent; model collapse is folded into "the quiet risk is sameness" | Farrell reframes collapse as homogenization; Sloman and Weinberger reframe atrophy |
| Scholars and publishers as "ultimate annotators" | **Broadened** to people and communities (reviewers, Wikipedians, sleuths); publishers "earn" the role by correcting the record | Deckelmann, Chan, Oransky and Hecht resist a publisher-centred version; Becker resists celebrating the annotator economy |
| Cynical opening (Bond villains, tarnished halo, forced upgrades) | **Dropped the tone, kept the target**: skepticism of business models and power, not of usefulness | Dash, Maher, Deckelmann, Cukier, O'Reilly, Caulfield, Hecht, Weinberger and Agüera y Arcas resist blanket cynicism. Becker, Turkle, Chan and Krakauer would keep it. Nonpartisan wording for Maher |
| Energy costs | **Dropped** from the manifesto (roadmap only) | Contested: Bratton and Agüera y Arcas oppose; Brand, Becker and Chan support. Not central enough to survive the word limit. This is a judgment call (see guesses) |

## Who dissented, on what, and why

| Dissenter | Principle | Grounds (corpus) |
|---|---|---|
| Blaise Agüera y Arcas | 2 (vocabulary) | Calling LLMs intelligent is "not delusional or 'anthropomorphic'" (`blaise-aguera-y-arcas/by/2025--book-what-is-intelligence.md`); rebuts Farrell et al.'s deflationism (`…/by/2026--unreasonable-effectiveness-pattern-matching.md`) |
| Benjamin Bratton | 2 (vocabulary) | "AI Denial," "Reflectionism," "you are a stochastic parrot, after all" (`benjamin-bratton/by/2024--the-five-stages-of-ai-grief.md`; `…/by/2025--after-alignment.md`) |
| Peter Salib | 2 (capabilities) | "AGI-denialist 'stochastic parrots'" (`peter-salib/social/bluesky-timeline.jsonl`, 2025-02-07); "treat AGI as an inevitability" (`…/by/2024--openais-latest-model-shows-agi-is-inevitable.md`) |
| Leslie Chan | 3 (new trust signals) | "Don't optimize for legibility — change the regime" (`leslie-chan/by/2026--rankings-as-governance-predatory-inclusion-data-intermediati.md`); DOI as compliance (`…/by/2026--will-diamond-open-access-redress-global-knowledge-inequity.md`) |
| Sherry Turkle | 5 (humans in the loop) | "humans in the loop"… "I have a different question" (`sherry-turkle/by/2025--response-on-ai-and-mental-health-care.md`); "There is no I there" (`…/av/2026--can-ai-companionship-cure-loneliness-or-deepen-it.md`) |
| David Weinberger | 5 (humans in the loop) | "humans degrade the loop"; humans "in the dialogue" (`david-weinberger/by/2026--kmworld-from-humans-in-the-loop-to-in-the-flow.md`) |
| Jason Priem | 6 (consent) | "set the default to open," "free data, paid service" (`jason-priem/by/2026--openalex-api-new-features-and-usage-based.md`); "AI evangelist" (`…/av/2026--townhall-with-ceo-jason-priem-q2-2026-april-16-2026.md`) |
| Selena Deckelmann | 6 (consent) | "we're not gonna put a pay per article blocker" (`selena-deckelmann/av/2025--wikimania-2025-ai-keynote-panel-technology-in-a-changing-wor.md`); training "within the licenses" (`…/by/2025--marketplace-tech-ai-search-vs-human-search.md`) |
| Amy Brand | 6 (goes further) | "defaulting to the opt-in model"; prefer RAG/MCP to pre-training (`amy-brand/by/2025--sk-who-controls-knowledge-in-the-age-of-ai-part-2.md`) |
| Benjamin Bratton | 6 (copyright tool) | "training on my books is ripping me off feels ludicrous"; AI sovereign wealth fund (`benjamin-bratton/social/x-timeline.jsonl`, 2026-06-01/02) |
| Steven Sloman | 9 (atrophy) | "Ignorance is our natural state" (`steven-sloman/by/2017--why-we-believe-obvious-untruths.md`); automation paradox (`…/by/2017--the-perils-of-letting-machines-into-the-hive-mind.md`); "We're not repositories of information" (`…/by/2025--securetalk-why-security-leaders-struggle-with-security-culture.md`) |
| Adam Becker | 10 (build with LLMs) | "fruit of the poisoned tree… ethically indefensible" (`adam-becker/social/bluesky-timeline.jsonl`, 2025-05-21); "despite all evidence to the contrary" (`…/by/2025--guardian-tech-oligarchs-gambling-our-future.md`) |
| Peter Salib | 10 (accountability) | A-corp, "not a master key but a leash" (`peter-salib/by/2026--why-law-needs-a-new-entity-to-govern-ai-agents.md`); `…/by/2026--ai-rights-for-human-safety.md` |

**Dissents I considered and folded into the text instead:**
- **Johns** on the historical arc: absorbed into principle 1.
- **Banaji** on human judgment and "mirror vs amplifier": absorbed into principle 4.
- **Caulfield** on deterministic checks: absorbed into principle 8.
- **Pomerantsev** on facts not being enough: absorbed into principle 4 ("belonging and agency").
- **Maher**'s nonpartisan wording and anti-paywall stance: absorbed into principles 1 and 6.
- **Dash** against "no LLMs" and scolding: absorbed into principle 10.
- **Dyson** against AI personhood: this *is* principle 10's accountability line.
- **Krakauer** would want stronger atrophy language: principle 9 is his.
- **Evans** would want amendments rather than dissent.
- **Alvarado** would want "epistemic technology" in place of "AI" and would resist "use or refuse." He gets the glossary.
- **O'Reilly** and **Cukier** would resist the cynical tone, which was dropped.

**Other dissents that are plausible but not recorded:**
- **Weinberger** on consent: he is anti-copyright-maximalist, but the evidence is older (`david-weinberger/by/2013--kmworld-the-failure-to-attribute.md`).
- **Salib** on copyright: principle 6 already carries Bratton's version, and one Salib note per principle seemed the more likely committee edit.
- **Vincent and Hecht** on "open is a tactic, not a value."
- **Bly** on AI extraction as enclosure in itself.

**No dissent expected** from Shaub, Miller, Cukier, Bilder, Krakauer (conveners and synthesizers), Bly, Springer, Oransky, Dyson, Evans, Gendler, Maher or Pomerantsev.

## Corpus items that carried the most weight

- `geoffrey-bilder/by/2024--on-ai.md`: the likely source text of the concept note's language section, and of "context over content."
- `blaise-aguera-y-arcas/by/2025--book-what-is-intelligence.md` and `…/by/2026--unreasonable-effectiveness-pattern-matching.md`: they establish that a convener rejects the note's framing.
- `benjamin-bratton/by/2024--the-five-stages-of-ai-grief.md` and `…/by/2025--after-alignment.md`: the sharpest anti-deflationary voice.
- `henry-farrell/by/2025--large-ai-models-are-cultural-and-social-technologies.md` and `…/by/2024--pm-the-map-is-eating-the-territory-the-political-economy-o.md`: "obligate complement," pay the producers, and homogenization.
- `james-evans/by/2026--artificial-intelligence-tools-expand-scientists-impact-but-contract-sciences.md` and `…/by/2026--contemporary-ai-lacks-the-imagination-to-diverge-or-negate.md`: the empirical spine of principle 8.
- `amy-brand/by/2025--sk-who-controls-knowledge-in-the-age-of-ai-part-2.md`: the opt-in position.
- `jason-priem/by/2026--openalex-api-new-features-and-usage-based.md`: the default-open position.
- `selena-deckelmann/av/2025--wikimania-2025-ai-keynote-panel-technology-in-a-changing-wor.md`: content free, infrastructure paid; no paywalls.
- `brent-hecht/by/2024--can-wikipedia-come-to-ais-rescue-again-keynote-slides.md`: the grand bargain, and the paradox of reuse.
- `nick-vincent/by/2026--the-paradox-of-reuse-in-2026-a-case.md` and `…/by/2025--collective-bargaining-in-the-information-economy-can-address.md`: "quasi-enclosure" and collective bargaining.
- `tim-oreilly/by/2024--radar-how-to-fix-ais-original-sin.md` and `…/by/2026--asimov-the-collaborative-exoskeleton-of.md`: pay for output, not training; fund the scholarly infrastructure.
- `ivan-oransky/by/2025--brownpoliticalreview-lifting-the-veil-interview.md` and `…/social/x-timeline.jsonl`: incentives, not AI.
- `mike-caulfield/by/2025--atlantic-ai-is-not-your-friend.md` and `…/by/2026--substack-publishing-brain-limits-peoples-understanding.md`: "no answers from nowhere."
- `mahzarin-banaji/by/2026--language-models-embody-amplify-human-cognitive-distortions-what-done.md`: "not merely a mirror, but an amplifier," and humans absorbing model bias.
- `steven-sloman/by/2017--the-perils-of-letting-machines-into-the-hive-mind.md`: the atrophy dissent.
- `david-krakauer/by/2026--competitive-and-complementary-tools.md`: "competence before reliance."
- `adrian-johns/by/2008--when-authorship-met-authenticity.md` and `…/by/2011--ahr-conversation-circulation-of-information.md`: the correction to the historical arc.
- `esther-dyson/by/2026--substack-know-your-agent.md`: accountability to humans.
- `leslie-chan/by/2026--rankings-as-governance-predatory-inclusion-data-intermediati.md`: compliance regimes.

## Where I was guessing

- **The writing committee's membership.** This is the biggest lever on tone. A committee including Brand or Becker would keep more of the concept note's edge. One including Weinberger or Priem would be sunnier and more pro-open.
- **Whether a convener files a written dissent.** Agüera y Arcas's position is well documented. Whether a host would put his name to a dissent, rather than just soften the text, is a social question the corpus can't answer. I recorded it because the instruction rules out modelling deference.
- **Consent versus open.** My count gives "reciprocity without individual opt-in" a majority. I predicted the committee would split the difference with "a collective say," which leaves both sides dissenting. A different committee could land on either side.
- **Energy.** Dropping the energy paragraph is a judgment about word budget and contestedness. It could easily survive as one sentence.
- **Thin corpora:**
  - **Tui Shaub:** six items, none on AI; she is played purely as process.
  - **Kara Miller:** almost no first-person AI opinion.
  - **Adam Bly:** thin since 2023.
  - **Tamar Gendler:** her AI talks are untranscribed.
  - **Alex Springer:** no scholarly writing.
  - **Brent Hecht:** nothing after 2024 in the corpus.
  - **Pomerantsev, Maher, Dyson, Turkle and Salib:** nothing on scholarly publishing.
- **Positions inferred, not stated:**
  - Chan on "annotators."
  - Priem and Farrell on atrophy.
  - Weinberger on consent.
  - Cukier's and Miller's framing of the synthesis.
- **Session assignments.** The roster says Chan is in S4, but the schedule puts him in S1; I followed the schedule. Gendler's and Johns's "lead" roles come from list order and the roster, not from labels on the page.
- **Data problems the agents found:**
  - `david-krakauer/av/2025--maintaining-human-intelligence-in-the-ai-era.md` is a different speaker.
  - `tui-shaub/av/2020--gene-editing-are-humans-playing-god.md` is Alta Charo speaking.
  - Evans's July 2026 Noema essay is filed as `james-evans/by/2022--what-humanity-needs-to-flourish-in-the-next-decade.md`.

  None of these was used as evidence of the named person's views.

## What I predict this simulation gets wrong

The real manifesto will probably be both blander and stranger than this one.

**Blander**, because a four-person committee circulating a draft to 33 people usually sands off named dissents. I expect fewer dissents (perhaps three to five), more of them anonymized ("some participants argued…"), and at least one convener-level disagreement quietly settled in the wording rather than recorded.

**Stranger**, because the day's real texture will come from things no corpus captures: the Wednesday unconference topics, one vivid anecdote or phrase that takes over the room, and whoever volunteers to hold the pen. My version is too tidy. Each session produces its "own" principle, and the argument follows the corpus's best-documented fault lines: intelligence versus statistics, consent versus open, individual versus collective atrophy. Those make good research-card material but may not be what the room actually fought about. I expect the real text to underweight Session 2's governance material and the marketplace mechanisms, and to overweight a few memorable slogans. I also expect it to carry more of the concept note's original wording than I kept, because the likely principal drafter of that note is on the committee and sets the defaults everyone else edits against. And I may be wrong that energy and political attacks recede, and that "competence before reliance" survives Sloman's objection.
