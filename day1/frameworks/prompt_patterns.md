# Prompt Patterns Reference
*Editable template — Day 1 (M2 / Lab 2). Add your team's measured entries at the bottom.*

## The four production patterns

| Pattern | What it is | Why it matters |
|---|---|---|
| **Structured output** | Demand JSON against a schema, not prose | Parseable, testable, cheaper (shorter outputs) |
| **Context engineering** | Supply the reference facts the task needs, nothing more | Facts in context beat facts hoped-for in training; extra context is paid noise |
| **Cache-friendly design** | Stable system prompt; variable content last | Cached input tokens are billed at a fraction — only identical, stable prefixes cache |
| **Model-appropriate scaffolding** | Mini models get rules + examples + schema; frontier models need less | Scaffolding is what unlocks the 15–20× cheaper model |

## The banned anti-pattern

The **kitchen-sink prompt**: hundreds of words of polite prose instructions, rewritten per call.
Costs multiples per call, never caches, usually scores *worse*. Standard response when you see one:
**"Show me the bake-off"** — the measured comparison against a short schema-constrained version.

## The bake-off method (from Lab 2)

1. One real task, ≥5 real inputs with known correct outputs.
2. 3–4 prompt designs (naive / verbose / few-shot / structured schema).
3. Score each design: quality % + tokens + cost per realistic annual volume.
4. Standardise the winner in this library; revisit when the task or model changes.

## Team prompt library

| Task | Standard design | Quality | Cost (per ___ ) | Model | Owner | Last measured |
|---|---|---|---|---|---|---|
| Ticket classification (lab example) | V4 structured schema | % | $ /100k tickets | mini | | 12 Nov 2026 |
| | | | | | | |
