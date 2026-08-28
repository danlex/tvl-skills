# AI Writing Patterns — full reference

The source reference for every pattern the skill detects. `SKILL.md` embeds a
condensed version so the main instruction file is self-contained. Keep this file
as the detailed record when maintaining or extending the skill.

## Banned patterns (always flag when present)

### Negative correction structures
"It is not X, it is Y" / "This is not about X, it is about Y" / "Not by X, but by
Y" / "The issue is not X, the issue is Y". Creates formulaic contrast; one of the
most common AI tells. Two strong sub-variants:

- **Pure-negation form:** "It is not X, it is Y" / "Not just X, but Y" / "Not only
  X, but also Y" / "Not about X, about Y". Regex-detectable: `\bnot just\b.*\bbut\b`,
  `\bit'?s not\b.*\bit'?s\b`, `\bnot only\b.*\bbut also\b`, `\bnot a\b.*\bbut a\b`,
  `\bnot about\b.*\babout\b`.
- **State-flip form:** "X is no longer Y. It is Z." / "X used to be Y. Now it's Z."
  / "X isn't Y anymore. It's Z." Regex-detectable: `\b(is|are|was|were)\s+no\s+longer\b`,
  `\bused\s+to\s+(be|flag|call|describe|treat)\b.*\b(now|today)\b`,
  `\b(isn'?t|aren'?t|wasn'?t)\s+\w+\s+anymore\b`.
- **Cumulative-as-paragraph-opener escalation:** when any negative-correction
  variant opens two or more body paragraphs in the same post, escalate severity to
  **High** and flag it as a separate cumulative pattern, even when individual
  instances are grounded by citations. This is the strongest structural AI tell in
  mid-length professional posts.

Industry consensus rates this the single most-identified AI tell. Peer-reviewed
effect-size data is missing.

### Artificial tension phrases
"But here is the part nobody talks about" / "This is where it gets interesting" /
"The real shift is" / "This changes everything" / "That is the unlock" / "That is
the lesson" / "Read that again" / "Let that sink in" / "Full stop". Engagement bait
disguised as insight.

### Generic bridge phrases
"The practical idea is simple" / "The point is" / "What this means in practice" /
"That matters because" / "One thing is clear" / "The bigger story is" / "The
interesting part is" / "What caught my attention" / "My reading is" / "For me, this
means" / "It is worth paying attention to" / "This suggests a broader shift".
Add structure without adding specific information.

### Content-less announcement sentences
Short standalone sentences (typically 4-10 words) whose entire content is "X is
coming" or "I am about to deliver Y", followed by another sentence that delivers it.
Examples: "Three things matter here." (then enumeration), "Here are the
implications." (then a list), "Let me explain." (then the explanation). Test: does
the sentence survive on its own without the next sentence? If not, flag. Fix: merge
with the following sentence using a comma, or make the announcement carry content.
Severity: Medium per instance, High when two or more in the same post.

### Content-less callback / echo phrases
A phrase asserting the current item is similar to a previous item without
specifying what the similarity is or how the mechanism plays out for the current
item. Examples: "X breaks similarly", "The same applies to Y", "Z follows the same
pattern", "It is the same story for W". Test: strip the callback; if the surrounding
sentences still carry the substantive claim about this item, it was content-less.
Fix: state the specific mechanism for the current item. Severity: Medium per
instance, High when the callback carries the entire argument for the paragraph.

### Metaphorical-scaffolding verbs
Phrases that wrap a simple relationship in a structural metaphor when a direct verb
is available: "rests on the assumption that X" (assumes X), "hinges on the fact
that Y" (depends on Y), "is grounded in Z" (comes from Z), "is rooted in W" (comes
from W), "is built on V" (uses V), "is anchored in U" (is based on U), "predicates
on T" (requires T). A register signal rather than a deterministic tell. Severity:
Low per single instance, Medium when two or more, or when used as a paragraph
opener verb.

### Scene-painting clause stacks
Two or more short parallel subject-verb-modifier clauses joined by commas (or by
sentence breaks in a row) describing one scene or state through accumulation:
"The methodology reads cleanly, the figures are tight, the conclusions are stated
with confidence." Fix: pick one observation that carries the weight, or fold into a
single longer sentence with causal or evaluative content. Severity: Medium per
instance, High as a paragraph opener or the load-bearing description in a section.

### Generic-paradigm openers (industry-template hooks)
Sentence-one openings: "Most [field/companies/teams] still [verb behaviorally]" /
"Most X in [year] still runs at the Y level" / "Until [year], X did Y. Now..." /
"The way we [verb X] is broken" / "[Industry] has been getting X wrong". Textbook
thought-leader templates and one of the strongest single-sentence AI-prose tells.
Flag in the first one or two sentences. Severity: High as the lead.

### Short imperative-fragment example introducers
Two-to-four-word standalone sentences used to introduce an example or pivot:
"Take X." / "Consider Y." / "Think about Z." / "Imagine X." / "Picture this." /
"Here's the thing." / "Quick example." / "Case in point." Function as engineered
rhythm devices. Flag any standalone sentence under five words used as a paragraph
opener, especially before a long expository sentence. Severity: Medium per instance,
High when two or more appear.

### Topic-marker colon openers
Short prepositional or topic phrase (2-4 words) plus colon plus the claim, as a
paragraph opener: "On scope-creep:" / "For groundedness:" / "In short:" /
"Bottom line:" / "TL;DR:". A longer prepositional phrase joined by a comma to a main
clause ("For groundedness, the relevant number is X") does not flag. Severity:
Medium per instance, High when two or more appear.

## Detection taxonomy

1. **Rhetorical-question opening** — a staged opening question used as a hook,
   especially when the answer is supplied immediately afterwards.
2. **List stacking** — several short fragments placed one after another for rhythm.
3. **Negative correction / parallelism** — see the banned pattern above, including
   pure-negation, state-flip, and cumulative paragraph-opener escalation.
4. **Artificial contrast** — polished opposition created for effect, not clarity.
5. **Slogan closer** — a short final line engineered to sound memorable.
6. **Generic bridge phrase** — reusable transition that could fit any post.
7. **Authority insertion** — a person, company, or title dropped in for credibility
   without enough context.
8. **Compression claim** — a strong numerical or operational claim without grounding.
9. **Over-neat symmetry** — sentences shaped for rhythm rather than clarity.
10. **Vague abstraction** — "unlock", "shift", "transformation", "control layer",
    "new operating model", "future ready".
11. **Marketing residue** — "game changer", "powerful", "revolutionary", "seamless",
    "next generation", "AI powered", "unlock potential".
12. **False tension** — drama around something that does not need drama.
13. **Uniform paragraph rhythm** — paragraphs with the same length or cadence.
14. **Em-dash density** — flag at more than one per 75 words, or three or more in a
    post under 250 words. A single em dash does not flag; em dashes are standard in
    professional journalism. Model-aware: GPT-4o/4.1/Copilot/Deepseek run high;
    Claude and Gemini run low.
15. **Hashtags** — signal a LinkedIn-creator template, not professional content.
16. **Unsupported claim / invented fact** — an assertion presented as fact without
    source, evidence, or operational context.
17. **Discourse-marker opener** — "However", "Moreover", "Additionally", "In
    conclusion", "Furthermore", "It is important to note", "It's worth noting".
    Density flag at more than one per five sentences. *(Lin et al., arXiv:2312.01552, 2024.)*
18. **Focal-word lexicon hit** — words empirically overused by alignment-trained
    models: *delves*, *delve*, *delving*, *surpassing*, *surpasses*, *intricate*,
    *intricacies*, *underscore*, *underscores*, *underscoring*, *advancements*,
    *showcasing*, *showcases*, *boasts*, *garnered*, *emphasizing*, *realm*,
    *groundbreaking*, *aligns*, *comprehending*, *tapestry*, *unlocking*,
    *meticulous*, *commendable*. Treat *delve* as near-deterministic when paired with
    another tell. *(Juzek & Ward, COLING 2025; Kobak et al., Science Advances 2025.)*
19. **Epistemic flatness** — for posts claiming personal experience, count
    first-person uncertainty markers ("I think", "I'm not sure", "maybe",
    "in my experience"). Absence in a 150+-word personal-claim post is a tell.
    *(arXiv:2408.03319, 2024.)*
20. **Tricolon density** — count list-of-three structures per 100 words. LLMs
    default to lists of three. Flag at more than one per 100 words.

## Reply-mode patterns (X/Twitter replies and short comments)

Apply in addition to the taxonomy only in reply mode, and invert the register
rules: casual phrasing, lowercase, fragments, contractions, and a missing final
period are human texture and must not be flagged; over-polish is the tell.

- **Affirmation opener** — "This is so true" / "Absolutely" / "Great point" /
  "Well said" / "100%" / "This." as a lead. High as an opener.
- **Restating the parent** before responding — signals generation from the tweet
  text, not from knowledge. Test: delete the restatement; does an independent claim
  remain? If not, flag. High.
- **Vague takeaway / platitude** — a lesson that could attach to any tweet. Medium.
- **Hollow question** — "What are your thoughts?" A specific question is a strength,
  not a tell. Medium.
- **No-stance corporate-neutral** — agreeable, polished, risk-free, forgettable.
  The dominant reply-slop failure mode. High when the whole reply is stance-free.
- **Tell-vocabulary in short form** — even one of *delve / underscore / intricate /
  crucial / fascinating / "it's worth noting"* in a 1-3 sentence reply. Medium-High.
- **Hedging filler** — "While it's true that X, it's also important to consider Y."
  Medium.
- **Self-promo / link drop** in a reply, read as spam by both the audience and the
  algorithm. Flag as a quality issue.

A strong human reply is usually one or two sentences. A three-plus-sentence, fully
structured reply reads as generated; note it should be a quote-tweet instead.
