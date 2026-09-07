#!/usr/bin/env python3
import json
import pathlib
import re
import sys
from datetime import datetime

ALLOWED_STATUS = {
    "NOT_STARTED",
    "CONTINUE",
    "PASS",
    "BLOCKED_HARDWARE",
    "BLOCKED_ENVIRONMENT",
    "STOP",
}
ALLOWED_GATE = {"PASS", "FAIL", "NA", "UNKNOWN"}
HARD_GATES = [f"HG{i}" for i in range(1, 11)]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: verify-loop-state.py <state.json>")

    path = pathlib.Path(sys.argv[1])
    if not path.is_file():
        fail(f"state file not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON: {exc}")

    required = {
        "task_id",
        "branch",
        "status",
        "iteration",
        "max_iterations",
        "acceptance_criteria",
        "quality",
        "hardware",
        "updated_at",
    }
    missing = sorted(required - data.keys())
    if missing:
        fail(f"missing required keys: {', '.join(missing)}")

    if not isinstance(data["task_id"], str) or not data["task_id"].strip():
        fail("task_id must be a non-empty string")

    branch = data["branch"]
    if not isinstance(branch, str) or not branch.startswith("loop/"):
        fail("branch must start with 'loop/'")

    status = data["status"]
    if status not in ALLOWED_STATUS:
        fail(f"invalid status: {status}")

    iteration = data["iteration"]
    max_iterations = data["max_iterations"]
    if not isinstance(iteration, int) or iteration < 0 or iteration > 5:
        fail("iteration must be an integer from 0 to 5")
    if not isinstance(max_iterations, int) or max_iterations < 1 or max_iterations > 5:
        fail("max_iterations must be an integer from 1 to 5")
    if iteration > max_iterations:
        fail("iteration exceeds max_iterations")

    criteria = data["acceptance_criteria"]
    if not isinstance(criteria, list) or not criteria:
        fail("acceptance_criteria must be a non-empty list")

    for idx, criterion in enumerate(criteria, start=1):
        if not isinstance(criterion, dict):
            fail(f"criterion {idx} must be an object")
        for key in ("id", "description", "status", "evidence"):
            if key not in criterion:
                fail(f"criterion {idx} missing {key}")
        if criterion["status"] not in {"PASS", "FAIL", "UNKNOWN", "NA"}:
            fail(f"criterion {idx} has invalid status")

    quality = data["quality"]
    if not isinstance(quality, dict):
        fail("quality must be an object")
    score = quality.get("score")
    if not isinstance(score, int) or not 0 <= score <= 100:
        fail("quality.score must be 0..100")

    gates = quality.get("hard_gates")
    if not isinstance(gates, dict):
        fail("quality.hard_gates must be an object")
    for gate in HARD_GATES:
        value = gates.get(gate)
        if value not in ALLOWED_GATE:
            fail(f"{gate} must be one of {sorted(ALLOWED_GATE)}")

    hardware = data["hardware"]
    if not isinstance(hardware, dict):
        fail("hardware must be an object")
    requirement = hardware.get("requirement")
    if requirement not in {"NONE", "REQUIRED_FOR_PASS", "EXPECTED_CHECKPOINT"}:
        fail("invalid hardware.requirement")
    if not isinstance(hardware.get("evidence_available"), bool):
        fail("hardware.evidence_available must be boolean")

    same_failure_count = data.get("same_failure_count", 0)
    if not isinstance(same_failure_count, int) or not 0 <= same_failure_count <= 2:
        fail("same_failure_count must be 0..2")
    if same_failure_count >= 2 and status in {"CONTINUE", "PASS"}:
        fail("same unresolved failure occurred twice; status must STOP/BLOCKED")

    try:
        datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
    except Exception:
        fail("updated_at must be an ISO-8601 date-time")

    if status == "PASS":
        bad_criteria = [c["id"] for c in criteria if c["status"] != "PASS"]
        if bad_criteria:
            fail(f"PASS task has non-PASS acceptance criteria: {', '.join(bad_criteria)}")

        bad_gates = [g for g in HARD_GATES if gates[g] not in {"PASS", "NA"}]
        if bad_gates:
            fail(f"PASS task has unresolved hard gates: {', '.join(bad_gates)}")

        if score < 90:
            fail("PASS task requires quality.score >= 90")

        if requirement == "REQUIRED_FOR_PASS" and not hardware["evidence_available"]:
            fail("PASS task requires hardware evidence")

    print(
        f"loop-state OK: task={data['task_id']} status={status} "
        f"iteration={iteration}/{max_iterations} score={score}"
    )


if __name__ == "__main__":
    main()
