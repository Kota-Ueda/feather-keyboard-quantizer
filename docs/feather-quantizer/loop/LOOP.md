# Feather Quantizer Loop Engineering Protocol

## Purpose

This project uses bounded loop engineering for implementation work. The agent may iterate autonomously, but only inside an explicit task contract, with hard stop conditions and human review at hardware or control-plane boundaries.

The protocol is designed for the Feather RP2040 Keyboard Quantizer port, where build automation is useful but real USB/HID behavior requires physical evidence.

## Branch model

```text
feather-main
  |
  +-- loop/<task-id>-<slug>          human-owned task branch
         |
         +-- codex/<task-work>       Codex working branch / inner PR
```

Normal flow:

1. create `loop/<task-id>-<slug>` from `feather-main`;
2. put the task prompt under `prompts/tasks/`;
3. run Codex against the loop task branch;
4. when the bounded loop reaches `PASS`, `BLOCKED_HARDWARE`, `BLOCKED_ENVIRONMENT`, or `STOP`, Codex creates or updates a **Draft inner PR** from its working branch to the declared loop task branch when the platform-supported PR action is available;
5. human reviews the diff, iteration evidence, and CI;
6. human marks the inner PR ready and merges it only when the task contract is satisfied or when a blocked state must be preserved for human action;
7. open `loop/<task-id>-<slug>` -> `feather-main` only when the task is `PASS`;
8. merge to `feather-main` only after merge-readiness gates pass.

Do not open project work directly against upstream `sekigon-gonnoc/vial-qmk`.

## Draft PR handoff

Draft PR creation is part of delivery, not project approval.

When a loop reaches a terminal handoff state (`PASS`, `BLOCKED_HARDWARE`, `BLOCKED_ENVIRONMENT`, or `STOP`), the agent should create or update one Draft inner PR when the execution platform exposes a repository-authorized PR action.

The Draft PR MUST:

- target the task contract's declared `loop/<task-id>-<slug>` base branch;
- originate from the current Codex working branch;
- remain Draft even when the task status is `PASS`;
- summarize status, iterations used, changed files, acceptance criteria, hard gates, quality score, verification, hardware evidence, blockers, and recommended next task;
- link or name the task prompt and run-state files;
- update an existing inner PR instead of creating duplicates for the same working branch/base pair.

The agent MUST NOT:

- mark its own PR ready for review;
- merge any PR;
- enable auto-merge;
- retarget the PR to `feather-main`;
- create a PR against upstream;
- request, expose, store, or configure a personal access token, SSH private key, or other long-lived GitHub credential merely to automate PR creation;
- bypass the platform-supported repository integration by adding ad-hoc credentials to the task environment.

If the platform does not expose an authorized PR action, PR creation is not a task failure. The agent must report the exact head branch, intended base branch, terminal task status, and that human PR creation is required.

Human review remains mandatory before any inner PR is marked ready or merged.

## Bounded loop

Each implementation iteration MUST follow this sequence:

1. **Observe**
   - inspect task contract;
   - inspect `git status --short` and existing diff;
   - capture the current failing check, missing behavior, or evidence gap;
   - separate pre-existing unrelated changes from task changes.
2. **Hypothesize**
   - state one primary causal hypothesis;
   - cite the file/function/error/evidence supporting it.
3. **Plan**
   - choose the smallest coherent change that can falsify or confirm that hypothesis;
   - list files expected to change before editing.
4. **Implement**
   - make only that scoped change;
   - do not bundle opportunistic cleanup or dependency updates.
5. **Verify**
   - run the smallest relevant static check/build/test;
   - run repository guardrail checks;
   - if a real-device claim is involved, require hardware evidence.
6. **Record**
   - append the iteration to `iterations.md` using `ITERATION_TEMPLATE.md`;
   - update `state.json`.
7. **Decide**
   - `PASS`: all acceptance criteria and hard gates satisfied;
   - `CONTINUE`: new evidence supports another bounded iteration;
   - `BLOCKED_HARDWARE`: physical evidence is required;
   - `BLOCKED_ENVIRONMENT`: required non-project tooling is unavailable and installing/updating it is not authorized;
   - `STOP`: a stop condition has been reached.

## Iteration limits

- Default maximum: **5 implementation iterations per task**.
- The task prompt may lower this limit but may not raise it above 5 without explicit human approval.
- A documentation-only observation step does not consume an implementation iteration until a project file is changed in pursuit of the task result.
- Never reset the counter by changing the hypothesis wording.

## One-hypothesis rule

An iteration should test one primary hypothesis. If two unrelated changes are needed, split them into separate iterations or separate tasks.

Bad:

```text
Update board definition + upgrade TinyUSB + refactor parser + add gesture logic
```

Good:

```text
Hypothesis: the Feather target fails because host D+ is still configured as GP4.
Change: Feather-local host init uses GP16 while preserving all other host settings.
Validation: compile target and compare the next error/result.
```

## Hardware checkpoints

The agent MUST stop at `BLOCKED_HARDWARE` when a conclusion requires physical evidence that is not already committed to the repository.

Examples:

- GP18 VBUS enable polarity/timing;
- DEFT/HUGE PLUS USB descriptors and report bytes;
- real cursor/scroll/gesture behavior;
- latency/gesture feel;
- suspend/resume/hot-plug stability;
- flash/persistence behavior on the actual Feather.

At a hardware checkpoint:

1. state exactly what must be measured;
2. provide a reproducible, non-destructive procedure;
3. define expected evidence format;
4. do not infer the result;
5. resume only after the evidence is added to the task branch.

## Task state

Every `loop/*` task uses:

```text
docs/feather-quantizer/loop/runs/<branch-slug>/state.json
docs/feather-quantizer/loop/runs/<branch-slug>/iterations.md
```

For branch:

```text
loop/002-phase-0-hid-capture
```

the run directory is:

```text
docs/feather-quantizer/loop/runs/002-phase-0-hid-capture/
```

`state.json` is machine-checked by CI. `iterations.md` is the human-readable engineering record.

## Final task report

Before a task is presented for human review, report:

- final status;
- iteration count;
- files changed and why;
- acceptance criteria result;
- hard-gate result;
- quality score;
- builds/tests/checks and exact outcomes;
- hardware evidence used or still missing;
- unresolved risks;
- Draft PR URL when automatically created, otherwise the exact manual PR handoff branches;
- smallest recommended next task.

## Authority order

1. system/developer/user instructions;
2. task-specific prompt;
3. `AGENTS.md`;
4. this loop protocol;
5. project documentation.

The loop never authorizes work that is forbidden by a higher-priority instruction or project guardrail.
