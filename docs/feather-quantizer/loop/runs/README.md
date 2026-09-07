# Loop run records

Each bounded loop task gets one immutable-by-convention engineering record directory.

Example:

```text
loop/002-phase-0-hid-capture
```

uses:

```text
docs/feather-quantizer/loop/runs/002-phase-0-hid-capture/
├── state.json
└── iterations.md
```

## state.json

Machine-readable current state. It must satisfy the invariants enforced by:

```text
scripts/feather-quantizer/verify-loop-state.py
```

and follow:

```text
docs/feather-quantizer/loop/state.schema.json
```

Minimum starting pattern:

```json
{
  "task_id": "002",
  "branch": "loop/002-phase-0-hid-capture",
  "status": "NOT_STARTED",
  "iteration": 0,
  "max_iterations": 3,
  "acceptance_criteria": [
    {
      "id": "AC1",
      "description": "Replace with task-specific criterion",
      "status": "UNKNOWN",
      "evidence": ""
    }
  ],
  "quality": {
    "score": 0,
    "hard_gates": {
      "HG1": "UNKNOWN",
      "HG2": "UNKNOWN",
      "HG3": "UNKNOWN",
      "HG4": "UNKNOWN",
      "HG5": "UNKNOWN",
      "HG6": "UNKNOWN",
      "HG7": "UNKNOWN",
      "HG8": "UNKNOWN",
      "HG9": "UNKNOWN",
      "HG10": "UNKNOWN"
    }
  },
  "hardware": {
    "requirement": "NONE",
    "evidence_available": false,
    "evidence": []
  },
  "last_failure_signature": null,
  "same_failure_count": 0,
  "updated_at": "2026-01-01T00:00:00Z"
}
```

Do not copy the example date literally; use the actual update time.

## iterations.md

Append-only human-readable engineering log based on:

```text
docs/feather-quantizer/loop/ITERATION_TEMPLATE.md
```

Preserve failed hypotheses. The point is traceability, not presenting a perfect-looking history.

## Hardware evidence

Hardware captures belong under the relevant research/evidence directory, not embedded as invented values in state files.

`state.json.hardware.evidence` should contain repository-relative paths or concise references to those committed artifacts.
