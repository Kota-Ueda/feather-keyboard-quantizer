# AGENTS.md — Feather Keyboard Quantizer

## Mission

Develop a Feather RP2040 USB Host implementation of Keyboard Quantizer functionality while keeping the `sekigon-gonnoc/vial-qmk` upstream code as unchanged as possible.

The primary target is ELECOM HUGE PLUS; ELECOM DEFT is the initial test device.

## Read before working

Before changing anything, read:

1. `FEATHER_QUANTIZER.md`
2. `docs/feather-quantizer/spec.md`
3. `docs/feather-quantizer/upstream-policy.md`
4. `docs/feather-quantizer/guardrails.md`
5. for `loop/*` tasks, all files under `docs/feather-quantizer/loop/` that define the loop protocol
6. the task-specific prompt or issue

Then inspect `git status --short` and the existing diff.

## Source-of-truth rule

Existing KQM Mini code under `keyboards/sekigon/**` is upstream reference code. Treat it as read-only unless the human explicitly authorizes a specific upstream-path edit in the current task.

Do not update QMK, Vial, TinyUSB, Pico-PIO-USB, pico-sdk, ChibiOS, submodule revisions, or toolchain versions as part of an implementation task unless the task explicitly says to do so.

## Default writable scope

For firmware implementation tasks, changes are limited to:

- `keyboards/feather_quantizer/**`
- `docs/feather-quantizer/**`
- task-specific files under `prompts/**` only when explicitly requested
- `scripts/feather-quantizer/**` only when explicitly requested by the task

Do not change repository control files such as `AGENTS.md`, `.github/workflows/**`, `.gitmodules`, or upstream source paths unless explicitly requested by the human.

## Loop Engineering protocol

Implementation work under a branch named `loop/<task-id>-<slug>` uses bounded loop engineering.

Before implementation, read:

- `docs/feather-quantizer/loop/LOOP.md`
- `docs/feather-quantizer/loop/TASK_CONTRACT.md`
- `docs/feather-quantizer/loop/QUALITY_GATES.md`
- `docs/feather-quantizer/loop/STOP_CONDITIONS.md`
- the task-specific prompt

Each implementation iteration must follow:

```text
Observe -> Hypothesize -> Plan -> Implement -> Verify -> Record -> Decide
```

Default maximum is 5 implementation iterations. A task may lower this limit. Raising it above 5 requires explicit human approval.

Every loop task maintains:

```text
docs/feather-quantizer/loop/runs/<task-slug>/state.json
docs/feather-quantizer/loop/runs/<task-slug>/iterations.md
```

Never erase previous iteration history. If an earlier hypothesis was wrong, record the correction in a later iteration.

The only valid loop decisions are:

```text
PASS
CONTINUE
BLOCKED_HARDWARE
BLOCKED_ENVIRONMENT
STOP
```

A loop does not grant additional permissions. All normal source-of-truth, protected-path, dependency-freeze, and destructive-operation rules still apply.

### Loop stop rules

Stop instead of improvising when:

- a protected/shared upstream edit appears necessary;
- a dependency/toolchain/submodule update appears necessary;
- physical hardware evidence is required but unavailable;
- the same unresolved failure appears twice without materially new evidence;
- the task reaches its iteration limit;
- the task would need to expand beyond its contract;
- a destructive/external action is required;
- no single evidence-backed next hypothesis can be stated.

Do not bypass a stop condition to achieve a green build.

### Loop PASS rule

A loop task may be declared PASS only when:

- all acceptance criteria are PASS with evidence;
- all applicable HG1..HG10 hard gates are PASS or NA;
- no hard gate is FAIL or UNKNOWN;
- quality score is at least 90/100;
- required hardware evidence exists;
- `bash scripts/feather-quantizer/verify-task.sh` passes;
- task-specific required verification passes.

Compilation proves compilation only. Hardware behavior requires hardware evidence.

## Minimal-diff rules

- Do not perform unrelated formatting or cleanup.
- Do not replace a whole upstream file when a small local implementation or wrapper is sufficient.
- Prefer a new Feather-specific file/target over modifying shared upstream behavior.
- Preserve upstream copyright and SPDX headers in any code derived from upstream.
- Do not rename or reorganize upstream directories.
- Do not introduce a new dependency when existing repository facilities can implement the task.
- Keep one task to one coherent concern.

## Task boundaries

If a task says read-only analysis, do not modify firmware source. A designated report file may be created if the task explicitly names it.

Do not flash hardware, issue destructive Git commands, force-push, rewrite history, merge branches, modify upstream repositories, or publish releases unless the human explicitly asks for that action.

## Verification

Before completing a code task:

1. run the smallest relevant build/checks;
2. run `bash scripts/feather-quantizer/verify-task.sh` for loop tasks;
3. run `git diff --check`;
4. inspect `git status --short`;
5. inspect `git diff --stat` and `git diff --name-only`;
6. confirm every changed file is within the authorized task scope.

If hardware verification is required but hardware is unavailable, state exactly what remains unverified. Never claim real-device behavior from compilation alone.

## Reporting

At the end of a task, report:

- status and iterations used (for loop tasks)
- files changed
- why each file changed
- commands/tests run and their outcomes
- acceptance-criteria results
- hard-gate results and quality score (for loop tasks)
- assumptions and unresolved risks
- whether real hardware was tested
- the smallest recommended next task

For analysis tasks, cite repository file paths, functions, macros, and relevant line ranges or symbols so the conclusions can be reviewed by a human.
