# ZeroTrustDesktop-V2

ZeroTrustDesktop-V2 is the promoted, structured continuation of the original ZeroTrustDesktop work.
This version converts the legacy step-based security stack into a professional local-first desktop security and observability tool with a clean bootstrap, an easy launcher, and a modular Python package layout.

The goal of V2 is simple:

- keep the operator surface easy
- keep the internal architecture strong
- separate observation from enforcement
- preserve legacy work without mixing it into the active runtime
- provide a stable repo that can grow without turning back into a pile of loose scripts

---

## Core Purpose

ZeroTrustDesktop-V2 is designed to help inspect, observe, report on, and later harden a Linux desktop environment through a structured local workflow.

This repo is being built around these principles:

- local-first execution
- deterministic file structure
- readable output
- safe bootstrap and launcher workflow
- modular Python internals
- future support for baseline, drift detection, and controlled restore behavior

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

- `ZeroTrustDesktop-V2 0.1.0 (read-only baseline)`

This version marks the first structured read-only baseline with:

- launcher and direct wrapper
- shared config and path handling
- shared reporting and logging
- live `doctor`, `status`, `audit`, and `observe`
- guarded `apply` and `restore`

---

## Current Status

This repository is now in the scaffolded V2 phase.

What currently works:

- local repo structure is created
- bootstrap entrypoint exists
- launcher entrypoint exists
- direct CLI wrapper exists
- Python package layout exists
- output folders exist
- systemd placeholders exist
- legacy reference files are preserved in `legacy/`
- baseline commit is complete

What is being built next:

- real README contract
- config defaults
- repo-safe path handling
- config loader
- real launcher routing
- real doctor, audit, and status behavior

---

## Operator Workflow

### First-time setup

```bash
cd /home/pc-10/repos/ZeroTrustDesktop-V2 && ./bootstrap.sh