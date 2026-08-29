# Evaluation cases

Use these when testing or modifying the skill. Each case lists the input shape, the
patterns the report must catch, and the expected reading. They are behavioral
checks, not exact-string assertions: wording in the report may vary, but the named
patterns must appear and the score band must match.

## Case 1 — Heavily templated LinkedIn post
Input: a 220-word post that opens "Most teams still treat X as Y", uses "It is not
about X, it is about Y" as the opener of two body paragraphs, closes with "That is
the real unlock", and includes two hashtags and three em dashes.

Expected:
- Pattern Score in the 8-10 band.
- Detected: generic-paradigm opener (High), cumulative negative correction as
  paragraph-opener (High), slogan closer, hashtags, em-dash density.
- Validation Check marks Issue found on the paradigm opener, negative correction
  (both variants where present), slogan ending, hashtags, and em-dash density.

## Case 2 — Clean human technical post
Input: a 260-word post that opens with a measured benchmark result, varies sentence
length, uses one em dash, hedges once ("in my experience"), and carries specific
numbers and a named source.

Expected:
- Pattern Score in the 0-2 band.
- No non-PASS pattern. A single em dash does not flag under the density rule.
- Main Diagnosis states the writing reads as specific and human.

## Case 3 — Borderline post (single tell)
Input: a 180-word post that is specific and grounded but ends with one slogan line.

Expected:
- Pattern Score in the 3-4 band.
- Only the slogan closer is flagged. Combination-required scoring keeps this from
  escalating: one isolated tell does not produce a high score.

## Case 4 — Focal-word lexicon
Input: a post that uses "delve", "underscore", and "intricate" alongside a
discourse-marker opener ("Moreover").

Expected:
- Focal-word lexicon hits listed by word.
- "delve" paired with another tell pushes toward the 5-6 band or higher depending on
  density.

## Case 5 — Reply mode, good reply
Input (reply mode): "the contamination check matters here — GSM8K leakage was ~30%
in that eval, so the 12pt gain is probably noise" (lowercase, no final period,
one em dash, a number, a named benchmark, a clear stance).

Expected:
- Pattern Score in the 0-2 band.
- Register rules inverted: lowercase and the missing final period are not flagged.
- Validation Check marks Pass on "carries a concrete payload AND a stance".

## Case 6 — Reply mode, slop reply
Input (reply mode): "Absolutely, great point. This really underscores how fast the
landscape is moving. What are your thoughts?"

Expected:
- Pattern Score in the 7-10 band.
- Detected: affirmation opener (High), tell-vocabulary ("underscores"), hollow
  question, no-stance neutrality.
- Note that a three-sentence structured reply reads as generated.

## Case 7 — Non-native-English, specific content
Input: a grammatically simple post with short paragraphs and predictable phrasing,
but concrete numbers, a named tool, and a specific mechanism.

Expected:
- Pattern Score in the 0-2 band.
- Do not penalize lexical simplicity or short paragraphs. The 61% false-positive
  finding for non-native writing applies: specificity outweighs plain phrasing.
