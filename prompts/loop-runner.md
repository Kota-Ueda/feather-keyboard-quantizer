# Codex Loop Runner — Feather Keyboard Quantizer

You are executing a bounded loop engineering task in this repository.

## Mandatory reading

Before changing anything, read in this order:

1. `AGENTS.md`
2. `FEATHER_QUANTIZER.md`
3. `docs/feather-quantizer/spec.md`
4. `docs/feather-quantizer/upstream-policy.md`
5. `docs/feather-quantizer/guardrails.md`
6. `docs/feather-quantizer/loop/LOOP.md`
7. `docs/feather-quantizer/loop/TASK_CONTRACT.md`
8. `docs/feather-quantizer/loop/QUALITY_GATES.md`
9. `docs/feather-quantizer/loop/STOP_CONDITIONS.md`
10. the task-specific prompt supplied by the human

Then inspect:

```bash
git status --short
git diff --stat
git diff --name-only
```

Do not clean, reset, or rewrite unrelated pre-existing changes.

## Task contract is authoritative

Extract and restate before implementation:

- Task ID
- Goal
- Base branch
- writable paths
- read-only/protected paths
- maximum implementation iterations
- acceptance criteria
- required verification
- hardware evidence requirement
- forbidden actions

If the task contract is incomplete or conflicts with repository guardrails, STOP and ask for human clarification. Do not infer broader authorization.

## Loop algorithm

For each implementation iteration, do exactly:

```text
OBSERVE
  -> identify one concrete failure/evidence gap
HYPOTHESIZE
  -> state one primary causal hypothesis
PLAN
  -> choose the smallest coherent test/change
IMPLEMENT
  -> modify only authorized files
VERIFY
  -> run the smallest relevant check/build/test
RECORD
  -> append iterations.md and update state.json
DECIDE
  -> PASS / CONTINUE / BLOCKED_HARDWARE / BLOCKED_ENVIRONMENT / STOP
```

Do not make a second unrelated implementation change in the same iteration.

## Limits

- Never exceed the task's declared `max_iterations`.
- `max_iterations` must be 1..5.
- If the same unresolved failure appears twice consecutively without materially new evidence, STOP.
- Do not reset counters by renaming/rephrasing the same hypothesis.

## Hard stop boundaries

STOP before doing any of the following unless the task explicitly contains human authorization for that exact action/path:

```text
edit keyboards/sekigon/**
edit lib/**
edit platforms/**
edit quantum/**
edit tmk_core/**
edit .gitmodules
update QMK/Vial/TinyUSB/Pico-PIO-USB/pico-sdk/ChibiOS
update submodule revisions
change compiler/toolchain versions
edit AGENTS.md
edit .github/workflows/**
force-push or rewrite history
flash hardware
create releases
modify upstream repositories
```

If a protected/shared change appears necessary, document the exact required seam and STOP.

## Hardware boundary

Compilation is not hardware verification.

If the next conclusion requires an actual Feather, DEFT, HUGE PLUS, USB receiver, HID descriptor, real report bytes, gesture feel, Vial persistence, suspend/resume, or hot-plug evidence that is not already in the repository:

1. set status to `BLOCKED_HARDWARE`;
2. describe the exact non-destructive human procedure;
3. describe the exact evidence file/format needed;
4. STOP.

Never invent hardware results.

## Run state

Maintain the task's run directory:

```text
docs/feather-quantizer/loop/runs/<task-slug>/state.json
docs/feather-quantizer/loop/runs/<task-slug>/iterations.md
```

`state.json` must follow `docs/feather-quantizer/loop/state.schema.json`.

Do not erase previous iteration history. Correct earlier mistakes in a later iteration.

## Verification before PASS

At minimum run:

```bash
bash scripts/feather-quantizer/verify-task.sh
```

plus every task-specific required verification.

For firmware tasks, repository CI is the authoritative build evidence when the Codex environment lacks the QMK/ARM toolchain.

Before declaring PASS also run/report:

```bash
git diff --check
git status --short
git diff --stat
git diff --name-only
```

## PASS criteria

You may set status to `PASS` only when:

- every acceptance criterion is PASS with explicit evidence;
- all applicable HG1..HG10 hard gates are PASS or explicitly NA;
- no gate is FAIL or UNKNOWN;
- quality score >= 90;
- iteration count <= max_iterations;
- required hardware evidence exists;
- no stop condition remains active.

If not, use CONTINUE/BLOCKED/STOP honestly.

## Final response

Report:

```text
Status:
Iterations used:
Files changed:
Acceptance criteria:
Hard gates:
Quality score:
Verification performed:
Hardware evidence:
Unresolved risks/blockers:
Recommended next task:
```

Do not merge the PR. Do not flash hardware. Human review is required.
