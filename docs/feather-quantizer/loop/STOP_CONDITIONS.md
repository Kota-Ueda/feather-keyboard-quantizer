# Loop Engineering Stop Conditions

The loop is autonomous only while none of these conditions is active.

## Immediate STOP conditions

Stop immediately and report the blocker when any of the following occurs.

### SC1 — Protected/shared change appears necessary

The task appears to require a change to any protected/shared area, including:

```text
keyboards/sekigon/**
lib/**
platforms/**
quantum/**
tmk_core/**
.gitmodules
```

Do not make the edit. Record the exact boundary and request human approval.

### SC2 — Dependency/toolchain change appears necessary

The task appears to require updating or replacing QMK/Vial, TinyUSB, Pico-PIO-USB, pico-sdk, ChibiOS, submodules, compiler, or toolchain.

A failure is evidence to diagnose, not authorization to update dependencies.

### SC3 — Hardware evidence is required

The next conclusion depends on an unmeasured physical fact.

Set status to `BLOCKED_HARDWARE`, record the exact procedure/evidence required, and stop.

### SC4 — Destructive or external action is required

Stop before:

- flashing hardware without explicit authorization;
- force push / history rewrite;
- deleting branches/tags;
- creating releases;
- modifying upstream repositories;
- changing external account/repository settings.

### SC5 — Scope expansion

The smallest coherent fix is no longer the concern described by the task contract.

Stop and propose a new task instead of silently expanding scope.

## Bounded-loop STOP conditions

### SC6 — Iteration limit reached

Default maximum is 5 implementation iterations.

If the task has not passed by the maximum, set status to `STOP` and summarize the strongest remaining hypotheses.

### SC7 — Same unresolved failure twice

If the same failure appears in two consecutive verification attempts and the second attempt does not provide materially new evidence, stop.

Do not make random third/fourth changes around the same error.

### SC8 — Hypothesis confidence collapses

If evidence contradicts the current mental model and no single, testable next hypothesis can be justified from source/logs, stop for analysis/human review.

### SC9 — Diff budget breach

Stop before exceeding:

- target: 500 non-documentation changed lines;
- hard threshold: 1,500 non-documentation changed lines.

Split the task unless a human explicitly approves a larger diff.

### SC10 — Acceptance criterion becomes impossible or ambiguous

If an acceptance criterion cannot be satisfied with the available environment/evidence, do not redefine it. Mark the blocker and stop.

## Environment blocker

Use `BLOCKED_ENVIRONMENT` only when the task cannot proceed because required tooling/environment is unavailable and installing or modifying it is outside authorized scope.

Examples:

- compiler absent in a sandbox where installation is disallowed;
- USB device access unavailable in Codex Cloud;
- expected CI service unavailable.

Do not use environment blocker to hide a source/build failure.

## Stop report format

When stopping, report:

```text
Status:
Stop condition:
Iteration:
Observed evidence:
Last hypothesis:
Last verification:
Exact human decision/evidence required:
Files changed so far:
Safe rollback point:
Recommended next action:
```

A stopped task is not merge-ready to `feather-main` unless the merge is explicitly intended to preserve documentation/evidence only and a human authorizes it.
