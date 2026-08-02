# Audit/ — where you run real engagements

**This folder ships EMPTY except this README. That is by design.**

Each project gets its own folder here, structured like this:

```
Audit/
  <ProjectName>/          <- you create this (any name)
    evidence/              <- you create this, and fill it with your delivery artifacts
    reports/                <- the engine creates this and writes into it
```

- **`evidence/`** — your responsibility. Drop the project's delivery artifacts here (schedules,
  RAID logs, cost trackers, status reports — whatever the audit needs to read). Point the
  `intelligence-engine` skill at this folder to start an audit.
- **`reports/`** — the engine's responsibility. The Audit Manifest, canonical findings JSON, and
  rendered HTML/TXT reports are all written here automatically, as a sibling of `evidence/`. You
  don't create this folder yourself.

Everything under `Audit/` (except this README) is **gitignored** — local-only, never committed.
Real engagement evidence and the reports generated from it are not example/demo data, so they
don't go into git history by default.

This is separate from `examples/` at the repository root, which holds curated, committed demo
audits and is unaffected by this folder.
