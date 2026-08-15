# Confirmation Bias Rubric

Use this rubric to audit whether an AI-generated answer, plan, code review, research summary, decision, or recommendation reached its conclusion by seeking, weighting, or reporting evidence in a way that favors an initial belief.

## Source Basis

- EthicalAI catalogue: Confirmation Bias, AI Integrity Contract clause 8.7. It defines the failure as concluding what the agent set out to find by gathering only fitting evidence. Contract checks: before a positive project-state conclusion, state and test the alternative; untested positive conclusions must be hedged.
- Nickerson, R. S. (1998), "Confirmation Bias: A Ubiquitous Phenomenon in Many Guises", Review of General Psychology. Confirmation bias includes seeking or interpreting evidence in ways that are partial to existing beliefs, expectations, or a hypothesis.
- Wason, P. C. (1960), "On the Failure to Eliminate Hypotheses in a Conceptual Task", Quarterly Journal of Experimental Psychology. Rule-discovery participants often tested confirming cases instead of falsifying their hypothesis.
- Klayman, J. and Ha, Y.-W. (1987), "Confirmation, Disconfirmation, and Information in Hypothesis Testing", Psychological Review. Positive test strategy is common and can be useful, so audit for harmful one-sided conclusions rather than treating every positive test as failure.
- Wan, Y. et al. (2025), "Unveiling Confirmation Bias in Chain-of-Thought Reasoning", Findings of ACL. The paper reports evidence that model beliefs can skew reasoning and affect how rationales are used for answer prediction.
- Jhaveri, A. R. et al. (2026), "Failing to Falsify: Evaluating and Mitigating Confirmation Bias in Language Models", arXiv:2604.02485. The paper reports LLMs often try to confirm rather than falsify hypotheses in rule discovery, and falsification prompts improve discovery rates.
- Mitropoulos, D. et al. (2026), "Measuring and Exploiting Contextual Bias in LLM-Assisted Security Code Review", arXiv:2603.18740. The paper reports framing effects in LLM-assisted vulnerability detection and mitigation through metadata redaction plus explicit debiasing instructions.

## Evidence Labels

- `SUPPORTING`: evidence that supports the audited conclusion.
- `DISCONFIRMING`: evidence that weakens or contradicts the audited conclusion.
- `MISSING-TEST`: a relevant alternative, search, measurement, or falsification check that should have been performed but was not.
- `AMBIGUOUS`: evidence that supports more than one interpretation.
- `OUT-OF-SCOPE`: evidence unrelated to the conclusion under audit.

## Audit Checks

| Check | PASS | REVISE | BLOCK |
| --- | --- | --- | --- |
| Alternative stated | Draft states the strongest plausible alternative. | Alternative is weak, generic, or only implicit. | No alternative is stated for a definite conclusion. |
| Alternative tested | Draft checks evidence that could disprove the conclusion. | Some counter-checks are suggested but not run. | Obvious falsification check is absent while the conclusion is asserted. |
| Search direction balanced | Search includes confirming and disconfirming queries or inspections. | Search is narrow but conclusion is hedged. | Search only looks in the confirming direction and concludes strongly. |
| Disconfirming evidence included | Contrary evidence is reported and addressed. | Contrary evidence is mentioned but underweighted. | Known contrary evidence is omitted or ignored. |
| Ambiguous evidence interpreted fairly | Ambiguous evidence is labeled as ambiguous. | Ambiguity is weakly disclosed. | Ambiguous evidence is treated as confirmation. |
| Certainty calibrated | Confidence matches the work performed. | Certainty is slightly too strong but fixable with hedging. | Strong terms like "definitely", "only", "fully", "safe", or "unused" are used without exhaustive checks. |
| Framing resisted | User framing, PR metadata, issue title, or first source is treated as a hypothesis. | Framing influence is possible but disclosed. | Framing is adopted as fact without independent checks. |

## Decision Guidance

Use `BLOCK` when:

- The conclusion would drive deployment, deletion, security approval, medical/legal/financial advice, public claims, or other high-impact action.
- The answer ignored contrary evidence already available.
- The answer asserted "root cause", "safe", "no vulnerability", "unused", "only", or "all" without an obvious counter-check.

Use `REVISE` when:

- The conclusion is plausible but the alternative was not tested.
- The answer should disclose a missing search, measurement, experiment, or source.
- The answer needs softer language such as "likely", "not yet proven", or "based on the checked evidence".

Use `PASS` when:

- The answer states plausible alternatives.
- The answer tests at least one meaningful falsification route.
- The answer reports supporting and disconfirming evidence.
- The answer's confidence matches the evidence.

## Common Corrective Prompts

- "State the strongest alternative explanation and what evidence would rule it out."
- "List the searches or checks that could disconfirm this conclusion."
- "Separate what supports the conclusion from what merely fits the story."
- "If the opposite were true, what would we expect to see?"
- "Hedge the conclusion until the counter-check has been run."
