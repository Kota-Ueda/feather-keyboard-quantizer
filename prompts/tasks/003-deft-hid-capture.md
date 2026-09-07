# Task 003 — ELECOM DEFT M-DT2DRBK 2.4 GHz HID capture and compatibility evidence

Use `prompts/loop-runner.md` as the execution protocol for this task.

## Task contract

**Task ID:** 003

**Task type:** hardware-verification

**Goal:** Capture and review real USB/HID evidence for the user's ELECOM DEFT M-DT2DRBK (label revision V02) when used through its 2.4 GHz USB receiver, then compare that evidence against the current Keyboard Quantizer Mini limits documented in Task 001. This task establishes evidence for later Feather implementation; it must not modify firmware.

**Base branch:** `loop/003-deft-hid-capture`

**Known physical identity supplied by the human:**

```text
Marketing name: ELECOM DEFT
Product number: M-DT2DRBK
Label revision: V02
Current connection mode: 2.4 GHz USB receiver
```

Do not infer USB VID/PID, receiver identity, HID descriptors, report bytes, report IDs, or button encoding from the product number. Those are hardware evidence to be captured.

**Evidence directory:**

```text
docs/feather-quantizer/research/hid-captures/elecom-deft-m-dt2drbk/2_4ghz-receiver/
```

**Writable paths:**

```text
docs/feather-quantizer/research/hid-captures/elecom-deft-m-dt2drbk/2_4ghz-receiver/**
docs/feather-quantizer/loop/runs/003-deft-hid-capture/**
```

**Read-only reference paths:**

```text
keyboards/sekigon/**
keyboards/feather_quantizer/**
AGENTS.md
.github/workflows/**
FEATHER_QUANTIZER.md
docs/feather-quantizer/spec.md
docs/feather-quantizer/phase-0-capture.md
docs/feather-quantizer/research/hid-captures/README.md
docs/feather-quantizer/research/task-001-upstream-analysis.md
```

**Maximum implementation iterations:** 5

**Hardware evidence required:** REQUIRED_FOR_PASS

Task 003 cannot PASS until real capture evidence from this exact DEFT / 2.4 GHz receiver setup is present in the repository and satisfies the acceptance criteria below.

## Acceptance criteria

### AC1 — Physical identity and capture environment

Evidence records:

- ELECOM DEFT `M-DT2DRBK`;
- label revision `V02`;
- the 2.4 GHz USB receiver as the active connection mode;
- receiver physical label/identity when observable;
- capture host OS/version/architecture;
- capture tool name/version and exact command/configuration;
- capture start/end time.

Do not store the device serial number unless it is materially needed for debugging. Prefer omitting or redacting unique serial identifiers from committed evidence.

### AC2 — USB enumeration and HID descriptors

Capture and commit, according to `docs/feather-quantizer/phase-0-capture.md` and the evidence schema:

- USB VID/PID and bcdDevice;
- manufacturer/product strings when available;
- complete configuration/interface/endpoint metadata;
- every HID interface;
- complete raw HID report descriptor for every HID interface;
- matching decoded descriptor text;
- report IDs and descriptor-derived report lengths;
- vendor-defined usages/collections without guessing semantics.

### AC3 — Raw input reports

Commit timestamped raw input evidence for at least:

- >=10 seconds idle baseline;
- each physical button individually: press and release;
- X positive / X negative;
- Y positive / Y negative;
- vertical wheel both directions;
- horizontal tilt/pan both directions when present;
- useful simultaneous inputs defined in Phase 0 procedure;
- any vendor-defined report/field that changes under user-accessible controls.

Each stimulus should have at least three trials unless the operator records a concrete physical reason it cannot be repeated.

### AC4 — Maximum report length and report inventory

Record:

- exact observed transfer lengths per interface/endpoint/report ID;
- maximum observed full input-transfer length;
- maximum descriptor-derived input-report length;
- discrepancies as unresolved findings rather than normalizing them away.

### AC5 — KQM constraint worksheet

Using only captured evidence, evaluate the Task 001 constraints:

- shared 64-byte HID report buffer;
- `CFG_TUH_DEVICE_MAX=4`;
- `CFG_TUH_HID=8`;
- parser pools: 8 devices / 16 collections / 32 members / 32 usages;
- current Vial path only exposes 8 actionable button bits;
- horizontal pan usage expectations.

Each result must be one of:

```text
within_constraint
exceeds_constraint
requires_parser_fixture
```

No overall Feather compatibility claim is allowed from this worksheet alone.

### AC6 — Evidence integrity

- JSON/NDJSON syntax validates;
- `data_hex` byte counts match recorded transfer lengths;
- descriptor `.bin` hashes match metadata;
- declared descriptor lengths are compared to captured byte lengths;
- wired evidence is not mixed with receiver evidence;
- observed bytes remain separate from interpretation.

### AC7 — Hardware-backed task conclusion

Task 003 may PASS only if the exact DEFT M-DT2DRBK / 2.4 GHz receiver capture is complete enough to support the next engineering decision.

If evidence is incomplete, use `BLOCKED_HARDWARE` with an exact, non-destructive follow-up procedure. Do not invent missing bytes or infer them from public documentation.

### AC8 — Loop evidence

Maintain:

```text
docs/feather-quantizer/loop/runs/003-deft-hid-capture/state.json
docs/feather-quantizer/loop/runs/003-deft-hid-capture/iterations.md
```

## Expected execution pattern

Because Codex Cloud cannot directly access the human's USB device, the normal first handoff is expected to be:

```text
OBSERVE
  -> confirm capture requirements and currently committed evidence
PLAN
  -> determine exact host-side non-destructive capture procedure
DECIDE
  -> BLOCKED_HARDWARE until the human performs the capture
```

At `BLOCKED_HARDWARE`, provide the human with:

1. exact host prerequisites;
2. commands/tool steps appropriate to the known host OS (if host OS is not known, request it instead of guessing);
3. a stimulus-by-stimulus checklist;
4. exact output files to place in the evidence directory;
5. validation commands to run before handoff;
6. no destructive operations and no undocumented HID output/feature writes.

After the evidence is committed to the loop branch, resume the same bounded task and analyze it.

## Required final verification

Run what the environment permits and report exact results:

```bash
python3 scripts/feather-quantizer/verify-loop-state.py docs/feather-quantizer/loop/runs/003-deft-hid-capture/state.json
bash scripts/feather-quantizer/verify-task.sh
git diff --check
git status --short
git diff --stat
git diff --name-only
```

Also validate every committed JSON/NDJSON evidence file and all hash/byte-length consistency checks applicable to the capture.

No firmware build is required specifically because Task 003 does not modify firmware, but repository CI must not regress the existing KQM baseline check.

## Explicitly forbidden

Do not:

- modify firmware source;
- modify `keyboards/sekigon/**`;
- modify `keyboards/feather_quantizer/**`;
- modify AGENTS.md or workflows;
- update dependencies/submodules/toolchain;
- invent USB/HID values;
- infer receiver HID behavior from the DEFT model label alone;
- send undocumented HID Feature/Output reports;
- flash the Feather;
- store unnecessary unique device serial identifiers;
- create an upstream PR;
- mark a Draft PR ready for review;
- merge or enable auto-merge.

## Draft PR handoff

Follow `prompts/loop-runner.md`. At PASS/BLOCKED/STOP handoff, create or update a Draft inner PR from the Codex working branch to `loop/003-deft-hid-capture` when the platform-authorized PR action is available. Never target `feather-main` directly.
