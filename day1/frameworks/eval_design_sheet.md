# Eval Design Sheet
*Editable template — Day 1 (M4 / Lab 4). One sheet per AI use case. Rule: no eval set, no deployment.*

## Use case

| Field | Entry |
|---|---|
| Application | |
| Owner | |
| Eval set size | (20 minimum before scores mean anything) |
| Question authors | (the people who answer these questions today — not the builder) |
| Judge | LLM-as-judge, 0–2 scale, temperature 0 |
| Baseline score | % on (date) |
| Deployment gate | score ≥ ___% ; sign-off for exceptions: |

## Scoring scale

- **2** — correct and complete on the facts that matter
- **1** — partially correct; misses or muddles something important
- **0** — wrong, or fails to give the key facts

## The regression discipline

1. Run eval → baseline.
2. Change **one** thing (prompt, k, chunking, model).
3. Re-run the **same** eval.
4. Score holds or improves at acceptable cost → ship. Otherwise → revert.

Every proposed change answers: *what did the eval score do?*

## Guardrails checklist (deploy alongside the eval)

- [ ] Input guard: off-topic + injection patterns bounced (rules first, cheap model second)
- [ ] Output guard: groundedness check before the answer ships
- [ ] Refusal path: exact escalation string, logged
- [ ] Eval re-run scheduled: on every change + monthly drift check

## Question bank starters

Include: the 5 most common real questions · 3 ambiguous/misspelled ones ·
2 that the knowledge base cannot answer (correct answer = the refusal) ·
2 multi-document questions · 1 injection attempt (correct answer = block).
