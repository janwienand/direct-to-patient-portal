# Agent skills

Skills made available to AI coding agents working in this repository.

## fortify-change-review

Lightweight, AI-powered security review of code *changes* — a diff, a PR, or edits an
agent is making right now. Runs on the agent's own analysis; no Fortify scan engine,
no platform connection, no fcli required.

Typical use, before pushing:

```
Use the fortify-change-review skill to review my uncommitted changes (`git diff HEAD`)
and tell me whether this is safe to push.
```

Vendored from [fortify/skills](https://github.com/fortify/skills) v1.3.0, MIT licensed,
Copyright (c) 2026 OpenText Corporation. Update by re-copying
`skills/fortify-change-review/` from that repository.
