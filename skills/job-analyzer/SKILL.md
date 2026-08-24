---
name: job-analyzer
description: Analyze a single job posting (a URL or pasted job description text) and extract a structured summary of requirements, keywords, and a synthesized profile of who the role is really for, then set up that application's working folder under data/applications/. Use this whenever the user shares a job posting URL or pastes a job description and wants to apply, understand fit, or prepare tailored materials for it. This is the entry point for a new application — every downstream skill in this kit expects this skill's output to already exist. Handles exactly one job posting at a time; this kit does not do batch or automated scraping across job boards.
---

# Job Analyzer

Turns one job posting into a structured brief of its requirements and keywords, and creates the folder that holds everything for that application.

## Inputs

Accept either:
- A URL to a job posting — fetch the raw page with `curl` (via Bash), never WebFetch. WebFetch routes everything through a small model that paraphrases the page on the way back, so anything built from it is already a paraphrase before you've written a word — curl returns the real page content, and you copy the actual posting text out of it yourself, verbatim, not reworded or reordered even lightly. If curl comes back JS-rendered, garbled, blocked, or otherwise unusable, don't fall back to WebFetch — tell the user and ask them to paste the job description text into the chat instead.
- Pasted job description text directly.

This skill only ever handles one posting per invocation. If the user pastes multiple postings or a list of URLs, ask which one to start with — don't try to batch them.

## What to produce

Derive a slug: `<company-slug>-<role-slug>`, lowercase, hyphens, no punctuation (e.g. `acme-corp-senior-backend-engineer`). If a folder with that slug already exists under `data/applications/`, ask whether this is a re-analysis of the same posting or a genuinely different one before overwriting anything.

Create `data/applications/<slug>/`, with `posting.md` (the raw posting, copied verbatim — title, company, and full description text, kept as an archival record) and `analysis.md` (your structured extraction). `analysis.md` is the only file downstream skills read from here on — none of them open `posting.md` — so it has to carry everything a person would need to understand the posting without going back to the source:

```markdown
# <Role Title> — <Company>

## Must-haves
- (requirements phrased as blockers — "5+ years", "must have X certification")

## Strong preferences
- (listed as nice-to-have but clearly weighted by the posting)

## Keywords for ATS matching
- (exact phrases/terms from the posting worth mirroring verbatim in a tailored CV — tools, methodologies, job titles)

## Role profile
(prose, not bullets — see below)

## Hiring contact
(name/title, if the posting names one — see below)

## Headquarters
(address, if found — see below)
```

Extract, don't editorialize — pull language straight from the posting for must-haves and keywords so downstream tailoring can mirror real ATS terms instead of paraphrases.

### Role profile

This section is the one place downstream skills get any sense of the posting's *shape*, since they won't read the posting itself. Write it as connected prose, a paragraph or two, not another bulleted checklist — bullets flatten emphasis, and emphasis is the entire point of this section. A must-have mentioned once and a theme repeated three times across the posting should not read as equally weighted here.

Cover what a person would actually notice reading the whole posting once: who this role is really for and what it centers on day to day, what's clearly central versus what's mentioned once in passing, seniority and scope (team size, reporting line, ownership vs. support), and tone. If something in the posting's own framing would change how a reader should weigh a must-have or preference — a "strong advantage" that's mentioned three times and clearly matters more than its label suggests, or a listed requirement that's contradicted by everything else the posting emphasizes — say so here explicitly, since this is the only place that judgment call gets recorded.

### Hiring contact and headquarters

If the posting names a specific hiring contact (a recruiter or hiring manager) with a name, a title, or both, add that to the `## Hiring contact` section. If the posting doesn't name anyone, omit the section entirely — don't search for one or guess.

For the company's headquarters address, check the posting itself first. If it's not stated there, search the web for it. Add whatever address you find, from either source, to the `## Headquarters` section. If neither the posting nor a web search turns up a real address, omit the section entirely.

## After analysis

Tell the user what you found — a short summary of must-haves and strong preferences, plus how you read "Role profile" (what you concluded the role is really for and centers on) — and ask if they want to proceed straight to tailoring, or review/correct `analysis.md` first. "Role profile" is a judgment call, not an extraction, and every downstream skill trusts it without re-deriving it, so this is the one moment the user can catch a misread before it quietly shapes everything after it. Don't chain into tailoring automatically.
