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

This version marks the first structured read-only baseline with:

- polished launcher and direct wrapper
- shared config and repo-safe path handling
- shared reporting and logging
- live `doctor`, `status`, `audit`, and `observe`
- guarded `apply` and `restore`
- deterministic smoke tests
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
- shared logging works
- live `doctor` module works
- live `status` module works
- live `audit` module works
- live `observe` module works
- guarded `apply` and `restore` handlers refuse by default
- test suite passes
- legacy reference files are preserved in `legacy/`

What is next:

- deepen `observe` with artifact age and freshness analysis
- continue strengthening read-only observability before enabling any real enforcement behavior
- preserve deterministic phase-based upgrades instead of restructuring the repo again

---

## Operator Workflow

### First-time setup

```bash
cd /home/pc-10/repos/ZeroTrustDesktop-V2 && ./bootstrap.sh