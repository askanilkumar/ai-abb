# RAG Architecture Reference
*Editable template — Day 1 (M3 / Lab 3). The shape your engineers build against, failure modes marked.*

## The pipeline

```
documents → CHUNK → EMBED → index          (indexing path: paid once per document update)
question  → EMBED → RETRIEVE top-k → ANSWER with citations   (query path: paid per question)
```

## The dials and their failure modes

| Stage | Dial | Classic failure | Symptom in production |
|---|---|---|---|
| Chunk | size & overlap (start ~1,200 chars) | Whole-document chunks | Vague answers, token bill 5× |
| Embed | model choice | Over-buying out of fear | Indexing cost is one-time — optimise the query path first |
| Retrieve | k (start 4) | k too small | Questions needing two documents fail |
| Answer | system prompt | No "answer only from context" rule | Confident fabrication filling retrieval gaps |

## Non-negotiables in the answer prompt

- Answer ONLY from provided context
- Cite sources per claim
- Exact refusal string when context lacks the answer ("Not in the knowledge base — escalate")

## Cost structure

- **Indexing**: embeddings, paid per corpus update → scales with document churn
- **Per question**: retrieved context + answer tokens → scales with adoption ← budget this one

## When flat RAG is not enough (M5 rule)

| Signal | Build |
|---|---|
| "What does X say / how do I fix Y" — answers live in passages | Flat RAG |
| Questions join entities (customer × firmware × bulletin) | Graph-backed retrieval — or honestly, SQL |
| Not sure | Start flat, log failing questions, count them |

## First three questions to ask any RAG proposal

1. Who owns document freshness, and how does the index update?
2. Where is the eval set, and who wrote the questions?
3. What is the cost per question at target adoption, and the chunk/k settings behind it?
