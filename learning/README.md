# Evidence-Based Workflow Improvement

This process improves stored instructions, skills, references, context, and tool use. It does not train model weights and does not create an always-running background process.

Use it when work exposes an observed failure, a user correction, or a demonstrated better method that may be worth preserving.

## Improvement cycle

1. Record the observed failure, user correction, or demonstrated better method. Preserve the task, evidence, expected behavior, and actual behavior without adding invented certainty.
2. Identify the instruction, skill, reference, context item, or tool behavior most directly responsible. If responsibility is unclear, keep competing explanations explicit.
3. Propose the smallest reversible change that could correct the problem. Do not broaden a local lesson into a universal rule without evidence.
4. For a substantive reusable workflow or reasoning change, have `seo_reviewer` assess both the evidence and the proposed persistent change. The reviewer should flag overfitting, conflicting instructions, and evaluation gaps. A simple explicit preference may instead receive a scope, conflict, and read-back check; do not invent a benchmark for it.
5. Test substantive changes with fixed criteria on:
   - The original case that exposed the problem.
   - A different but relevant case that should benefit from the change.
   - An unaffected case that should not regress.
6. Keep the evaluation inputs and success criteria fixed during comparison. Do not change the rubric to favor the proposed revision.
7. Adopt supported changes and record the result. Leave unsupported ideas documented as hypotheses rather than presenting them as improvements.
8. Revisit adopted changes when later tasks provide confirming or conflicting evidence.

Routine task completion, a documented defect, or agent agreement alone is not a learning trigger. If the task demonstrates no reusable correction, make no learning record.

After the initial revision, limit repair to two additional rounds. If the fixed criteria still are not met, stop changing the workflow and report the unresolved issue, evidence, and likely next investigation.

## Suggested change record

For a future learning record, capture:

- Date and task reference.
- Observed failure or correction.
- Evidence.
- Suspected responsible component.
- Proposed minimal change.
- Reviewer assessment.
- Frozen evaluation criteria.
- Original, different, and unaffected case results.
- Decision: adopted, rejected, or retained as a hypothesis.
- Follow-up trigger or review date.
