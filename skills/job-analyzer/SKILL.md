---
name: job-analyzer
description: Analyze a single job posting (a URL or pasted job description text) and extract a structured summary of requirements, keywords, seniority, and likely ATS terms, then set up that application's working folder under data/applications/. Use this whenever the user shares a job posting URL or pastes a job description and wants to apply, understand fit, or prepare tailored materials for it. This is the entry point for a new application — tailor-cv and cover-letter both expect this skill's output to already exist. Handles exactly one job posting at a time; this kit does not do batch or automated scraping across job boards.
---

# Job Analyzer

Turns one job posting into a structured brief of its requirements and keywords, and creates the folder that holds everything for that application.

## Inputs

Accept either:
- A URL to a job posting — fetch it (WebFetch) and extract the visible posting text. Job boards vary wildly in markup; if the fetch comes back mostly navigation/boilerplate, ask the user to paste the description text instead rather than guessing at a bad extraction.
- Pasted job description text directly.

This skill only ever handles one posting per invocation. If the user pastes multiple postings or a list of URLs, ask which one to start with — don't try to batch them.

## What to produce

Derive a slug: `<company-slug>-<role-slug>`, lowercase, hyphens, no punctuation (e.g. `acme-corp-senior-backend-engineer`). If a folder with that slug already exists under `data/applications/`, ask whether this is a re-analysis of the same posting or a genuinely different one before overwriting anything.

Create `data/applications/<slug>/`, with `posting.md` (the raw posting, verbatim — title, company, and full description text) and `analysis.md` (your structured extraction):

```markdown
# <Role Title> — <Company>

## Must-haves
- (requirements phrased as blockers — "5+ years", "must have X certification")

## Strong preferences
- (listed as nice-to-have but clearly weighted by the posting)

## Keywords for ATS matching
- (exact phrases/terms from the posting worth mirroring verbatim in a tailored CV — tools, methodologies, job titles)

## Seniority & scope signals
- (team size, reporting line, scope of ownership implied by the posting's language)

## Notable gaps vs. a typical candidate
- (things the posting asks for that are easy to overlook when tailoring)

## Company/role context worth mentioning in a cover letter
- (mission, product, team framing — anything specific enough to prove the letter isn't generic)
```

Extract, don't editorialize — pull language straight from the posting for must-haves and keywords so downstream tailoring can mirror real ATS terms instead of paraphrases. Save the editorializing (fit assessment, gap flags) for the sections that call for it.

## After analysis

Tell the user what you found — a short summary of must-haves and any notable gaps — and ask if they want to proceed straight to tailoring, or review/correct `analysis.md` first. Don't chain into tailoring automatically.
