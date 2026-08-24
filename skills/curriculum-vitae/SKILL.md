---
name: curriculum-vitae
description: Rewrite the content (never the design or theme) of the user's existing real CV into a per-application copy for one specific job posting, using material already selected and cited by fit-picker to reorder, reword, or replace what's already on the page to mirror the posting's exact terminology, never to add or remove a bullet, skill, or entry beyond what the baseline already has, then rendering it with rendercv. Use this whenever tailoring, adapting, or customizing a CV for one specific job that already has a selection.md (from fit-picker) and an analysis.md (from job-analyzer) ready. Refuses to invent anything beyond what was selected or already in the baseline — building a first baseline CV from nothing is out of scope for this skill.
---

# Curriculum Vitae

Rewrites the user's existing CV for one job — same person, same design, different emphasis — using only material `fit-picker` already selected and verified.

## Inputs

- `data/cv.yaml` — the user's real baseline CV. Read-only: never modify it. Read it for its existing content, not just its structure — that content gets reconciled against `selection.md`, not discarded and rewritten from scratch.
- `data/applications/<slug>/selection.md` — from `fit-picker`. The material ceiling — see "Reconciling existing content" below.
- `data/applications/<slug>/analysis.md` — two things from it: "Keywords for ATS matching," for mirroring the posting's phrasing, and "Role profile," for judgment calls `selection.md` alone can't inform (e.g. framing a bullet around ownership vs. task execution). `fit-picker` reads "Role profile" too, but only to rank; it never surfaces that judgment in `selection.md` itself, so this is where it's still needed.

If `selection.md` is missing, stop and tell the user to run `fit-picker` first — don't read `fact-base.md` yourself and pick material ad hoc, that skips its citation discipline. If `analysis.md` is missing, stop and tell the user to run `job-analyzer` first — don't guess at the posting from the conversation.

## What to produce

Copy `data/cv.yaml` to `data/applications/<slug>/cv.yaml`. If `data/applications/<slug>/cv.yaml` already exists, that's an existing draft to read and edit, not overwrite.

Only `cv:` content changes — every other top-level block stays exactly as the baseline has it. Within `cv`, only two things ever get rewritten: an entry's `highlights` list, and the skills section. An entry that's a pure record of fact — a credential, an education — is fixed, never touched, whatever section it lives in, even if `selection.md` cited something from it as supporting evidence elsewhere. An entry that showcases actual work — a role held, a project built, any contribution with a real highlight to make — is tailorable, with its `highlights` list reconciled against `selection.md` and rewritten. Within skills, the one line that's itself a pure fact (languages spoken) is fixed, copied from the baseline exactly; the rest is tailorable, always exactly 4 lines total, never more and never fewer.

The aim is never to rebuild the page around this posting alone. It's to make the baseline stronger without erasing it: most of what's already there should come out the other side as Keep as-is, and Replace is reserved for genuine weak points, not a license to swap in `selection.md` material just because it exists. Nothing gets added or removed either — whatever the baseline already has stays on the page, in the same slot; only its wording and relative strength are tailorable. A bullet that's weak against "Role profile" is a candidate to sink toward the bottom of its entry or lose out to a **Replace**, never a candidate to cut outright. The baseline and the tailored content live on the page together, side by side; tailoring reinforces what's already there, it doesn't rewrite the page from scratch.

Before writing anything, decide what happens to what's already on the page. There are two layers of relevance here, and only one is this skill's job. `fit-picker` already decided which material from the fact-base is strongest, ranking `selection.md`'s "Experience" against `analysis.md`'s "Role profile" — that's layer one, already done, not something to re-derive here. This skill's layer is different: for each tailorable entry, and separately for each of the 4 tailorable skills lines, go bullet by bullet (or skill by skill) and check it against two things, not just whether it formally ticks a must-have, preference, or keyword. First, does it point at what "Role profile" says this role actually centers on. Second, does its wording already use the posting's own terminology, its "Keywords for ATS matching," must-haves, and strong preferences, wherever that's honest to do so — most CVs get filtered by ATS keyword matching before a person ever reads them, so this is a real, separate question from whether the underlying substance belongs.

- **Keep as-is** — the bullet or skill already points at that center, and its wording already uses the posting's own terminology.
- **Reword** — the bullet or skill already points at that center, but its wording doesn't yet. This is the default move whenever the substance is already right, and mostly a substitution problem, not an addition problem: swap a generic verb or noun for the posting's exact keyword when the underlying work genuinely involved it ("moved data between systems" becomes "orchestrated a data pipeline" when the fact-base shows it actually was one), or drop in a specific tool verbatim, exactly as the posting spells it, when the work genuinely used it. This cuts both ways, in bullets and skills lines alike: don't reach for a keyword the work doesn't actually support, and don't paraphrase away a tool name that's already exact. A word, a few words, or a couple of words is the right scope; forcing more than that in is stuffing, not tailoring, and a sign the bullet isn't pointing at the right place to begin with, not just phrased wrong — which makes it a Replace, not a Reword.
- **Replace** — the bullet or skill doesn't point at that center at all, not a wording problem but a substance one, and `selection.md` has something that does. This is a last resort, not a default: a bullet that's already on-theme never gets promoted to Replace just because a punchier alternative happens to exist elsewhere, only Reword does that work. When Replace is genuinely warranted, work down `selection.md`'s ranked list from the top, within whatever's relevant to this entry or this skills category, and take the first item that genuinely points at that center, written in the posting's own terminology from the start. Don't skip past a higher-ranked item because a lower one would make a punchier bullet or a more impressive-sounding skill — a vivid highlight built on weaker evidence still argues the wrong thing. Judge every bullet and skill this way independently: a bullet that already earned a Replace elsewhere on the page doesn't make the next genuinely off-theme one any less deserving of one. If the CV has several real, distinct gaps against "Role profile" or its keywords, each gets its own Replace — the last-resort test applies per bullet, not once per entry or once per CV.

Don't add a `headline` or `summary` if the baseline doesn't have one either — that's a new structural element, not a reconciliation. Never invent an accomplishment, number, or skill that isn't in `selection.md` or in the existing baseline.

The tailored CV stays within one page, the same page budget the baseline already fits in. Tailoring changes what's on the page and how it's worded, never how many pages it takes.

### Writing the bullets

Once reconciliation has settled what's kept, reworded, or replaced for an entry, this is how to write each resulting bullet.

A bullet states one thing that was built, found, or delivered, and nothing else. Not an inventory of adjacent facts (tech stack, team size, department count), not that one thing plus a trailing clause narrating how, why, or under what conditions it happened, not a when/where clause unless the timing is itself the measurable difficulty being proven (validating a pipeline before the hardware it serves existed earns its place; a generic "in the last month of the internship" is just metadata), not naming who else was involved unless that person's role is itself the measurable difficulty (routine sign-off from a reviewer or approver is metadata, not achievement, the same way a generic timing clause is), and not company or role framing that already lives in the entry's own `company`/`position`/`date` fields. "Migrated the billing service to microservices, cutting deploy time in half" is a highlight; tacking on "using a strangler-fig pattern to avoid a big-bang cutover" is commentary about method, not a second highlight, and a semicolon or comma stringing two clauses together is usually the tell that two facts got glued into one bullet and need to split. 

Within one entry, no two bullets should repeat that same number, scope detail, or opening verb either; each should introduce something new, and two that end up proving the same underlying fact belong merged into one, not written separately. Two clean bullets beat one crowded one, and beat four thin ones too, since a true fact doesn't automatically earn a slot, and routine participation ("used the tool daily") is context, not a highlight, fine to leave off the page.

Every bullet follows the XYZ formula, always: *Accomplished [X], as measured by [Y], by doing [Z]*. Lead with a strong, specific action verb for [Z], and when the underlying material gives you a real number, quantify it as [Y]. If there's no real number to measure by, drop [Y] and write the leaner XZ form instead — *Accomplished [X] by doing [Z]* — never settle for a vague description in its place. Before finishing a bullet, apply the achievement test: delete the [Z] clause and check whether what remains still says something valuable on its own. If it does — it's a real achievement. If nothing meaningful is left — the bullet is describing a task or a decision, not an outcome. 

Never fabricate or embellish beyond what the underlying material supports, even in ways that don't feel like lying: turning "helped with a rebrand" into "helped *lead* a company rebrand," or inventing a plausible date range. Write the honest, flatter version, since a flat bullet is a smaller problem than a CV that overclaims.

Never quote a reference or recommendation letter as a bullet either. `selection.md` may cite a quote as evidence a soft-skill must-have is satisfied, which is fine for matching, but a CV bullet isn't a citation, so find the underlying fact the assessment was based on and write that instead. If there's no underlying fact to point to, the material wasn't well-selected, not a reason to quote the letter.

Write fragments, not full sentences, drop personal pronouns, leave off the trailing period, and keep each bullet to two rows at most. Don't write that something was "adopted" or "accepted." Usage and acceptance are implied by the outcome itself and by the fact the bullet exists at all, so stating it outright adds nothing and reads as an unearned credibility claim rather than a fact. No em dashes, en dashes, colons, or semicolons anywhere, replace with a comma, period, or rewrite the sentence, and no unicode math symbols, "R-squared" not "R²," "roughly 3 percent" or "within 3%" not "±3%," though plain `%` is fine.

### Writing the skills lines

Order skills within and across the 4 tailorable lines by relevance to `analysis.md`, most relevant first — a skill matching one of its exact keywords or a named must-have belongs ahead of one that doesn't. The category labels aren't fixed either: rename a line, or move a skill from one category to another, when that groups this posting's most relevant skills together more clearly than the baseline's own categories do. Fill the 4 lines with as many skills genuinely relevant to `analysis.md`'s keywords as the reconciliation rules above allow, rather than defaulting to however the baseline happened to group them.

Only the single most important line, the one most central to `analysis.md`'s "Role profile," can run to two rows. Every other tailorable line is capped at one row.

Expand domain-specific abbreviations wherever they appear — `RAG (Retrieval-Augmented Generation)`, `MCP (Model Context Protocol)`. A bare abbreviation should never appear with no expansion anywhere on the page. Skip this only for universally standard terms real resumes never spell out — GPA, IELTS.

The Languages line is copied from the baseline exactly, same order, regardless of this posting's relevance.

## Humanizing the draft

Run the drafted bullets and skills lines through `humanizer` before rendering — a required step, not optional polish, since unedited LLM tells undo the tailoring above. Do this before the final keyword check, not after, since humanizer can smooth away a deliberately-kept keyword; afterward, skim against `analysis.md`'s keyword list and restore anything lost.

## Rendering

Once the humanized draft is ready, render it:

```
uv run rendercv render data/applications/<slug>/cv.yaml
```

If the user later asks for a change to one bullet, a skills line, or any other tailorable entry, edit that field directly in `data/applications/<slug>/cv.yaml` and re-render. Re-run the humanizing pass on anything you rewrote, not just the first draft; a hand-edited follow-up can reintroduce the same tells the first pass removed.

## Checking row and page counts

Don't eyeball the PDF and guess — row-wrapping depends on font metrics, not something reliably judged from a glance. `scripts/page_usage.py` reads the rendered PDF alongside the source `cv.yaml` and reports raw numbers only, no pass/fail judgment of its own: total page count, and for every bullet and skills line, how many physical rows it occupies.

```
uv run python skills/curriculum-vitae/scripts/page_usage.py data/applications/<slug>/output/<Name>_CV.pdf
```

Trimming a bullet's wording, or dropping one item from a skills line, is otherwise off the table — the aim throughout is never to add or remove — but a measured overflow is the one exception. A bullet or skills line the script reports over its cap (two rows for a bullet, one row for a skills line, two only for the single most important one), or a CV the script reports at more than one page, gets trimmed, and only then: never preemptively, never because something merely looks long. When a skills line has to lose an item to fit, or a bullet has to lose a phrase, cut whatever contributes least to fit against "Role profile" or the posting's keywords first, not whatever's easiest to cut.

## After rendering

Tell the user the tailored CV PDF is ready and where it is, then ask if they want to review/correct it before treating it as final. Summarize what actually changed from the baseline — which bullets and skills were Reworded or Replaced, and why — so the user can review the judgment calls themselves instead of re-diffing the YAML. Reconciliation decisions built on `analysis.md`'s "Role profile" are a judgment call, not an extraction, so this is the checkpoint where the user can catch a bad call before it goes out — sending or submitting the application is a separate, manual step outside this skill's scope.
