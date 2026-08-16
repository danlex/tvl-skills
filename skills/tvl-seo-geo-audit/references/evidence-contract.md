# Evidence Contract

All audits must separate evidence state from evidence origin.

## Evidence States

| State | Meaning | Can pass? |
| --- | --- | --- |
| `CONFIRMED` | Direct evidence verifies the statement. | Yes |
| `REFUTED` | Evidence contradicts the statement. | No |
| `NOT_FOUND` | The expected element was absent in collected evidence. | Sometimes, only when absence is acceptable |
| `NOT_TESTED` | The check was not run. | No |
| `MISSING_TEST` | The check was required for the declared scope but evidence was not collected. | No |
| `UNVERIFIABLE` | Evidence exists but cannot establish the conclusion. | No |
| `MISLEADING` | The element exists but misrepresents visible content, source, entity, language, or offer. | No |

## Evidence Origins

| Origin | Meaning |
| --- | --- |
| `MEASURED` | Collected directly by an identified tool during this audit. |
| `USER_PROVIDED` | Supplied by the user, including exports or screenshots not independently rechecked. |
| `INFERRED` | A model conclusion from cited observations. |

Do not collapse origin and state. A user-provided Search Console export can support a `CONFIRMED` finding while still retaining `USER_PROVIDED` origin.

## Audit Manifest

Evidence JSON must include:

- Requested URL.
- Final URL when fetched.
- Retrieval timestamp.
- Audit mode.
- Selected sample.
- Evidence source identifiers and collection status.
- Tool names and versions when available.
- Fetch, rendering, robots, sitemap, parsing, or environment limitations.
- Content hash for each saved response or rendered snapshot.

## Finding Contract

Each finding must include:

- `id`
- `check_id`
- `priority`: `P0`, `P1`, or `P2`
- `area`
- `result`: `PASS`, `REVISE`, or `BLOCK`
- `blocker_category` when applicable
- `evidence_state`
- `origin`
- `evidence_refs`
- `location`
- `evidence`
- `impact`
- `fix`
- `verification`
- `effort`: `S`, `M`, or `L`

Every fix must include a verification method. Do not invent implementation hours.

## Rollup Rules

- Any verified `P0` finding rolls up to `BLOCK`.
- Any verified `P1` finding or core `MISSING_TEST` rolls up to `REVISE`.
- `PASS` requires no verified `P0` or `P1` findings and verified core evidence for the declared mode.
- Suppressed findings must keep a suppression reason for debugging.
