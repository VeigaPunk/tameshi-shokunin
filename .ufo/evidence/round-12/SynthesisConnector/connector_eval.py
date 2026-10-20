#!/usr/bin/env python3
"""connector_eval.py - Evaluate C1 baseline precondition vs C2 witness attribution

Demonstrates the orthogonal decision table connecting repeat-control (C1)
and witness-scoped kill analysis (C2) without creating an operational dependency.
"""
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parents[3]

def load_decision_table():
    table_path = BASE_DIR / "decision_table.json"
    with open(table_path, "r", encoding="utf-8") as f:
        return json.load(f)["matrix"]

def match_verdict(matrix, c1_finding, c1_exit, c2_outcome):
    # Check exact match first
    for row in matrix:
        if row["c1_finding"] == c1_finding and row["c1_exit"] == c1_exit:
            if row["c2_outcome"] == c2_outcome or row["c2_outcome"] == "*":
                return row
    return {
        "joint_verdict": "UNKNOWN_COMBINATION",
        "valid_attribution": False,
        "enters_witness_rate": False,
        "enters_aggregate_rate": False,
        "epistemic_status": f"Unmatched combination: C1({c1_finding}, {c1_exit}) x C2({c2_outcome})"
    }

def evaluate_cases():
    matrix = load_decision_table()
    cases = []

    # Case Group 1: BaselineControl Scenarios
    # Scenario A: Flaky suite (passes run 1, fails run 2)
    # Runner alone gave D1 KILLED (false positive).
    # Under C1 repeat-control: run 1 pass, run 2 fail -> controls_mismatch (exit 1).
    res_a = match_verdict(matrix, "controls_mismatch", 1, "killed-on-witness")
    cases.append({
        "case_id": "BaselineControl_ScenarioA",
        "description": "Flaky suite passing run 1, failing run 2 on harmless D1",
        "observed_runner_verdict": "KILLED (100% false positive kill rate)",
        "c1_finding": "controls_mismatch",
        "c1_exit": 1,
        "c2_outcome": "killed-on-witness",
        "joint_verdict": res_a["joint_verdict"],
        "valid_attribution": res_a["valid_attribution"],
        "epistemic_status": res_a["epistemic_status"]
    })

    # Scenario B: Flaky suite failing on run 1
    # Runner aborted (die_setup, exit 2).
    # Under C1: controls_mismatch (or baseline_nonzero, depending on repeat runs).
    res_b = match_verdict(matrix, "baseline_nonzero", 2, "inconclusive")
    cases.append({
        "case_id": "BaselineControl_ScenarioB",
        "description": "Flaky suite failing on run 1, passing run 2",
        "observed_runner_verdict": "ABORT (die_setup exit 2)",
        "c1_finding": "baseline_nonzero",
        "c1_exit": 2,
        "c2_outcome": "inconclusive",
        "joint_verdict": res_b["joint_verdict"],
        "valid_attribution": res_b["valid_attribution"],
        "epistemic_status": res_b["epistemic_status"]
    })

    # Scenario C: Nondeterministic stdout (timestamps/PID) but exit 0
    # Runner alone: passed as clean CONTROL: GREEN and D1 SURVIVED.
    # Under C1: controls_mismatch (exit 1) due to byte variance.
    res_c = match_verdict(matrix, "controls_mismatch", 1, "survived")
    cases.append({
        "case_id": "BaselineControl_ScenarioC",
        "description": "Nondeterministic stdout (timestamps/PID) with exit 0",
        "observed_runner_verdict": "SURVIVED (runner blind to stream jitter)",
        "c1_finding": "controls_mismatch",
        "c1_exit": 1,
        "c2_outcome": "survived",
        "joint_verdict": res_c["joint_verdict"],
        "valid_attribution": res_c["valid_attribution"],
        "epistemic_status": res_c["epistemic_status"]
    })

    # Scenario D: Persistent nonzero baseline
    # Runner: die_setup (exit 2).
    # Under C1: baseline_nonzero (exit 2).
    res_d = match_verdict(matrix, "baseline_nonzero", 2, "survived")
    cases.append({
        "case_id": "BaselineControl_ScenarioD",
        "description": "Persistent broken baseline (always exit 1)",
        "observed_runner_verdict": "ABORT (die_setup exit 2)",
        "c1_finding": "baseline_nonzero",
        "c1_exit": 2,
        "c2_outcome": "survived",
        "joint_verdict": res_d["joint_verdict"],
        "valid_attribution": res_d["valid_attribution"],
        "epistemic_status": res_d["epistemic_status"]
    })

    # Case Group 2: Pinned JS Kimi-Census Witness Sweep (10 defects)
    # Pristine control: GREEN 43/43, byte-stable, exit 0 -> controls_match (exit 0)
    js_witnesses = [
        ("D1", "killed-on-witness"),
        ("D2", "survived"),
        ("D3", "killed-on-witness"),
        ("D4", "killed-on-witness"),
        ("D5", "killed-on-witness"),
        ("D6", "killed-on-witness"),
        ("D7", "killed-on-witness"),
        ("D8", "killed-on-witness"),
        ("D9", "killed-on-witness"),
        ("D10", "survived")
    ]
    for defect, outcome in js_witnesses:
        res = match_verdict(matrix, "controls_match", 0, outcome)
        cases.append({
            "case_id": f"JS_KimiCensus_{defect}",
            "description": f"JS kimi-census pinned sweep defect {defect}",
            "observed_runner_verdict": "KILLED" if "killed" in outcome else "SURVIVED",
            "c1_finding": "controls_match",
            "c1_exit": 0,
            "c2_outcome": outcome,
            "joint_verdict": res["joint_verdict"],
            "valid_attribution": res["valid_attribution"],
            "epistemic_status": res["epistemic_status"]
        })

    # Case Group 3: Synthetic Boundary Probes
    # Accidental kill on valid control
    res_acc = match_verdict(matrix, "controls_match", 0, "accidental")
    cases.append({
        "case_id": "Synthetic_AccidentalKill",
        "description": "Mutant fails suite, but fails non-witness assertions on clean baseline",
        "observed_runner_verdict": "KILLED",
        "c1_finding": "controls_match",
        "c1_exit": 0,
        "c2_outcome": "accidental",
        "joint_verdict": res_acc["joint_verdict"],
        "valid_attribution": res_acc["valid_attribution"],
        "epistemic_status": res_acc["epistemic_status"]
    })

    # Tampered snapshot
    res_tamp = match_verdict(matrix, "snapshot_tampered", 2, "killed-on-witness")
    cases.append({
        "case_id": "Synthetic_SnapshotTampered",
        "description": "Fixture input modified or hash mismatch under --snapshot",
        "observed_runner_verdict": "N/A",
        "c1_finding": "snapshot_tampered",
        "c1_exit": 2,
        "c2_outcome": "killed-on-witness",
        "joint_verdict": res_tamp["joint_verdict"],
        "valid_attribution": res_tamp["valid_attribution"],
        "epistemic_status": res_tamp["epistemic_status"]
    })

    return cases

def main():
    cases = evaluate_cases()
    output_path = BASE_DIR / "observed_eval.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"evaluated_cases_count": len(cases), "cases": cases}, f, indent=2)

    print(f"=== Evaluated {len(cases)} cases across C1 x C2 Decision Table ===")
    for c in cases:
        print(f"[{c['case_id']}] C1:({c['c1_finding']}, exit={c['c1_exit']}) x C2:{c['c2_outcome']} => {c['joint_verdict']} (valid={c['valid_attribution']})")

if __name__ == "__main__":
    main()
