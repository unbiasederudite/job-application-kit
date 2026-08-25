# data/

Generated and edited by this plugin's skills — not hand-authored from scratch.

- `fact-base.md` — the user's career record (built up by `interviewer`). Doesn't exist until you run it for the first time.
- `cv.yaml` — the master CV. Doesn't exist until you scaffold it with `rendercv new` (see the repo README's "Getting started").
- `cl.yaml` — the master baseline cover letter. Doesn't exist until you scaffold it with `rendercl new` (see the repo README's "Getting started").
- `applications/<company-slug>-<role-slug>/` — one folder per job application (created by `job-analyzer`):
  - `posting.md` — the raw job posting, copied verbatim (`job-analyzer`)
  - `analysis.md` — extracted requirements, keywords, and role profile (`job-analyzer`)
  - `selection.md` — fact-base material selected as fitting this posting, cited back to its source (`fit-picker`)
  - `cv.yaml` — tailored copy of the master CV for this posting (`curriculum-vitae`)
  - `cl.yaml` — tailored copy of the master cover letter for this posting (`cover-letter`)
  - `output/` — rendered PDFs/Typst/HTML/etc. for both the CV and cover letter — gitignored, regenerate from the YAML sources

This file is the only thing in `data/` meant to be read rather than generated.
