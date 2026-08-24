---
name: cover-letter
description: Write and render a formal, tailored cover letter PDF for one specific job application (3-4 short paragraphs, a specific opening hook, 1-2 accomplishments picked for genuine fit to the role, a company-specific close) — built entirely from cited source material, never invented. Use this whenever the user wants to write, draft, revise, or render a cover letter for one specific job that already has a selection.md (from fit-picker) and an analysis.md (from job-analyzer) to draw from, or mentions pairing a cover letter with a job application. This never touches data/cv.yaml — a cover letter is its own document with its own baseline, not derived from the CV. Always use this rather than writing a plain text/Word cover letter, unless the user explicitly asks for something other than a rendered PDF.
---

# Cover Letter

Copies the user's baseline cover letter into one application's folder and rewrites the per-application fields into a short, specific letter for that posting.

## Inputs

- `data/cl.yaml` — the user's baseline cover letter, maintained manually. Never modify it — this skill only copies it into each application folder.
- `data/applications/<slug>/selection.md` — the accomplishments this letter draws from.
- `data/applications/<slug>/analysis.md` — everything about this posting: must-haves, strong preferences, ATS keywords, "Role profile," and (when present) "Hiring contact"/"Headquarters". This is the only source for what the posting wants and who it's for.

If `selection.md` is missing, stop and tell the user to run `fit-picker` first — don't improvise a substitute from the conversation. If `analysis.md` is missing, stop and tell the user to run `job-analyzer` first — don't guess at posting requirements from the conversation. If `cl.yaml` is missing, stop and tell the user to run `uv run rendercl new "Full Name"` from the repo root — don't build a first baseline here, this skill only copies an existing one.

## What to produce

Copy `data/cl.yaml` to `data/applications/<slug>/cl.yaml`. If `data/applications/<slug>/cl.yaml` already exists, that's an existing draft to read and edit, not overwrite.

`cl.sender`, `design`, and `settings` are fixed, copied unchanged: personal/preference-level details, not something one application should rewrite. Within `cl`, `recipient`, `salutation`, `closing`, and `body` are tailorable, rewritten for this application. Fill `recipient.name`/`title` from `analysis.md`'s "Hiring contact" section and `recipient.company`/`address` from its "Headquarters" section when present; otherwise leave those fields blank — the baseline's own "Hiring Manager" fallback covers it.

A cover letter earns its place by being short and specific. There are two layers of relevance here, and only one is this skill's job. `fit-picker` already decided which material is strongest, ranking `selection.md`'s "Experience" against `analysis.md`'s "Role profile" — that's layer one, already done, not something to re-derive while drafting. This skill's layer is different, and it governs every paragraph: the Opening's hook, the Body's "what this means for this role" sentence, and the Close's "why this company" reason all have to point at the same place — what "Role profile" says this role actually centers on — not just at whichever must-have, preference, or keyword the paragraph happens to tick. A paragraph can cite the single best-ranked item in `selection.md`, or the single truest fact about the company, and still fail this layer if it points somewhere else. The CV already covers what you *did*; every paragraph here needs the explicit pivot to what you'll *do for them*, aimed at that same center.

Formal register throughout, no contractions ("I am," not "I'm"). Punctuation: commas and periods only. No em dashes, en dashes, colons, or semicolons — split into two sentences instead.

Mirror `analysis.md`'s "Keywords for ATS matching" naturally throughout the letter, in your own sentences about your own experience — never lifted as a block in quotation marks, which reads as copy-paste rather than genuine relevance. This applies everywhere in the letter: most cover letters get filtered for missing the posting's own vocabulary, not for missing substance.

Fit 3-4 short paragraphs on one page, 250-300 words total. Short is the goal, but under-length is its own failure mode: a letter that's too thin to fit a real hook, a real bridge, and a real close has usually skipped one of them rather than earned genuine brevity. Over 300 is the opposite failure: a paragraph is carrying two ideas that should be one, or a sentence is explaining itself instead of just making its point — cut, don't just trim words, until it fits.

- **Opening** — role and a specific hook, in 1-2 sentences. Never "I am writing to apply for..." or "I'm excited to apply for...". The hook is a specific detail from `analysis.md` that proves you read past the job title — something about what "Role profile" says this role actually centers on, not a generic fact anyone could have found. Don't build it from the same accomplishment the Body bridges from, even "at a different angle" — two paragraphs arguing from the same fact reads as repetition no matter how it's rephrased, and the Opening's job is to point at the same center from different evidence, not the same evidence twice. Compare the role to your experience directly, not a description of one to the other ("your description of this role is close to the four months I spent" isn't a valid comparison). Draft this last, after the Body, so it complements the bridge you actually used. Test: if it could be pasted into a letter for any other company, rewrite it.

- **Body** — 1-2 accomplishments from `selection.md`'s "Experience", built as a bridge: name the must-have or preference from `analysis.md`, give the proof from `selection.md`, then say what it means for this role. Never invent an accomplishment, number, or skill that isn't in `selection.md`. Pick candidates the same way `fit-picker` did: work down `selection.md` from the top, since it's already ranked by fit to "Role profile," and take the first items that give you a genuine bridge to this posting. Don't skip down the list because a lower item happens to make livelier prose — a vivid story built on weaker evidence argues the wrong thing to the reader. Quote reference-letter material in quotation marks with attribution, e.g. "my supervisor described the report as 'a professional and well reasoned assessment.'" Attribution without actual quote marks ("my supervisor wrote that my report was...") still reads as self-description — check for literal quotation marks around the source's own words. Only name a tool or library `analysis.md` itself calls for.

- **Close** — restate your value as the outcome of the opening hook, cite a genuine "why this company" detail drawn from `analysis.md` (most often something "Role profile" says about what the team actually does or values), end with a direct call to action. A benefit the posting offers you — flexible hours, onboarding support, tool access — doesn't count as "why this company," even when it's specific: it argues what you'd get, not what you'd bring. If the only specific detail available is a perk, cut the sentence rather than reach for it. State the next step plainly ("I would welcome the chance to talk about how I could contribute to X"), not passively ("I hope to hear from you") or demandingly ("I look forward to your response by Friday").

## Humanizing the draft

Run the drafted `body` paragraphs through `humanizer` before rendering — a required step, not optional polish, since unedited LLM tells (inflated importance, forced rule-of-three, "I am excited to...") undo the tailoring above. Do this before the final keyword check, not after, since humanizer can smooth away a deliberately-kept keyword; afterward, skim against `analysis.md`'s keyword list and restore anything lost.

## Rendering

Once the humanized draft is ready, render it:

```
uv run rendercl render data/applications/<slug>/cl.yaml
```

If the user later asks for a change to one paragraph, the recipient, or any other tailorable field, edit that field directly in `data/applications/<slug>/cl.yaml` and re-render. Re-run the humanizing pass on any paragraph you rewrote, not just the first draft; a hand-edited follow-up can reintroduce the same tells the first pass removed.

## After rendering

Tell the user the PDF is ready and where it is, then ask if they want to review/correct it before treating it as final. Each paragraph's pivot toward `analysis.md`'s "Role profile" is a judgment call, not an extraction, and a hiring manager reads the finished letter without re-deriving it, so this is the checkpoint where the user can catch a bad pivot before it goes out — sending or submitting the application is a separate, manual step outside this skill's scope.
