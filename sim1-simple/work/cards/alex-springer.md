# Position card: Alex Springer (OpenAttribution)

## 1. Role at summit and relevant bio

**Role:** One of three 7-minute talks in "What might a well-designed AI-mediated knowledge marketplace look like?" (11:45–12:30), with Tim O'Reilly and Nick Vincent, followed by discussion.

**Bio:** A London-based technologist, and the outsider in this room: he has no scholarly record and comes from about a decade in affiliate and partnership marketing technology (impact.com, most recently Senior Director of AI Strategy and Partnerships). He is founding director of **OpenAttribution Ltd** (a UK company limited by guarantee, incorporated January 2026). It publishes **AIMS**, a DID-based agent-identity manifest standard, and a commerce profile of **Content Telemetry**, and it runs PolicyCheck, a scanner for robots.txt and licensing signals. He is also **technical lead and maintainer of Content Telemetry for the SPUR Coalition** (BBC, FT, Guardian, Sky News, Telegraph, Mediahuis, later AP), co-leads the APMA AI Taskforce, and runs the NarrativAI consultancy. His public record on AI attribution begins only in December 2025, and most of it is specification text. His thinking is infrastructure-first: identity, measurement, then value return. He deliberately stays neutral on price and on how credit is allocated.

## 2. Core recent positions

- **Generative AI broke the economy of paid-for knowledge.** Human learners' inputs "were paid for," but AI is "ingesting the sum of human experience without upholding the social or financial contract." "Generative AI has broken this economy." (`alex-springer/by/2025--borrowed-knowledge.md`, 2025)
- **Free ingestion leads to model collapse and creators leaving.** "By treating human creativity as a free raw material, we are not just cheating creators; we are sprinting toward an intellectual heat death — a closed loop where the internet feeds on its own exhaust." (same file, 2025)
- **Missing attribution is a choice, not a technical limit.** RAG proves that systems can cite. "This is a choice, not a technical limitation." (same file, 2025)
- **The precedent is a compulsory licence, not a ban.** He points to the 1908 piano-roll case and the statutory licence that followed. "We are in the 1908 moment again, but this time we are letting the machine ingest the entire internet for free." (same file, 2025)
- **AI is not search. Three things are missing: identity, measurement and value return.** "Without measurement, attribution is impossible." He frames this as sustaining supply: "This is not a philosophical position — it is a market sustainability question." (`alex-springer/by/2026--ai-is-not-search.md`, 2026)
- **A deterministic vocabulary of events should replace probabilistic "visibility" guesswork.** The events are retrieved, grounded, reproduced, cited, presented and engaged. Retrieval can be measured from a publisher's own CDN logs today. The rest requires AI providers to report (`alex-springer/by/2026--measuring-content-influence-in-ai-assistants.md`, 2026). His May 2026 audit of 24,127 citations found that 7.8% came from domains blocking the provider's training bot. The figure was 2.1% when checked against the live-search bot, and he calls that difference the "bot-taxonomy gap."
- **Every licence should require event-level reporting.** "A licence without an event-level reporting clause is incomplete." (same file, 2026)
- **Neutral measurement.** "The measurement currency that decides what counts should not be set by the parties that take a margin on the count." (same file, 2026). Also: "platform self-reporting is insufficient" (`alex-springer/by/2026--cma-consultation-responses.md`, 2026).
- **Training and grounding need separate controls.** "Training is effectively permanent… Grounding is per-query and revocable." Robots.txt "is not fit for purpose as a licensing tool." (`2026--cma-consultation-responses.md`, 2026)
- **The standard carries signals, not prices.** "Telemetry does not determine ownership, permission, price or compensation." (`alex-springer/by/2026--content-telemetry-scope.md`, 2026). In a webinar he said: "I'm very explicitly not trying to advocate for a specific like attribution methodology. I wanna get the signals out." (`alex-springer/av/2026--open-attribution-the-fix-for-the-zero-click-era.md`, 2026, ASR transcript)
- **Citing sources is a general norm of knowledge work that AI should follow.** "Showing your work and citing your sources have always been the second most important thing in knowledge work… AI systems shouldn't be the exception." (`alex-springer/by/2026--linkedin-posts-partial-capture.md`, 2026)
- **Work with the platforms, but keep control.** "We need to be doing that in collaboration with AI platforms, not in opposition to them." At the same time, content owners should license "through their own agents rather than just showing up in someone else's agents and hoping they say nice things about us." (`alex-springer/by/2026--apma-the-future-of-ai-two-experts.md`, 2026)

## 3. Relation to the concept note

- **Strongly endorses** the anti-anthropomorphism paragraph ("We say a model 'knows,' 'understands'…"). His own essay says: "We use anthropomorphic language to cement this. Models are 'trained.' They 'learn.'" (`2025--borrowed-knowledge.md`). In a webinar: "they're not smart. They don't think… they don't know anything… It's a messy distribution channel as opposed to an intelligent entity" (`av/2026--open-attribution-...md`). He would likely support the note's "shared vocabulary" deliverable.
- **Endorses** "treating decades of accumulated human judgment as a free input." It is nearly his thesis word for word ("treating human creativity as a free raw material").
- **Endorses** the model-collapse passage ("photocopy of a photocopy") through his "heat death… internet feeds on its own exhaust" line.
- **Endorses** the hype and marketing critique. He wrote that the "strangers" of ChatGPT "are backed by billions of advertising dollars" and "trained by psychologists recruited from addictive technologies" (`2025--borrowed-knowledge.md`). He also attacks the GEO industry's unverifiable metrics as "marketing rather than measurement."
- **Endorses, but narrows,** "who pays… how that labor gets recognized and rewarded." He supplies the measurement layer and deliberately leaves out the pricing. He would say fair compensation is impossible to negotiate without event records.
- **Reframes** the "ultimate annotators" idea in commercial terms. For him the valuable good is *influence on outcomes* ("the value of the content is influence"), and his "content owners" explicitly include brands' product feeds, not only publishers or scholars ("intentionally not using the word publisher"). Scholarly publishing is **absent** from his corpus. His coalition is news, affiliate and commerce.
- **Likely silent** on fluency and privilege, peer review, and cognitive atrophy. No evidence was found.

## 4. Predicted contributions

**What his 7-minute talk would argue:**
1. **A marketplace needs plumbing before prices.** Declared terms (RSL and other source-side licensing), verified agent identity (AIMS), and usage telemetry (Content Telemetry) together form "a complete chain: publishers declare terms, agents prove identity, and usage is tracked" (`2026--ai-is-not-search.md`).
2. **Current evidence shows the market is opaque and consent signals are broken.** Crawl-to-referral ratios (Anthropic 38,065:1), cited-while-blocked sources ranking near the top of answers, "citation laundering" and "content laundering," and licensing deals that invisibly override robots.txt (`2026--measuring-content-influence-in-ai-assistants.md`).
3. **The measurement layer must be neutral, open and cross-checkable.** Two independent witnesses, the agent's log and the publisher's CDN log, joined by a Content-Telemetry-ID. No self-certification, and one member one vote in governance.
4. **Collective coalitions give publishers bargaining power.** SPUR and OpenAttribution membership is "from a collective bargaining power" perspective (webinar).

**Session 5 interventions he would push:**
- **Adopt the open Content Telemetry event schema, and require event-level reporting clauses** in every AI licence or data deal that scholarly publishers or infrastructure providers sign.
- **Require separate controls for training and for grounding** (and, by implication, a crawler-separation or preference-signal standard beyond robots.txt) (`2026--cma-consultation-responses.md`).
- **Instrument now:** every scholarly publisher or repository deploys retrieval telemetry at its CDN and runs a reproducible citation-compliance audit (`2026--measuring-content-influence-in-ai-assistants.md`, §6–7).

## 5. Likely dissents he'd want recorded

- **Against baking a specific valuation or compensation formula into the standard.** He would keep measurement and price separate (`2026--content-telemetry-scope.md`; webinar).
- **Against self-reported or vendor-certified metrics** as a basis for payment (`2026--cma-consultation-responses.md`; working paper §2).
- **Against treating robots.txt or opt-out as sufficient consent** (`2026--cma-consultation-responses.md`).
- **Probably against a purely adversarial or "blocking" stance toward AI platforms.** He argues for building the market "in collaboration with AI platforms, not in opposition to them" (`2026--apma-the-future-of-ai-two-experts.md`).

## 6. Tensions and alliances with other attendees

- **Tim O'Reilly:** grounded connection. Springer's LinkedIn reports conversations at Foo Camp in July 2026 with O'Reilly and Ilan Strauss about skills (`alex-springer/by/2026--linkedin-posts-partial-capture.md`). O'Reilly's paper also calls for "standardized telemetry." Paul Farrow (Microsoft) attended both O'Reilly's Bellagio convening and Springer's OpenAttribution event. Possible friction: O'Reilly favours per-output royalty *allocation*, while Springer refuses to specify allocation.
- **Nick Vincent:** convergent. Vincent's "attestation across the AI supply chain" explicitly includes an attestation that "a certain piece of information was retrieved and used at inference time" (`nick-vincent/by/2026--attestation-across-the-ai-supply-chain.md`), which is essentially Springer's grounding and retrieval events. Both favour collective bargaining units. Vincent tracks the same preference-signal and RSL landscape.
- **Scholarly-infrastructure attendees (Bilder, Priem, Chan):** no direct engagement found. His commerce framing, with brands and affiliates treated as "content owners" and influence on purchases as the value metric, may sit uneasily with open-access advocates. This is inferred, not attested.

## 7. Distinctive vocabulary

"Borrowed knowledge"; "intellectual heat death… internet feeds on its own exhaust"; "the 1908 moment" (`2025--borrowed-knowledge.md`); "AI is not search"; "no identity, no measurement, no value return" (`2026--ai-is-not-search.md`); "deterministic vs. probabilistic measurement"; "bot-taxonomy gap"; "citation laundering / content laundering"; "brands are paying twice" (`2026--measuring-content-influence-in-ai-assistants.md`); "zero-click era"; "content owner, not publisher"; "prices on the shelves and a security guard"; "the value of the content is influence" (webinar); "show your work" (LinkedIn); "engineered… cross-aisle" coalition language.

## 8. Confidence and gaps

**High confidence** on his technical proposals, which come from specifications, a working paper and blog posts, all 2025–26. **Medium confidence** on his broader normative stance, since the long-form evidence is essentially one essay (`borrowed-knowledge`). **Gaps:** LinkedIn, his most active outlet, is only partly captured (4 posts). There is no social corpus. He has no stated views on scholarly publishing, open access, peer review, or academic incentives, so his attitude toward the scholarly record has to be extrapolated from his news and commerce work. Some commits and specs were co-drafted by a "NarrativAI Agent." One personal essay supports a compulsory licence, while his standards work stays neutral on pricing, so which position he leads with is uncertain.

## 9. Key files

1. `alex-springer/by/2025--borrowed-knowledge.md`
2. `alex-springer/by/2026--measuring-content-influence-in-ai-assistants.md`
3. `alex-springer/by/2026--ai-is-not-search.md`
4. `alex-springer/by/2026--cma-consultation-responses.md`
5. `alex-springer/av/2026--open-attribution-the-fix-for-the-zero-click-era.md`
6. `alex-springer/by/2026--open-standard-launch.md`
7. `alex-springer/by/2026--content-telemetry-scope.md`
8. `alex-springer/by/2026--linkedin-posts-partial-capture.md`
9. `alex-springer/by/2026--apma-the-future-of-ai-two-experts.md`
10. `alex-springer/by/2026--telemetry-design-considerations.md`
11. `alex-springer/by/2026--content-attribution-for-agentic-commerce.md`
12. `alex-springer/by/2026--speaker-and-bio-page.md`
