---
name: fit-picker
description: Match a specific job posting's requirements against the user's comprehensive career fact-base, selecting which real experience stories and skills are worth using for that application — cited back to their exact source, with zero rewriting or polishing. Use this whenever preparing to tailor a CV or cover letter for one specific job that already has an analysis.md (from job-analyzer) and a fact-base.md to draw from, or whenever the user asks things like "what from my background actually fits this role" or "pull the relevant stuff for this application." This sits between job-analyzer and the skills that write tailored materials. This is a pure selection step — never invent, never rephrase into something punchier, and never touch any CV file directly.
---

# Fit Picker

Matches a job posting's requirements against the user's fact-base, selecting which real experience genuinely fits and citing exactly where each match came from.

## Inputs

- `data/fact-base.md` — the user's career record, maintained manually. Expect one heading per role/project so every fact is citable to a specific section. If it's unstructured, ask the user to add headings before citing anything from it — a citation that just says "somewhere in fact-base.md" isn't verifiable.
- `data/applications/<slug>/analysis.md` — this posting's must-haves, strong preferences, ATS keywords, and "Role profile". "Role profile" is written specifically to capture what the posting as a whole emphasizes.

If `analysis.md` is missing, stop and tell the user to run `job-analyzer` first — don't guess at posting requirements from the conversation. If `fact-base.md` is missing, stop and tell the user to run `interviewer` first — don't search for material that was never recorded.

## What to produce

For every must-have, strong preference, and keyword in `analysis.md`, search the *entire* fact-base for everything that genuinely matches — not just the first match. The same requirement is often supported by more than one entry, and they're rarely equally useful: a reference letter calling someone "highly organized" and the actual project that assessment was based on can both match "structured, analytical approach," but the project is the far more useful material to build a bullet from. Cite everything relevant under a requirement, not one example of it.

Those bullets tell you *what* to search for. They do not tell you *how strong* a match is once you've found it — that's decided by fit to "Role profile" alone, and nothing else. Order "Experience" most relevant first by that single measure: whether a match *is* the thing "Role profile" describes this role as actually being about, versus one that merely brushes against a related skill in passing. This isn't a formality — this order is a claim about strength that whatever consumes `selection.md` will trust without re-deriving it, so get it wrong and a technically-correct but off-theme story ends up presented as the strongest one. A match with the single strongest number in the entire fact-base still ranks below a weaker-sounding one if the number belongs to a story "Role profile" treats as peripheral, and a strong preference "Role profile" treats as central outranks a must-have it treats as boilerplate — quantification and must-have/strong-preference labels never outrank fit to "Role profile." Only when two matches are genuinely tied on that measure does the tiebreaker kick in: prefer whichever has the more concrete, quantified outcome.

"Role profile" usually states not just what the role *is* but what it explicitly *isn't* — "support work, not ownership of a build," "collaborative, not solo," a domain it says isn't actually screened for. Before ranking, pull out every one of those explicit exclusions. Then check each candidate match against all of them, not only the ones a big number or a keyword happens to make salient — a match can satisfy a must-have or keyword and still be the exact thing "Role profile" said the role isn't about. Matches sharing the same disqualifying trait (both solo technical builds with no collaborative angle, say) form one tier and must be ranked consistently with each other: none of them jumps the tier just for having an eye-catching number, but the tiebreaker above still applies *within* the tier, so among tier-mates the one with the more concrete, quantified outcome ranks above the rest of that same tier, not below it.

Write the result to `data/applications/<slug>/selection.md`:

```markdown
# Selected material — <Role> at <Company>

## Experience (most relevant first)
- [source: fact-base.md § "Acme Corp — Senior Engineer (2021–2023)"] Led the migration of the payments service to a microservices architecture, cutting p99 latency by 40%.
  — matches must-have: "Kubernetes in production at scale"

## Skills (in relevance order)
- Kubernetes — matches keyword "Kubernetes"
- Go — matches "Go or Python for operators/tooling"

## Gaps against your fact-base
- AWS Solutions Architect Professional certification — no matching entry found anywhere in fact-base.md
```

Quote or lightly paraphrase for brevity, never improve — a flat, unremarkable fact-base entry should read flat and unremarkable here too, since later rewriting steps need a faithful copy to build from honestly. Every line under "Experience" and "Skills" needs its `[source: fact-base.md § ...]` citation, and it has to name the actual entry or heading it came from (`E1.6`, `R2.4`, `"E1 — Acme Corp"`) — not a vague pointer like "E1 context" that can't be checked against the file. If you can't cite it precisely, don't include it.

Before finishing, do a separate completeness pass, one item at a time through every must-have, strong preference, and keyword in `analysis.md`: each one needs a visible outcome, with no third option — cited somewhere in "Experience" or "Skills," or named in "Gaps." This is a different failure mode from a bad ranking, and easy to shortchange once you're focused on getting the ranking right: a low-ranked citation is still visible to whatever reads `selection.md`, but a silently dropped one is invisible and can't be caught downstream — and that risk is highest for whatever "Role profile" itself calls out as central or most-repeated, since that's the one thing a reader would notice missing fastest.

A near-miss doesn't count as a match just because it shares a surface feature with what's being asked for. If the closest candidate doesn't actually demonstrate the specific thing being asked for, it belongs in Gaps with a sentence explaining why, not a citation that stretches the evidence to avoid an empty entry.

If `fact-base.md` gets updated later, re-run this skill on the updated file rather than telling the user it's covered now without actually refreshing `selection.md`.

## After selection

Tell the user what you found — a short summary of what's well-covered and any gaps — and ask if they want to proceed straight to tailoring, or review/correct `selection.md` first. The ranking is a judgment call built on top of `analysis.md`'s "Role profile," and whatever consumes `selection.md` will trust it without re-deriving it, so this is the checkpoint where the user can catch a bad ranking before it shapes anything downstream. Don't chain into tailoring automatically.
