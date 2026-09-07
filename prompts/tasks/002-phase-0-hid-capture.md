# Task 002 — Phase 0 HID capture procedure and evidence schema

Use `prompts/loop-runner.md` as the execution protocol for this task.

## Task contract

**Task ID:** 002

**Task type:** documentation

**Goal:** Define a reproducible, non-destructive Phase 0 procedure and evidence schema for capturing the USB/HID characteristics required to evaluate ELECOM DEFT and ELECOM HUGE PLUS compatibility before Feather firmware implementation begins.

**Base branch:** `loop/002-phase-0-hid-capture` (create this branch from `feather-main` only after the Loop Engineering infrastructure task has been merged)

**Writable paths:**

```text
docs/feather-quantizer/phase-0-capture.md
docs/feather-quantizer/research/hid-captures/**
docs/feather-quantizer/loop/runs/002-phase-0-hid-capture/**
```

**Read-only reference paths:**

```text
keyboards/sekigon/**
FEATHER_QUANTIZER.md
docs/feather-quantizer/spec.md
docs/feather-quantizer/research/task-001-upstream-analysis.md
AGENTS.md
.github/workflows/**
```

**Maximum implementation iterations:** 3

**Hardware evidence required:** NONE for Task 002 PASS. This task defines the procedure/schema only; it must not claim that DEFT/HUGE PLUS hardware was captured or verified.

## Acceptance criteria

### AC1 — Capture procedure

Create `docs/feather-quantizer/phase-0-capture.md` containing a step-by-step, non-destructive procedure that defines how a human will capture:

- USB VID/PID and product/revision strings;
- device/configuration/interface/endpoint information;
- complete HID report descriptor for every HID interface;
- report IDs and exact report lengths;
- timestamped raw input reports;
- button press/release samples;
- positive/negative X and Y movement;
- vertical wheel both directions;
- horizontal tilt/pan both directions when present;
- simultaneous input examples;
- vendor-defined reports/usages;
- maximum observed input report length.

The procedure must separate wired and 2.4 GHz receiver modes when applicable.

### AC2 — Target-device matrix

The procedure explicitly identifies:

```text
Current initial device: ELECOM DEFT (exact product number still to be recorded by human)
Primary future target: ELECOM HUGE PLUS
```

Do not invent the exact DEFT model number.

Define a capture matrix for every applicable connection mode without claiming results.

### AC3 — Evidence naming/schema

Create `docs/feather-quantizer/research/hid-captures/README.md` defining deterministic names and metadata for future evidence, including at least:

```text
<device>/<connection-mode>/device-metadata.json
<device>/<connection-mode>/hid-interface-<n>-report-descriptor.bin
<device>/<connection-mode>/hid-interface-<n>-report-descriptor.txt
<device>/<connection-mode>/input-reports.ndjson
<device>/<connection-mode>/stimulus-checklist.md
```

The schema must distinguish observed bytes from interpretation/annotation.

### AC4 — KQM compatibility checks

The procedure must explicitly compare future evidence against current KQM constraints discovered in Task 001:

- one shared 64-byte HID report buffer;
- `CFG_TUH_DEVICE_MAX=4`;
- `CFG_TUH_HID=8`;
- parser pools: 8 devices / 16 collections / 32 members / 32 usages;
- Vial mouse path currently reduces actionable buttons to 8 bits;
- horizontal pan may use Consumer AC Pan or another/vendor usage.

Cite the repository source/report that establishes each constraint.

### AC5 — Feather safety boundary

Document GP16/GP17 as the intended Feather USB host data pair only as a project requirement already established in project documentation.

For GP18 VBUS enable, do not invent polarity or timing. The procedure must say how the human will verify/record the authoritative polarity/timing source before a later hardware task uses it.

No hardware flashing is performed in Task 002.

### AC6 — No compatibility claim

The completed documents explicitly state that Task 002 does **not** prove DEFT or HUGE PLUS compatibility. Actual compatibility requires later hardware evidence.

### AC7 — Loop evidence

Create/update:

```text
docs/feather-quantizer/loop/runs/002-phase-0-hid-capture/state.json
docs/feather-quantizer/loop/runs/002-phase-0-hid-capture/iterations.md
```

The final `state.json` must be valid and may be `PASS` only when AC1..AC7 are all PASS and the applicable Hard Gates pass.

## Required final verification

Run what the environment permits and report exact results:

```bash
python3 scripts/feather-quantizer/verify-loop-state.py docs/feather-quantizer/loop/runs/002-phase-0-hid-capture/state.json
bash scripts/feather-quantizer/verify-task.sh
git diff --check
git status --short
git diff --stat
git diff --name-only
```

If the Codex workspace cannot resolve the declared base ref for `verify-task.sh`, do not change Git history/remotes to work around it. Record the environment limitation and rely on repository CI for that check; all other locally available static checks should still run.

No firmware build is required specifically for this documentation-only task, but repository CI must not regress the existing KQM baseline check.

## Explicitly forbidden

Do not:

- modify firmware source;
- modify `keyboards/sekigon/**`;
- modify `keyboards/feather_quantizer/**`;
- modify workflows or AGENTS.md;
- update dependencies/submodules/toolchain;
- invent HID bytes/descriptors;
- claim DEFT/HUGE PLUS compatibility;
- flash hardware;
- create an upstream PR.

## Expected final status

This task should normally finish as `PASS` because it is documentation/schema preparation only. If a required procedural fact cannot be stated without inventing hardware behavior, use the safest evidence-recording wording and identify the later hardware checkpoint instead of guessing.
