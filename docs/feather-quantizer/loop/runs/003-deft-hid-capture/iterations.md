# Task 003 — DEFT HID capture loop log

Branch: `loop/003-deft-hid-capture`

Task prompt: `prompts/tasks/003-deft-hid-capture.md`

Loop protocol: `prompts/loop-runner.md`

## Initialization

Known human-supplied physical identity:

- Marketing name: ELECOM DEFT
- Product number: `M-DT2DRBK`
- Label revision: `V02`
- Current connection mode: `2.4 GHz USB receiver`

Important distinction: the physical product label is identity evidence only. USB VID/PID, receiver identity, descriptors, report IDs, raw report bytes, button mappings and compatibility remain uncaptured until the hardware procedure is performed.

- Status: `NOT_STARTED`
- Implementation iterations used: `0 / 5`
- Hardware evidence requirement: `REQUIRED_FOR_PASS`
- No compatibility claim has been made.

Codex must append future iterations below this section using `docs/feather-quantizer/loop/ITERATION_TEMPLATE.md` and must not rewrite prior history.

## Iteration 1

### Observe

- Current task status: `NOT_STARTED`
- Current failing check / missing behavior / evidence gap: Task 003 requires a
  capture from the exact DEFT/receiver, but the designated evidence directory is
  empty and this execution environment has no access to the human's USB device.
- Exact source/log/evidence: `find` returned no files below the designated
  evidence directory; `state.json` records `evidence_available: false`.
- Pre-existing unrelated changes observed: `builddefs/docsgen/yarn.lock` is
  modified and `builddefs/docsgen/.yarn/` plus `.yarnrc.yml` are untracked. They
  were not changed, staged, cleaned, or included in Task 003 work.

### Hypothesis

**Primary hypothesis:** A full USBPcap capture beginning before receiver
insertion, paired with timestamped stimuli, will preserve the missing Windows USB
enumeration, HID descriptor, and interrupt-IN evidence for repository-side
extraction and review.

Why this hypothesis is supported:

- `docs/feather-quantizer/phase-0-capture.md` requires enumeration, every HID
  report descriptor, and simultaneous interrupt-IN capture.
- Capturing before insertion is necessary to observe enumeration descriptor
  requests rather than only later input traffic.

What would falsify it:

- The returned PCAP lacks receiver insertion/enumeration, one or more descriptor
  transfers, interrupt-IN traffic, the ten-second idle interval, or timestamped
  coverage for required stimuli.

### Planned minimal change

Expected files to change before editing:

```text
docs/feather-quantizer/research/hid-captures/elecom-deft-m-dt2drbk/2_4ghz-receiver/CAPTURE-HANDOFF.md
docs/feather-quantizer/loop/runs/003-deft-hid-capture/iterations.md
docs/feather-quantizer/loop/runs/003-deft-hid-capture/state.json
```

Why this is the smallest coherent change: it records the hardware checkpoint and
gives the Windows operator an exact, non-destructive procedure without modifying
firmware or inventing evidence.

### Implementation

Files actually changed:

```text
docs/feather-quantizer/research/hid-captures/elecom-deft-m-dt2drbk/2_4ghz-receiver/CAPTURE-HANDOFF.md
docs/feather-quantizer/loop/runs/003-deft-hid-capture/iterations.md
docs/feather-quantizer/loop/runs/003-deft-hid-capture/state.json
```

Summary of change: added a Windows Wireshark/USBPcap handoff with prerequisites,
exact returned files, the complete three-trial stimulus checklist, validation
commands, serial-number privacy boundary, and an explicit prohibition on HID
Output/Feature writes. Updated the loop record to the required hardware stop.

### Verification

Commands/checks run:

```text
python3 scripts/feather-quantizer/verify-loop-state.py docs/feather-quantizer/loop/runs/003-deft-hid-capture/state.json
bash scripts/feather-quantizer/verify-task.sh
git diff --check
git status --short
git diff --stat
git diff --name-only
```

Results:

- `verify-loop-state.py`: PASS (`BLOCKED_HARDWARE`, iteration `1/5`, score 40).
- `verify-task.sh`: the literal command cannot resolve the absent local
  `feather-main` ref and exits 128 before checks; with the available pre-Task-003
  baseline `BASE_REF=724783789`, the script passes. This is a local ref
  limitation, not hardware or acceptance evidence.
- task-file `git diff --check`: PASS.
- status/diff inspection: PASS for task scope; it also continues to show the
  pre-existing unrelated docsgen Yarn changes listed under Observe.
- capture JSON/NDJSON/hash/byte-length validation: NOT_RUN because no capture
  artifacts exist yet; this cannot be treated as passing.

New evidence: no hardware evidence. The evidence gap and exact capture procedure
are now reviewable in the repository.

### Guardrails

- Authorized scope: PASS
- Dependency freeze: PASS
- Protected paths untouched: PASS
- `git diff --check`: PASS for Task 003 files
- Diff size within budget: PASS (documentation only)
- Hardware evidence required for next conclusion: YES

### Decision

```text
BLOCKED_HARDWARE
```

Reason: SC3 applies. AC1--AC7 require observations from the exact physical
M-DT2DRBK V02 and supplied 2.4 GHz receiver. No such capture is committed, so
USB identity, descriptors, report bytes, report lengths, mappings, and KQM
constraint results remain unknown.

### Next action

- The human runs `CAPTURE-HANDOFF.md` on the Windows PC, reviews the result for
  unique serial data, and commits the five requested staging files to the task
  branch. Resume this same bounded loop to extract, validate, and analyze them.

## Iteration 2

### Observe

- Current task status: `BLOCKED_HARDWARE`
- Current failing check / missing behavior / evidence gap: human review confirmed
  Windows 11 will be used and identified two pre-capture defects: the UTC command
  depended on PowerShell 7.1, and the handoff could allow unrelated root-hub USB
  traffic to be committed to a public repository.
- Exact source/log/evidence: inline review of `CAPTURE-HANDOFF.md` requested a
  Windows PowerShell 5.1-compatible UTC expression and a new-device-only privacy
  boundary with a fail-closed fallback.
- Pre-existing unrelated changes observed: the same docsgen Yarn changes noted
  in Iteration 1 remain present and untouched.

### Hypothesis

**Primary hypothesis:** Replacing the UTC expression and making raw-PCAP
publication fail closed unless new-device-only capture or verified isolation is
used will make the procedure safe to perform on Windows 11 without changing the
hardware checkpoint.

Why this hypothesis is supported:

- `[DateTime]::UtcNow.ToString(...)` is available in Windows PowerShell 5.1.
- Capturing only a newly connected receiver prevents already-connected input
  devices on the same root hub from entering the returned raw PCAP.

What would falsify it:

- The procedure still instructs `Get-Date -AsUTC`, or permits committing a PCAP
  when unrelated USB traffic cannot be excluded with confidence.

### Planned minimal change

Expected files to change before editing:

```text
docs/feather-quantizer/research/hid-captures/elecom-deft-m-dt2drbk/2_4ghz-receiver/CAPTURE-HANDOFF.md
docs/feather-quantizer/loop/runs/003-deft-hid-capture/iterations.md
docs/feather-quantizer/loop/runs/003-deft-hid-capture/state.json
```

Why this is the smallest coherent change: it corrects only the reviewed capture
instructions and appends the required loop state/history; firmware, upstream,
workflow, and task-contract files remain untouched.

### Implementation

Files actually changed:

```text
docs/feather-quantizer/research/hid-captures/elecom-deft-m-dt2drbk/2_4ghz-receiver/CAPTURE-HANDOFF.md
docs/feather-quantizer/loop/runs/003-deft-hid-capture/iterations.md
docs/feather-quantizer/loop/runs/003-deft-hid-capture/state.json
```

Summary of change: replaced both `Get-Date -AsUTC` uses with the requested .NET
UTC expression; made new-device-only capture preferred; added a fail-closed
fallback, capture-note fields, and a whole-capture privacy gate that prohibits
committing unrelated USB traffic or unique serials.

### Verification

Commands/checks run:

```text
rg -n 'Get-Date\s+-AsUTC' docs/feather-quantizer/research/hid-captures/elecom-deft-m-dt2drbk/2_4ghz-receiver/CAPTURE-HANDOFF.md
python3 scripts/feather-quantizer/verify-loop-state.py docs/feather-quantizer/loop/runs/003-deft-hid-capture/state.json
bash scripts/feather-quantizer/verify-task.sh
git diff --check
git status --short
git diff --stat
git diff --name-only
```

Results:

- forbidden UTC-form search: PASS; `rg` found no `Get-Date -AsUTC` in the
  handoff (exit 1 means no match).
- required UTC-expression search: PASS; both timestamp commands use the
  Windows PowerShell 5.1-compatible expression.
- `verify-loop-state.py`: PASS (`BLOCKED_HARDWARE`, iteration `2/5`, score 45).
- `verify-task.sh`: PASS with `BASE_REF=HEAD^` after committing this iteration;
  the literal command remains limited by the absent local `feather-main` ref
  already recorded in Iteration 1.
- task-file `git diff --check`: PASS.
- status/diff inspection: PASS for the three authorized Task 003 files; the
  pre-existing docsgen Yarn working-tree changes remain excluded.

New evidence: Windows 11 is the confirmed capture OS. No USB/HID capture has yet
been supplied, so AC1--AC7 remain unresolved.

### Guardrails

- Authorized scope: PASS
- Dependency freeze: PASS
- Protected paths untouched: PASS
- `git diff --check`: PASS for Task 003 files
- Diff size within budget: PASS (documentation only)
- Hardware evidence required for next conclusion: YES

### Decision

```text
BLOCKED_HARDWARE
```

Reason: the handoff is safer and PowerShell 5.1-compatible, but SC3 remains
active until the exact DEFT/receiver evidence is captured and committed.

### Next action

- The human performs the revised procedure. Commit the raw PCAP only when the
  documented privacy gate passes; otherwise retain it locally and repeat with
  new-device-only mode or an isolated root hub.
