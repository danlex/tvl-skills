# Calibration notes and research basis

Derived from 2023-2026 AI-detection literature. These thresholds keep the skill
from flagging normal human style as AI. Read them before changing any severity.

## Combination-required scoring
Single instances of any pattern are unreliable. Penalize combination and density,
not isolated occurrences. A post with one em dash or one tricolon may be a
stylistic choice; the same post with three em dashes, two tricolons, and a slogan
closer in 200 words is statistically AI-typical. Require at least two distinct tell
categories before a non-PASS verdict.

## Length gate
Below about 50 words, even state-of-the-art commercial detectors degrade severely.
Be conservative on short posts: require at least two converging strong tells before
flagging anything as a real problem.

## Density, not presence
- Em dashes flag at more than one per 75 words, or three or more in a post under
  250 words.
- Discourse-marker openers flag at more than one per five sentences.
- Tricolons flag at more than one per 100 words.

The literature is consistent: single-instance signals are noise; cluster signals
are signal.

## Reply mode
For X replies the register rules invert: casual, lowercase, fragmentary phrasing is
human and must not be penalized; over-polish is the tell. Below about 50 words the
structural detectors are weak, so the decisive test is simpler — does the reply
carry a concrete payload and take a stance? If both are true, with no
affirmation/restate/takeaway/hollow-question opener, it passes even when short.

## Non-native-English overlap
Stanford research (Liang et al. 2023, *Patterns*) found a 61% false-positive rate
when AI detectors are applied to non-native-English writing. Do not penalize:
lexical density on its own; short-paragraph styles common across writing traditions;
predictable phrasing, as long as the content is specific.

## Lexicon decays
The focal-word list has a 6-12-month half-life. Liang et al. (Nature Human
Behaviour 2025) showed *delve* and *intricate* frequencies dropped after public
awareness in 2024. Flag current uses but expect the list to age out.

## Key sources
- Lin et al., arXiv:2312.01552, 2024 — discourse-marker clustering in
  alignment-trained output.
- Juzek & Ward, COLING 2025 — focal-word overuse lexicon.
- Kobak et al., Science Advances 2025 — excess word frequency in model text.
- Liang et al., Nature Human Behaviour 2025 — lexicon decay after awareness.
- Liang et al., Patterns 2023 — non-native-English false-positive rate.
- arXiv:2408.03319, 2024 — hedging and epistemic markers in human vs model text.
