# Loop Iteration Template

Append one section per implementation iteration to the task run's `iterations.md`.

Do not rewrite previous iterations to make the history look cleaner. If an earlier statement was wrong, correct it in a later iteration and preserve the original record.

---

## Iteration N

### Observe

- Current task status:
- Current failing check / missing behavior / evidence gap:
- Exact source/log/evidence:
- Pre-existing unrelated changes observed:

### Hypothesis

**Primary hypothesis:**

Why this hypothesis is supported:

- 

What would falsify it:

- 

### Planned minimal change

Expected files to change before editing:

```text
path/to/file
```

Why this is the smallest coherent change:

### Implementation

Files actually changed:

```text
path/to/file
```

Summary of change:

### Verification

Commands/checks run:

```text
command
```

Results:

```text
PASS / FAIL / NOT_RUN
```

New evidence:

### Guardrails

- Authorized scope: PASS/FAIL
- Dependency freeze: PASS/FAIL
- Protected paths untouched: PASS/FAIL
- `git diff --check`: PASS/FAIL/NOT_RUN
- Diff size within budget: PASS/FAIL
- Hardware evidence required for next conclusion: YES/NO

### Decision

One of:

```text
PASS
CONTINUE
BLOCKED_HARDWARE
BLOCKED_ENVIRONMENT
STOP
```

Reason:

### Next action

- 
