# Job Application Kit

A Claude Code plugin for preparing job applications one posting at a time: build up a career fact-base, analyze a job posting, select what genuinely fits, tailor a CV built with [rendercv](https://github.com/rendercv/rendercv), and write a matching cover letter — all as local files in this repo, no external job-board integration or batch scraping.

## Skills

| Skill | Does |
|---|---|
| `interviewer` | Interviews the user and writes structured, cited facts into `data/fact-base.md` |
| `job-analyzer` | Extracts requirements/keywords from one job posting, sets up `data/applications/<slug>/` |
| `fit-picker` | Matches a posting's requirements against `fact-base.md`, selecting cited material for that application |
| `curriculum-vitae` | Produces a per-application CV copy, reordered/reworded to match the posting (never inventing content) |
| `cover-letter` | Writes and renders a cover letter via a Typst ([letterloom](https://typst.app/universe/package/letterloom/)) template |

## Agent

| Agent | Does |
|---|---|
| `job-application-agent` | Chains `job-analyzer` → `fit-picker` → `curriculum-vitae` → `cover-letter` into one pipeline for a single job posting, pulling in `interviewer` first if the fact-base doesn't exist yet, or again mid-pipeline to fill a real gap |

## Command

| Command | Does |
|---|---|
| `/apply <job-url-or-description>` | Runs the orchestrator |

## Setup

```
uv sync
npx skills experimental_install -y
```

`npx` needs Node.js installed.

### Companion skills

Tracked in `skills-lock.json` and restored by `npx skills experimental_install -y` in one command:

- [`blader/humanizer`](https://github.com/blader/humanizer)

## Getting started

One-time, before tailoring anything: create your master CV and baseline cover letter, both live at the repo root's `data/` and get copied per application from there.

```
uv run rendercv new "Full Name"
mv Full_Name_CV.yaml data/cv.yaml

uv run rendercl new "Full Name"
mv Full_Name_CL.yaml data/cl.yaml
```

Both commands scaffold a realistic filled example, not a blank form. Replace every field in `data/cv.yaml` with your real career data. In `data/cl.yaml`, only `sender` needs to be your real, reusable details, everything else gets overwritten per application.

## Layout

See `data/README.md` for what lives under `data/` and how the per-application folders are structured.
