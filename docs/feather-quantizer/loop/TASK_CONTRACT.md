# Loop Task Contract

Each loop task must have a task-specific prompt that explicitly declares the following fields before implementation begins.

## Required fields

```text
Task ID:
Task type:
Goal:
Base branch:
Writable paths:
Read-only reference paths:
Maximum implementation iterations:
Acceptance criteria:
Required verification:
Hardware evidence required:
Explicitly forbidden actions:
```

## Task types

Use one primary type:

```text
analysis
documentation
board-port
hid-parser
gesture
vial-integration
hardware-verification
infrastructure
```

A task should not combine unrelated types merely to save PRs.

## Writable scope

The task must list exact writable prefixes/files. The default firmware scope remains:

```text
keyboards/feather_quantizer/**
docs/feather-quantizer/**
```

Prompts/scripts may be writable only when the task explicitly includes them.

Control-plane files require explicit human authorization:

```text
AGENTS.md
.github/workflows/**
.gitmodules
```

Shared upstream paths remain read-only by default.

## Acceptance criteria

Acceptance criteria must be observable and binary enough to review.

Bad:

```text
Make USB support robust.
```

Good:

```text
- `make feather_quantizer:vial:uf2` exits 0.
- `.build/*feather_quantizer*.uf2` exists.
- original KQM baseline build still exits 0.
- no protected path is modified.
```

Hardware criteria must name the device and evidence.

Example:

```text
- On ELECOM DEFT 2.4 GHz receiver, capture and commit the HID report descriptor for every HID interface.
- Record exact report IDs and maximum observed input report length.
```

## Verification declaration

Before editing, the task prompt must say which checks are required to claim PASS.

Possible checks include:

```text
bash scripts/feather-quantizer/verify-task.sh
make sekigon/keyboard_quantizer/mini:vial:uf2
make feather_quantizer:vial:uf2
unit/parser fixture tests
hardware evidence checklist
```

The agent may add a smaller diagnostic command during an iteration, but may not weaken the required final verification.

## Hardware evidence declaration

Set one of:

```text
NONE
REQUIRED_FOR_PASS
EXPECTED_CHECKPOINT
```

If `REQUIRED_FOR_PASS` and the hardware is not accessible, the correct result is `BLOCKED_HARDWARE`, not PASS.

## Run files

Each task must maintain:

```text
docs/feather-quantizer/loop/runs/<task-slug>/state.json
docs/feather-quantizer/loop/runs/<task-slug>/iterations.md
```

The prompt itself should live at:

```text
prompts/tasks/<task-id>-<slug>.md
```

## Completion

The agent may declare `PASS` only after the task contract, `QUALITY_GATES.md`, and `STOP_CONDITIONS.md` all agree that the task is complete.
