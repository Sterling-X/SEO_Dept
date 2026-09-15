# Core Hub Validator Test Summary

Intentionally broken documents were created only in a temporary directory and removed after execution.

## Positive fixture

| Case | Expected pass observed | Exit | Required marker |
|---|---|---:|---|
| Structural validator accepts the fixture | Yes | 0 | `PASS: Supported deterministic Core Hub checks cleared.` |
| Recovered page validator accepts the fixture | Yes | 0 | `PASS: All hard rules cleared.` |
| Legal citation abbreviations remain within two sentences | Yes | 0 | `count=2` |
| Documented local-detail marker warns without inventing a hard failure | Yes | 0 | `[LOCAL DETAIL] markers require editorial resolution` |
| Conditional child with explicit gate evidence can generate | Yes | 0 | `DOCX written:` |
| Ephemeral claim-free sourced output uses the 12 pt Sources contract | Yes | 0 | `PASS: Supported deterministic Core Hub checks cleared.` |

## Meaningful negative fixtures

| Case | Expected failure observed | Exit | Required marker |
|---|---|---:|---|
| Wrong page size rejected by structural validator | Yes | 1 | `Page size must be US Letter` |
| Duplicate body URL rejected by recovered validator | Yes | 1 | `Single-Placement Rule violated` |
| Em dash rejected by recovered validator | Yes | 1 | `Em dashes` |
| Broken hyperlink relationship rejected by structural validator | Yes | 1 | `not an external OOXML hyperlink relationship` |
| Unmanifested functional URL rejected by structural validator | Yes | 1 | `Unmanifested DOCX hyperlink target` |
| Heading inserted into two-paragraph opening rejected | Yes | 1 | `H1 must be followed immediately` |
| Reordered required sections rejected | Yes | 1 | `Required H2 roles must appear` |
| Required CTA without body copy rejected | Yes | 1 | `Required cta section has no body content` |
| Unbold local-detail marker rejected | Yes | 1 | `local-detail markers must be bold runs` |
| Undocumented generic placeholder rejected | Yes | 1 | `Unresolved placeholder markers found` |
| Missing local-contract header rejected | Yes | 1 | `Local Core contract requires a header part` |
| Missing local-contract footer rejected | Yes | 1 | `Local Core contract requires a footer part` |
| V2-held child target rejected before generation | Yes | 1 | `cannot be linked while its gate is HOLD` |
| Conditional child without gate evidence rejected | Yes | 1 | `requires target_gate_approval` |
| Four true sentences rejected after citation-aware parsing | Yes | 1 | `exceeds 3 sentences (4)` |
| Eleven-point Sources entry rejected | Yes | 1 | `Sources text must use 12 pt body size` |
| Renderer rejects a stale output directory | Yes | 2 | `Render output directory must be absent or empty` |

These tests demonstrate only the named mechanical detections. They do not evaluate legal accuracy, editorial quality, strategy, or rendered layout.
