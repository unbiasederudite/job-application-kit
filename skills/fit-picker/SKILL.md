---
name: fit-picker
description: Match a specific job posting's requirements against the user's comprehensive career fact-base, selecting which real experience stories and skills are worth using for that application — cited back to their exact source, with zero rewriting or polishing. Use this whenever preparing to tailor a CV or cover letter for one specific job that already has an analysis.md (from job-analyzer) and a fact-base.md to draw from, or whenever the user asks things like "what from my background actually fits this role" or "pull the relevant stuff for this application." This sits between job-analyzer and tailor-cv — tailor-cv expects this skill's output to already exist. This is a pure selection step — never invent, never rephrase into something punchier, and never touch any CV file directly.
---

# Fit Picker

Matches a job posting's requirements against the user's fact-base, producing the material `tailor-cv` builds a tailored CV from.

## Inputs

- `data/fact-base.md` — the user's career record, maintained manually. Expect one heading per role/project (e.g. `## Acme Corp — Senior Engineer (2021–2023)`) so every fact is citable to a specific section. If it's just a wall of text with no headings, ask the user to add them before citing anything from it — a citation that just says "somewhere in fact-base.md" isn't verifiable.
- `data/applications/<slug>/analysis.md` — this posting's must-haves, strong preferences, and ATS keywords.

If either file is missing, stop and say which skill to run first (`job-analyzer` for a missing `analysis.md`, or ask the user to create `fact-base.md` if that's missing) — don't improvise a substitute from the conversation.

## What to produce

For every must-have, strong preference, and keyword in `analysis.md`, search the *entire* fact-base for everything that genuinely matches — not just the first hit. The same requirement is often supported by more than one entry, and they're rarely equally useful: a reference letter calling someone "highly organized" and the actual project that assessment was based on can both match "structured, analytical approach," but the project is the far more useful material to build a bullet from. Cite everything relevant under a requirement, not one example of it.

Write the result to `data/applications/<slug>/selection.md`:

```markdown
# Selected material — <Role> at <Company>

## Experience
- [source: fact-base.md § "Acme Corp — Senior Engineer (2021–2023)"] Led the migration of the payments service to a microservices architecture, cutting p99 latency by 40%.
  — matches must-have: "Kubernetes in production at scale"

## Skills (in relevance order)
- Kubernetes — matches keyword "Kubernetes"
- Go — matches "Go or Python for operators/tooling"

## Gaps against your fact-base
- AWS Solutions Architect Professional certification — no matching entry found anywhere in fact-base.md
```

Quote or lightly paraphrase for brevity, never improve — a flat, unremarkable fact-base entry should read flat and unremarkable here too, since turning it into a punchy bullet is `tailor-cv`'s job downstream, and it can only do that honestly starting from a faithful copy. Every line under "Experience" and "Skills" needs its `[source: ...]` citation. If you can't cite it, don't include it.

## Real gaps vs. generic gaps

`analysis.md` may already have a "Notable gaps vs. a typical candidate" section — that one is generic, written without knowledge of this specific person. "Gaps against your fact-base" is different: a requirement this person's recorded history doesn't cover *at all*. Don't merge the two.

If `fact-base.md` gets updated later, re-run this skill on the updated file rather than telling the user it's covered now without actually refreshing `selection.md`.
