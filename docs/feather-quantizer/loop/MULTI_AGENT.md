# Codex Multi-Agent Development Model

## Decision

The default development topology for this project is **3 core Codex agents + 1 conditional specialist**.

```text
Human goal / approval
        |
        v
Codex Planner
        |
        v
Codex Runner  <-----------------------+
        |                              |
        v                              |
CI / deterministic checks             |
        |                              |
        v                              |
Codex Reviewer -- REQUEST_CHANGES -----+
        |
        +-- APPROVE ------------------> Human merge
        |
        +-- ESCALATE_HUMAN ----------> Human decision

Conditional high-risk path:
Planner / Reviewer -- trigger --> Codex Specialist Reviewer
```

The normal task does **not** use four permanent agents. CI already provides an independent deterministic verification layer, so a permanent fourth "Verifier" agent would usually duplicate checks and add coordination cost without enough independent value.

The fourth Codex role is therefore **conditional** and is activated only for a specific risk domain.

## Why 3 + 1

The roles separate three different failure modes:

1. **Planning failure** — wrong task boundary, weak acceptance criteria, missing evidence requirement.
2. **Implementation failure** — incorrect or over-broad code/doc change.
3. **Review failure** — the implementer rationalizes its own assumptions or misses task-contract violations.

CI covers a fourth class mechanically: reproducible build/test/guardrail failure.

A specialist is added only when the task has a domain-specific risk that deserves a second independent reasoning pass.

## Core role 1 — Planner

Purpose: turn a human goal into a bounded, reviewable engineering task.

The Planner:

- reads repository documentation and current state;
- decomposes work into the smallest coherent task;
- writes or proposes the task contract;
- defines acceptance criteria and required evidence;
- assigns a risk class;
- decides whether a Specialist Reviewer is required;
- identifies hardware or control-plane checkpoints before implementation starts.

The Planner must not implement product/firmware changes.

The Planner may write task-planning artifacts only when explicitly authorized, such as:

```text
prompts/tasks/**
docs/feather-quantizer/loop/runs/<task>/**   # initialization only
```

If a valid human-authored task contract already exists, the Planner step may be skipped.

## Core role 2 — Runner

Purpose: implement the task inside the bounded Loop Engineering protocol.

The Runner uses `prompts/loop-runner.md` and:

- owns all implementation iterations;
- may self-review before handoff;
- runs local verification that the environment supports;
- records `state.json` and `iterations.md`;
- creates/updates one Draft inner PR when the platform supports it;
- never approves or merges its own work.

The Runner is the **only Codex role that normally edits implementation files**.

## Core role 3 — Reviewer

Purpose: independently challenge the candidate change.

The Reviewer must start from **fresh context**. It should not inherit the Runner's conversational reasoning or implementation narrative except where that information is itself committed evidence.

The Reviewer reads:

```text
AGENTS.md
project/spec/guardrail docs
task-specific prompt
PR diff
state.json
iterations.md
CI/check results
hardware evidence when applicable
```

The Reviewer is read-only with respect to repository implementation files. It does not fix findings.

Allowed verdicts:

```text
APPROVE
REQUEST_CHANGES
ESCALATE_HUMAN
```

Finding severities:

```text
BLOCKER   # cannot approve
MAJOR     # cannot approve
MINOR     # may approve with note if no correctness/safety impact
```

The Reviewer must cite concrete file/diff/test/evidence for every BLOCKER or MAJOR finding.

## Conditional role 4 — Specialist Reviewer

A fourth Codex agent is **not** part of every task. It is required when independent domain review materially reduces risk.

Specialist types:

```text
HARDWARE_EVIDENCE
SECURITY_PRIVACY
ARCHITECTURE
DEPENDENCY_TOOLCHAIN
HID_PROTOCOL
```

Default triggers include:

- hardware procedures, electrical assumptions, VBUS, flashing, real-device behavior;
- public capture/log artifacts or privacy-sensitive evidence;
- authentication, secrets, privilege boundaries, or security-sensitive code;
- cross-module architecture changes or shared parser abstractions;
- dependency, submodule, compiler, SDK, QMK/Vial/TinyUSB changes;
- HID descriptor/report interpretation that changes parser behavior or compatibility claims.

The Specialist is independent of both Runner and Reviewer and is normally read-only.

Specialist verdicts:

```text
CLEAR
FINDINGS
ESCALATE_HUMAN
```

A Specialist finding returns to the Runner through the normal review loop.

## Risk classes

### R0 — trivial / docs-only

Examples: typo, non-behavioral wording, deterministic metadata update.

Default topology:

```text
Runner -> CI -> Reviewer optional
```

Reviewer may be skipped only when the task contract or human explicitly allows it.

### R1 — normal engineering

Examples: Feather-local implementation, parser fixture, gesture logic, Vial integration.

Default topology:

```text
Planner -> Runner -> CI -> Reviewer -> Human merge
```

### R2 — high risk / hardware / security / architecture

Default topology:

```text
Planner -> Runner -> CI -> Reviewer + Specialist -> Human merge/checkpoint
```

Reviewer and Specialist should review independently before seeing each other's conclusions when practical.

### R3 — control-plane / protected / dependency boundary

Examples: `AGENTS.md`, workflows, protected upstream/shared paths, dependency or toolchain revisions.

Default action:

```text
STOP / ESCALATE_HUMAN
```

No agent count converts an unauthorized R3 change into an authorized one.

## Review timing

Do **not** invoke the independent Reviewer after every Runner iteration.

Normal timing:

```text
Runner performs bounded internal iterations
        |
        v
terminal handoff candidate
(PASS / BLOCKED_* / STOP)
        |
        v
CI
        |
        v
Independent Reviewer
```

Early review is justified only when:

- the Runner reaches a hardware handoff procedure with safety/privacy impact;
- an architectural/protected/dependency seam appears necessary;
- the Runner cannot make progress without choosing between materially different designs.

This avoids turning the human into a message relay and avoids excessive agent coordination.

## Review correction limit

A task allows at most **2 independent review correction cycles** by default.

```text
Reviewer REQUEST_CHANGES
        -> Runner fixes
        -> CI
        -> Reviewer re-reviews
```

If BLOCKER/MAJOR findings remain after the second review cycle, use:

```text
ESCALATE_HUMAN
```

Do not create an unbounded reviewer/runner ping-pong loop.

## Fresh-context rule

For independent review quality:

- Reviewer uses a separate Codex task/thread from Runner.
- Specialist uses a separate Codex task/thread from both.
- Reviewer does not receive the Runner chat transcript by default.
- The repository, task contract, diff, tests, and evidence are the source of truth.
- Explanations from the Runner may be requested only after a finding is identified, not used as the initial frame.

## Human responsibilities

The human remains the authority for:

- merge / ready-for-review approval;
- hardware operation and physical evidence collection;
- protected/control-plane authorization;
- architecture or product decisions when agents disagree;
- changing task scope or iteration/review limits;
- destructive or externally consequential actions.

The human should not be required to relay routine review findings between Codex roles when platform-supported PR review or task handoff can carry them.

## ChatGPT role

ChatGPT is **not a mandatory agent in the development loop**.

It may be used as an external advisor for product direction, architecture exploration, task portfolio planning, or human-requested escalation, but normal implementation/review should be capable of running entirely through Codex + CI + human approval.

## Preferred future automation

When repository/platform capabilities permit, automate this handoff:

```text
Runner Draft PR
    -> CI
    -> Codex Review
    -> REQUEST_CHANGES comments
    -> Runner resumes same PR
    -> CI
    -> Codex re-review
    -> APPROVE candidate
    -> Human ready/merge
```

Automation must not grant agents authority to merge, enable auto-merge, bypass hardware checkpoints, or weaken protected-path rules.
