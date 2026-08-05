# Specifications

Feature specifications for Pharmacy Direct. A spec is the source of truth: it describes
what the feature must do and how we will know it works. An agent reads the spec, proposes
a plan, breaks it into tasks and implements it. A human reviews and approves.

Written to be compatible with [GitHub Spec Kit](https://github.com/github/spec-kit)
(`/specify` → `/plan` → `/tasks` → `/implement`), but readable on their own.

## Working agreement for agents

Before the implementation of any spec is proposed for merge:

1. Run the review skill in `.github/skills/fortify-change-review/` against the diff.
2. Check every new or changed dependency against policy before it goes into `pom.xml`.
3. State clearly what was checked and what was not. See `.github/copilot-instructions.md`.

The pipeline still runs afterwards. These steps make it likely to be green, they do not
replace it.

## Where the backlog lives

Feature requests are raised as [issues](../../issues) so the whole team can see what is
planned, discuss it and pick it up. An issue that is picked up becomes a spec file here.
The issue stays the place for discussion; this directory holds the agreed wording.

| Spec | Feature | Issue | Status |
|---|---|---|---|
| [SPEC-001](SPEC-001-repeat-prescription.md) | Repeat prescription ordering | #25 | Ready for implementation |
| [SPEC-002](SPEC-002-order-receipt.md) | Downloadable order receipt | #26 | Ready for implementation |

Everything else is still an issue. There are two labels, and they exist because they
change how the work is done:

- `dependency` — introduces a third-party component. It is checked against policy
  **before** it reaches `pom.xml`.
- `security` — touches authentication, authorisation, uploads, input handling or
  outbound calls. The change review runs against the diff before merge.
