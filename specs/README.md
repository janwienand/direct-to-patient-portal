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

| Spec | Feature | Status |
|---|---|---|
| [SPEC-001](SPEC-001-repeat-prescription.md) | Repeat prescription ordering | Ready for implementation |
| [SPEC-002](SPEC-002-order-receipt.md) | Downloadable order receipt | Ready for implementation |
