# Deployment Decision Tree
*Editable template — AI Engineering for Managers, Day 1 (M1). Fill the worked example with your own team's request.*

Use this on any AI request your team brings you. It takes minutes, not meetings.

## The tree

**1. Is this one person being faster, or a team workflow?**
- One person → **Tier 1** (Abby / Copilot). Stop — don't build what a seat licence solves.
- Team workflow → continue.

**2. Can the data leave your tenancy under vendor terms?**
- Cannot even sit in your cloud region → **Tier 3** (self-hosted).
- Can sit in your tenancy/region → continue.

**3. Is volume steady and very high (always-on, millions of calls/month)?**
- Yes → price Tier 3 against Tier 2 before committing.
- No / spiky / unknown → **Tier 2**.

**4. Default: Tier 2 (managed/serverless endpoint).** Start serverless, measure, move only with evidence.

## Tier reference

| | Tier 1 · SaaS assistant | Tier 2 · Managed endpoint | Tier 3 · Self-hosted |
|---|---|---|---|
| You control | Prompts only | Prompts, context, guardrails, routing | Everything incl. weights |
| Cost model | Per seat | Per token | Per GPU-hour |
| Data path | Vendor's terms | Your tenancy, your region | Never leaves your network |
| Right for | Individual productivity | Team applications (the 80% case) | Hard data constraints, extreme steady volume |

## Worked example (replace with yours)

| Field | Entry |
|---|---|
| Request | |
| Requested by / date | |
| Q1 person or workflow? | |
| Q2 data constraint? | |
| Q3 volume? | |
| **Decision** | Tier ___ |
| Revisit when | (volume 10×? data class changes?) |
