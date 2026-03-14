# ZeroTrustDesktop-V2

ZeroTrustDesktop-V2 is the promoted, structured continuation of the original ZeroTrustDesktop work.
This version converts the legacy step-based security stack into a professional local-first desktop security and observability tool with a clean bootstrap flow, an easy launcher, and a modular Python package layout.

The goal of V2 is simple:

- keep the operator surface easy
- keep the internal architecture strong
- separate observation from enforcement
- preserve legacy work without mixing it into the active runtime
- provide a stable repo that can grow without turning back into a pile of loose scripts

---

## Core Purpose

ZeroTrustDesktop-V2 is designed to help inspect, observe, report on, and later harden a Linux desktop environment through a structured local workflow.

This repo is built around these principles:

- local-first execution
- deterministic file structure
- readable output
- safe bootstrap and launcher workflow
- modular Python internals
- controlled expansion from read-only observability into future guarded enforcement

---

## V2 Design Goals

V2 exists to replace the older step-based workflow with a real application boundary.

The promoted design introduces:

- one repo root
- one bootstrap flow
- one launcher flow
- one direct CLI wrapper
- one Python package
- one output contract
- one clean separation between active code and legacy reference files

---

## Version

Current version:

- `ZeroTrustDesktop-V2 0.1.1 (read-only baseline)`

This version marks the structured read-only baseline with:

- polished launcher and direct wrapper
- shared config and repo-safe path handling
- shared reporting and logging
- live `doctor`, `status`, `audit`, and `observe`
- guarded preview `apply` and `restore`
- read-only `state` capture
- read-only `diff` artifact generation
- deterministic smoke and module tests
- synced GitHub remote baseline

---

## Current Status

This repository is now in the **0.1.1 read-only baseline** phase.

What currently works:

- local repo structure is stable
- bootstrap entrypoint works
- launcher entrypoint works
- direct CLI wrapper works
- Python package layout is active
- shared config loading works
- repo-safe path handling works
- shared JSON and markdown reporting works
- shared console and file logging works
- live `doctor` module works
- live `status` module works
- live `audit` module works
- live `observe` module works
- guarded preview `apply` works
- guarded preview `restore` works
- read-only `state` capture works
- read-only `diff` artifact generation works
- test suite passes
- legacy reference files are preserved in `legacy/`

What is next:

- preview artifact summaries
- state-aware status reporting
- observe + state convergence
- audit severity expansion
- doctor threshold checks
- dry-run enforcement planning
- 0.1.2 checkpoint

---

## Next 7 Goals

1. **Preview artifact summaries**
   - Extend `apply` and `restore` preview output to summarize latest `doctor`, `audit`, `observe`, `state`, and `diff` artifacts in one place.
   - Keep behavior read-only.

2. **State-aware status reporting**
   - Extend `status` so it reports latest state file, latest diff file, diff status, and changed count.
   - Make repo/runtime posture visible from one command.

3. **Observe + state convergence**
   - Wire `observe` to report latest state/diff freshness and age alongside doctor/report freshness.
   - Unify observability around artifact age and drift visibility.

4. **Audit severity expansion**
   - Expand `audit` to classify state/diff conditions as informational, warning, or critical.
   - Preserve deterministic summary counts and overall result.

5. **Doctor threshold checks**
   - Add threshold-style checks for disk free space, required binary presence, and basic runtime expectations.
   - Keep outputs structured and testable.

6. **Dry-run enforcement planning**
   - Introduce deterministic dry-run planning for future firewall/runtime actions without performing changes.
   - Output planned actions into reports only.

7. **0.1.2 checkpoint**
   - After preview/report integration is stable, bump from `0.1.1` to `0.1.2`.
   - Update tests, README, and version identity together in one clean checkpoint.

---

## Operator Workflow

### First-time setup

```bash
cd /home/pc-10/repos/ZeroTrustDesktop-V2 && ./bootstrap.sh
