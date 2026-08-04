# Copilot instructions

This repository has security guidance available to you. Use it — do not wait to be asked.

## Before proposing a commit, a push, or a pull request

Run a security review of the change you just made, using the skill in
`.github/skills/fortify-change-review/`. Read `SKILL.md` first, then the reference files
under `references/` that match what the change actually touches.

Report findings the way the skill defines them: category, severity, the exact file and
line, why it is exploitable, and the concrete fix. If a change is clean, say so plainly
rather than inventing findings.

## Dependencies

When adding, upgrading or replacing a dependency, check it against policy before writing
it into the build file. If a Sonatype MCP server is available in this workspace, use it to
look up the component and prefer a version without policy violations. If it is not
available, state that the component has not been checked rather than assuming it is fine.

## What this review is and is not

This is a fast local check that catches the obvious things before they leave the machine.
It does **not** replace the pipeline. The authoritative analysis runs in GitHub Actions
(SAST and SCA) and publishes to the Security tab. Never describe a change as "secure"
because this review passed — describe it as "no issues found in this review".

## Repository specifics

- Java 17, Spring Boot, Maven. Application code lives under `src/main/java/com/microfocus/example/`.
- This application contains **deliberately vulnerable code** for demonstration purposes.
  Do not silently "fix" existing vulnerabilities you were not asked to touch — they are the
  subject matter. Only review and fix the change currently being made.
- `EXPLOITS.md` documents the intentional weaknesses.
