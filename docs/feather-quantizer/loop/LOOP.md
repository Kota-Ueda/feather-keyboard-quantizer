# Feather Quantizer Loop Engineering Protocol

## Purpose

This project uses bounded loop engineering with **separated Codex roles**. Implementation may iterate autonomously inside an explicit task contract, but planning, implementation, independent review, deterministic verification, specialist review, and human authority are deliberately separated.

The default topology is defined in `docs/feather-quantizer/loop/MULTI_AGENT.md`:

```text
Codex Planner -> Codex Runner -> CI -> Codex Reviewer -> Human merge
                                  \
                                   -> conditional Specialist Reviewer
```

The protocol is designed for the Feather RP2040 Keyboard Quantizer port, where build automation is useful but real USB/HID behavior requires physical evidence.

## Branch model

```text
feather-main
  |
  +-- loop/<task-id>-<slug>          human-owned task branch
         |
         +-- codex/<task-work>       Runner working branch / inner PR
```

Planner, Reviewer, and Specialist roles do not need implementation branches. The Runner owns implementation writes.

Normal flow:

1. create `loop/<task-id>-<slug>` from `feather-main`;
2. create/validate the task contract; use Codex Planner unless a valid human-authored contract already exists;
3. run Codex Runner against the loop task branch;
4. Runner performs bounded internal iterations and creates/updates a **Draft inner PR** at terminal handoff when platform-supported PR actions are available;
5. run repository CI / deterministic checks;
6. run an independent Codex Reviewer from fresh context;
7. when `MULTI_AGENT.md` triggers a specialist domain, run the corresponding independent Specialist Reviewer;
8. if review returns `REQUEST_CHANGES`/`FINDINGS`, return findings to Runner and update the same Draft PR; default maximum is 2 independent review correction cycles;
9. if review returns `APPROVE` and all required specialist verdicts are `CLEAR`, the human may mark the inner PR ready and merge it;
10. blocked states may be merged into the loop task branch only to preserve reviewed handoff/evidence procedures for human action;
11. open `loop/<task-id>-<slug>` -> `feather-main` only when the task is `PASS`;
12. merge to `feather-main` only after merge-readiness gates pass and human approval.

Do not open project work directly against upstream `sekigon-gonnoc/vial-qmk`.

## Agent-role separation

The role contract in `MULTI_AGENT.md` is mandatory for R1/R2 work:

- Planner plans but does not implement product code;
- Runner implements but does not approve itself;
- Reviewer reviews from fresh context and does not fix findings;
- Specialist Reviewer is conditional and read-only by default;
- CI is the deterministic verification layer, not an agent;
- human retains merge, hardware, protected-path, scope-expansion, and destructive-action authority.

The independent Reviewer is not invoked after every Runner iteration. Review normally occurs only at a terminal handoff candidate, with early review reserved for high-risk hardware/privacy/architecture/protected/dependency decisions.

## Draft PR handoff

Draft PR creation is part of Runner delivery, not project approval.

When a loop reaches a terminal handoff state (`PASS`, `BLOCKED_HARDWARE`, `BLOCKED_ENVIRONMENT`, or `STOP`), the Runner should create or update one Draft inner PR when the execution platform exposes a repository-authorized PR action.

The Draft PR MUST:

- target the task contract's declared `loop/<task-id>-<slug>` base branch;
- originate from the current Runner working branch;
- remain Draft even when the task status is `PASS`;
- summarize status, iterations used, changed files, acceptance criteria, hard gates, quality score, verification, hardware evidence, blockers, and recommended next task;
- link or name the task prompt and run-state files;
- update an existing inner PR instead of creating duplicates for the same working branch/base pair.

The Runner MUST NOT:

- mark its own PR ready for review;
- approve its own PR;
- merge any PR;
- enable auto-merge;
- retarget the PR to `feather-main`;
- create a PR against upstream;
- request, expose, store, or configure a personal access token, SSH private key, or other long-lived GitHub credential merely to automate PR creation;
- bypass the platform-supported repository integration by adding ad-hoc credentials to the task environment.

If the platform does not expose an authorized PR action, PR creation is not a task failure. The Runner must report the exact head branch, intended base branch, terminal task status, and that human PR creation is required.

Independent review plus human merge authority remain mandatory unless an R0 task contract explicitly authorizes reviewer omission.

## Bounded Runner loop

Each implementation iteration MUST follow this sequence:

1. **Observe**
   - inspect task contract;
   - inspect `git status --short` and existing diff;
   - capture the current failing check, missing behavior, review finding, or evidence gap;
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

A correction made in response to Reviewer/Specialist findings consumes a normal implementation iteration when project files are changed. Review cycles do not reset the implementation iteration counter.

## Iteration and review limits

- Default maximum: **5 implementation iterations per task**.
- The task prompt may lower this limit but may not raise it above 5 without explicit human approval.
- Default maximum: **2 independent review correction cycles per task**.
- A task prompt may lower the review-cycle limit; raising it requires explicit human approval.
- A documentation-only observation step does not consume an implementation iteration until a project file is changed in pursuit of the task result.
- Never reset counters by changing hypothesis/finding wording.
- If BLOCKER/MAJOR findings remain after the second review correction cycle, use `ESCALATE_HUMAN` rather than continuing reviewer/runner ping-pong.

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

The Runner MUST stop at `BLOCKED_HARDWARE` when a conclusion requires physical evidence that is not already committed to the repository.

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
5. invoke early independent review when the handoff itself has safety/privacy/HID-protocol risk;
6. resume only after the evidence is added to the task branch.

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

Before a task is presented for human merge approval, report:

- final status;
- implementation iteration count;
- independent review cycle count;
- files changed and why;
- acceptance criteria result;
- hard-gate result;
- quality score;
- builds/tests/checks and exact outcomes;
- hardware evidence used or still missing;
- Reviewer verdict;
- required Specialist type and verdict, if any;
- unresolved risks;
- Draft PR URL when automatically created, otherwise the exact manual PR handoff branches;
- smallest recommended next task.

## Authority order

1. system/developer/user instructions;
2. task-specific prompt;
3. `AGENTS.md`;
4. this loop protocol and `MULTI_AGENT.md`;
5. project documentation.

The loop never authorizes work that is forbidden by a higher-priority instruction or project guardrail.
