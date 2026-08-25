---
description: Run the full job-application pipeline (analyze posting, select fitting material, tailor CV, write cover letter) for one job posting at a time
argument-hint: <job-url-or-pasted-description>
---

Run the `job-application-agent` agent for the following job posting: $ARGUMENTS

If no posting was provided above, ask the user to paste a job URL or the full job description text before proceeding — this command handles exactly one posting per invocation, not a batch.
