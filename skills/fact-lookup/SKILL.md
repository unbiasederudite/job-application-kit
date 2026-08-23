---
name: fact-lookup
description: Search the user's fact-base.md for everything true about a specific topic, entry, or gap, returning every match cited to its exact source. Use this whenever the user asks something like "what do I know about X" or "look up my experience with Y" directly, or whenever tailor-cv needs one more concrete, true detail to fill out a bullet or skills line after selection.md is already exhausted. This is pure retrieval, not selection — it doesn't weigh matches against a job posting or decide what's worth using, it just reports what's true and cites where it's documented.
---

# Fact Lookup

Searches `fact-base.md` for a specific query and returns everything true that matches, cited to its exact source.

## Inputs

- `data/fact-base.md` — the user's career record, maintained manually. Expect one heading per role/project so every fact is citable to a specific section. If it's unstructured, ask the user to add headings before citing anything from it — a citation that just says "somewhere in fact-base.md" isn't verifiable.
- A query: a topic, an entry name, or a specific gap to fill (e.g. "Acme Corp internship, anything not already used elsewhere," "Docker experience," "one more skill for the Tools category").

If `fact-base.md` is missing, stop and tell the user to run `interviewer` first — don't search for material that was never recorded.

## What to produce

Search the *entire* file for the query, not just the first match. Return every true match, however many there are — don't judge relevance to any particular job posting, and don't stretch a weak match to look like a stronger one; if nothing matches, say so plainly.

```markdown
## Results for "<query>"
- [source: fact-base.md § "Acme Corp — Senior Engineer (2021–2023)"] Led the migration of the payments service to a microservices architecture, cutting p99 latency by 40%.
- [source: fact-base.md § "Acme Corp — Senior Engineer (2021–2023)"] Mentored two junior engineers through their onboarding.
```

Or, if nothing matches: `No matching material found in fact-base.md.`

Quote or lightly paraphrase for brevity, never improve — whoever's asking decides what to do with a flat fact, not this skill. Every line needs its `[source: ...]` citation; if you can't cite it, don't include it.

## After lookup

Report the results exactly as shown above and stop — deciding what to do with a flat fact isn't this skill's job.
