# Pharmacy Direct Constitution

Pharmacy Direct dispenses prescription medication to patients. A defect here is not a bad
user experience, it is a patient receiving the wrong thing. These principles govern every
specification, plan and implementation in this repository, whether written by a person or
by an agent.

## Core Principles

### I. The specification is the source of truth

Work starts from a spec in `specs/`, not from a chat message. If the spec does not say it,
it is not in scope. If the spec is ambiguous, ask before implementing — a guess that
reaches a patient is worse than a question that delays a sprint.

### II. Security is part of done, not a later phase

Every change is reviewed for security **before** it is proposed for merge, using the skill
in `.github/skills/fortify-change-review/`. The review runs against the diff, not against
the whole codebase. Findings are reported with file, line, why it is exploitable and the
concrete fix.

This review does not replace the pipeline. The authoritative analysis runs in GitHub
Actions and publishes to the Security tab. A change is never described as "secure" because
this review passed — only as "no issues found in this review".

### III. Dependencies are decisions, not details

A new or upgraded dependency is checked against policy **before** it is written into
`pom.xml`. Prefer a version with no policy violations. If the component cannot be checked,
say so explicitly rather than assuming it is acceptable.

Every dependency added must be justified in the plan: what it does, why an existing
library cannot, and what the licence is.

### IV. A human approves

Automated tooling may find, classify, explain and propose. It does not merge. Every change
carries a named human who accepted it, and the reasoning behind that acceptance survives
in the pull request — six months later, an auditor must be able to read why.

### V. The existing weaknesses are the subject matter

This application deliberately contains insecure code, documented in `EXPLOITS.md`. Do not
silently "fix" vulnerabilities you were not asked to touch. Review and fix the change
currently being made, nothing else.

## Constraints

- Java 17, Spring Boot, Maven. Application code under `src/main/java/com/microfocus/example/`.
- Patient data is personal data. It is never written to logs, never included in an error
  message returned to a client, and never used in test fixtures.
- Any lookup by an identifier supplied by the client must verify that the caller is
  entitled to that record, and must not reveal whether a record exists otherwise.
- This application must never be deployed to a production environment.

## Workflow

`/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`

Each phase writes a file the next phase reads. The plan states which parts of this
constitution apply to the change and how they are satisfied. Anything that violates a
principle is raised in the plan, not discovered in review.

**Version**: 1.0.0 | **Ratified**: 2026-08-04 | **Last amended**: 2026-08-04
