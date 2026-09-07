# Loop Task Contract

Each loop task must have a task-specific prompt that explicitly declares the following fields before implementation begins.

## Required fields

```text
Task ID:
Task type:
Goal:
Risk class: R0 / R1 / R2 / R3
Agent topology:
Specialist triggers:
Base branch:
Writable paths:
Read-only reference paths:
Maximum implementation iterations:
Maximum review correction cycles:
Acceptance criteria:
Required verification:
Hardware evidence required:
Explicitly forbidden actions:
```

Default multi-agent behavior is defined in `docs/feather-quantizer/loop/MULTI_AGENT.md`.

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

## Risk class

Choose one:

```text
R0  trivial / non-behavioral docs or metadata
R1  normal engineering
R2  high-risk hardware / security / architecture / protocol
R3  control-plane / protected / dependency boundary requiring human authority
```

R1 default topology:

```text
Planner -> Runner -> CI -> Reviewer -> Human merge
```

R2 default topology:

```text
Planner -> Runner -> CI -> Reviewer + Specialist Reviewer -> Human merge/checkpoint
```

R3 does not authorize implementation. The default action is `STOP / ESCALATE_HUMAN` until explicit authorization exists.

For R0, Reviewer may be omitted only if the task contract or human explicitly permits it.

## Agent topology

Declare the roles expected for the task:

```text
Planner: REQUIRED / SKIPPABLE_EXISTING_CONTRACT
Runner: REQUIRED
Reviewer: REQUIRED / OPTIONAL_R0
Specialist: NONE / HARDWARE_EVIDENCE / SECURITY_PRIVACY / ARCHITECTURE / DEPENDENCY_TOOLCHAIN / HID_PROTOCOL
```

Multiple specialist domains may be listed when justified, but do not add agents without a concrete risk trigger.

The Planner does not implement product code. The Runner does not approve itself. Reviewer and Specialist roles are independent/read-only by default.

## Specialist triggers

Explicitly evaluate these domains:

```text
HARDWARE_EVIDENCE
SECURITY_PRIVACY
ARCHITECTURE
DEPENDENCY_TOOLCHAIN
HID_PROTOCOL
```

Each task contract should mark every domain `REQUIRED` or `NOT_REQUIRED` with a short reason. A required specialist must return `CLEAR` before a candidate can receive final Reviewer `APPROVE`.

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

The Runner may add a smaller diagnostic command during an iteration, but may not weaken the required final verification.

CI/deterministic checks are not replaced by an agent Reviewer. The Reviewer audits the evidence and intent; CI executes reproducible checks.

## Hardware evidence declaration

Set one of:

```text
NONE
REQUIRED_FOR_PASS
EXPECTED_CHECKPOINT
```

If `REQUIRED_FOR_PASS` and the hardware is not accessible, the correct Runner result is `BLOCKED_HARDWARE`, not PASS.

A hardware procedure with safety/privacy/HID interpretation risk should normally trigger the appropriate Specialist Reviewer before human execution.

## Review-cycle declaration

Default:

```text
Maximum review correction cycles: 2
```

A review correction cycle is:

```text
Reviewer REQUEST_CHANGES
  -> Runner correction
  -> CI
  -> independent re-review
```

Any Runner correction that changes project files still consumes a normal implementation iteration. Review cycles never reset the implementation counter.

If BLOCKER/MAJOR findings remain after the maximum review correction cycles, escalate to the human instead of continuing indefinitely.

## Draft PR handoff policy

The default inner-PR policy for every loop task is:

```text
DRAFT_INNER_PR_WHEN_PLATFORM_SUPPORTS_IT
```

A task-specific prompt does not need to repeat this default unless it intentionally changes the handoff behavior with explicit human authorization.

When the Runner reaches `PASS`, `BLOCKED_HARDWARE`, `BLOCKED_ENVIRONMENT`, or `STOP`, it should create or update one Draft PR from its working branch to the declared loop task `Base branch` when the execution platform exposes an authorized PR action.

Draft PR creation is a delivery step. It does not authorize the Runner to:

- approve its own work;
- mark the PR ready for review;
- merge or enable auto-merge;
- retarget to `feather-main`;
- create an upstream PR;
- provision or request a PAT, SSH key, or other long-lived credential.

If no platform-supported PR action is available, the task may still complete or block normally. The final report must provide the exact head/base branch pair for manual PR creation.

## Independent review gate

For R1/R2 tasks, a candidate is not merge-ready solely because Runner status is PASS.

Required sequence:

```text
Runner terminal candidate
-> CI / deterministic verification
-> independent Reviewer
-> required Specialist(s)
-> human merge authority
```

General Reviewer verdict must be `APPROVE`; required Specialist verdicts must be `CLEAR`.

`REQUEST_CHANGES` returns to Runner within the same task contract. `ESCALATE_HUMAN` stops autonomous progress until the human decides.

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

The Runner may declare task state `PASS` only after the task contract, `QUALITY_GATES.md`, and `STOP_CONDITIONS.md` agree that the implementation/evidence is complete.

`PASS` is a Runner/task-state claim, not self-approval. For R1/R2 work, merge readiness additionally requires the independent review gate above.

Creating a Draft PR is not a PASS criterion by itself and does not change task status. A platform limitation that prevents automated PR creation/review is a handoff limitation, not a reason to falsify `BLOCKED_ENVIRONMENT` or `STOP` when the engineering task itself is otherwise complete.
