# Loop Engineering Quality Gates

## Principle

Quality is evaluated with **Hard Gates + Score**.

The score helps compare review readiness. It never overrides a failed Hard Gate.

A task may be marked `PASS` only when:

1. every applicable Hard Gate passes;
2. quality score is **90/100 or higher**;
3. all acceptance criteria are satisfied with evidence;
4. no stop condition remains active;
5. required hardware claims are backed by committed hardware evidence.

## Hard Gates

### HG1 — Authorized scope

All changed files are inside the task contract's writable paths.

Automatic failure if protected/shared upstream code was changed without explicit task authorization.

### HG2 — Dependency freeze

No unapproved changes to QMK/Vial, TinyUSB, Pico-PIO-USB, pico-sdk, ChibiOS, submodule revisions, compiler/toolchain, or `.gitmodules`.

### HG3 — Baseline integrity

For firmware tasks, the original KQM Mini baseline build must still pass in repository CI unless the task is explicitly documentation-only.

### HG4 — Target verification

The smallest task-relevant verification must pass.

Examples:

- documentation task: structure/schema/static checks;
- board-port task: Feather target compile;
- parser task: parser/unit fixture checks plus Feather compile;
- gesture task: unit/state-machine checks plus Feather compile;
- hardware-dependent task: hardware evidence in addition to software checks.

A skipped check counts as `N/A` only when the task contract explicitly declares why it is not applicable.

### HG5 — Acceptance criteria

Every acceptance criterion is marked `PASS` with evidence. `UNKNOWN`, `NOT_RUN`, or `ASSUMED` is not PASS.

### HG6 — Hardware evidence boundary

No physical-device claim may be marked verified without repository evidence from the actual target hardware/device.

Compilation is not hardware verification.

### HG7 — Bounded-loop compliance

- iteration count does not exceed task maximum;
- no same unresolved failure was repeated twice without a materially new hypothesis;
- every implementation iteration has an entry in `iterations.md`;
- `state.json` matches the human-readable record.

### HG8 — Diff hygiene

- `git diff --check` passes;
- no unrelated formatting/generated churn;
- no untracked task output required for review;
- changed-file list matches the task scope.

### HG9 — Reversibility

The task can be reverted without rewriting upstream history or modifying unrelated project state.

### HG10 — Human checkpoint respected

If a stop condition requires human review or physical intervention, the agent stopped instead of bypassing it.

## Quality score — 100 points

| Category | Points | Full-credit requirement |
|---|---:|---|
| Scope discipline | 15 | Minimal coherent diff; no unrelated changes |
| Root-cause evidence | 15 | Changes are tied to observed evidence, not guesswork |
| Build/static verification | 20 | Relevant automated checks pass |
| Acceptance criteria | 20 | All criteria have explicit evidence |
| Regression protection | 10 | KQM baseline and relevant existing behavior protected |
| Iteration record | 10 | Complete Observe/Hypothesis/Change/Verify/Decision history |
| Documentation | 5 | Design/risk/user-facing behavior updated where needed |
| Reviewability | 5 | Small commits/diff, clear final report, unresolved risks explicit |

## Score interpretation

```text
90-100  merge-ready if all Hard Gates pass
80-89   needs improvement / human review
60-79   incomplete
<60     not review-ready
```

## Machine representation

`state.json` contains:

```json
{
  "quality": {
    "score": 0,
    "hard_gates": {
      "HG1": "PASS",
      "HG2": "PASS"
    }
  }
}
```

Allowed gate states:

```text
PASS
FAIL
NA
UNKNOWN
```

`PASS` task status is invalid when any applicable Hard Gate is `FAIL` or `UNKNOWN`.
