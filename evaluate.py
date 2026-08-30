"""
micro1 Hackathon Benchmark Evaluation Runner
=============================================

Evaluates dispute resolution approaches against the 10-case benchmark dataset.

Modes:
- baseline: Single Gemini prompt with no tools/policy (naive approach)
- advanced: Multi-agent orchestrator with skills, memory, and function calling

Scoring Rubric:
1. Primary Verdict Accuracy — Does the action code match ground truth?
2. Financial Math Accuracy — Is the refund amount within $0.01 of expected?
3. Avg Latency per Task — Speed (vs ~10-15 min human baseline)
4. Avg Estimated API Cost — Cost efficiency
"""

import json
import os
import sys
import glob
import time

# Load .env file for API keys
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    with open(_env_path, "r") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _key, _val = _line.split("=", 1)
                os.environ.setdefault(_key.strip(), _val.strip())


def run_evaluation(mode="baseline"):
    """
    Evaluates benchmark test cases against the micro1 Hackathon Rubric.
    
    Args:
        mode: 'baseline' for single-prompt or 'advanced' for multi-agent pipeline
    """
    cases_pattern = os.path.join(os.path.dirname(__file__), "data", "cases", "*.json")
    case_files = sorted(glob.glob(cases_pattern))

    if not case_files:
        print("Error: No test cases found in data/cases/")
        return

    # ── Import the appropriate solver ──
    if mode == "baseline":
        from baseline import solve_baseline_ticket
        solver = solve_baseline_ticket
    elif mode == "advanced":
        from agent import solve_advanced_ticket, get_orchestrator
        orchestrator = get_orchestrator()
        orchestrator.memory.clear()  # Fresh memory for each evaluation run
        solver = solve_advanced_ticket
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'baseline' or 'advanced'.")

    # ── Header ──
    print()
    print("=" * 100)
    print(f"  MICRO1 HACKATHON BENCHMARK EVALUATION — MODE: [{mode.upper()}]")
    print(f"  Dataset: {len(case_files)} Ground-Truth Test Cases")
    if mode == "advanced":
        print(f"  Architecture: Multi-Agent Orchestrator with Skills, Memory & Function Calling")
    else:
        print(f"  Architecture: Single Direct Gemini Prompt (No Tools, No Policy)")
    print("=" * 100)
    print()

    # ── Evaluation Loop ──
    results = []
    correct_verdicts = 0
    correct_refund_amounts = 0
    total_cost = 0.0
    total_latency = 0.0

    for idx, filepath in enumerate(case_files, 1):
        with open(filepath, "r", encoding="utf-8") as f:
            case_data = json.load(f)

        case_id = case_data.get("case_id")
        title = case_data.get("title")
        gt = case_data.get("ground_truth_verdict")

        # Run solver
        output = solver(case_data)

        pred_action = output.get("predicted_action")
        gt_action = gt.get("action")

        pred_refund = output.get("refund_amount", 0.0)
        gt_refund = gt.get("refund_amount", 0.0)

        verdict_match = (pred_action == gt_action)
        refund_match = (abs(pred_refund - gt_refund) < 0.01)

        if verdict_match:
            correct_verdicts += 1
        if refund_match:
            correct_refund_amounts += 1

        total_cost += output.get("estimated_cost_usd", 0.0)
        total_latency += output.get("latency_seconds", 0.0)

        # Both must match for PASS
        is_pass = verdict_match and refund_match
        status_icon = "PASS" if is_pass else "FAIL"

        results.append({
            "id": case_id,
            "title": title,
            "pred_action": pred_action,
            "gt_action": gt_action,
            "pred_refund": f"${pred_refund:.2f}",
            "gt_refund": f"${gt_refund:.2f}",
            "verdict_match": verdict_match,
            "refund_match": refund_match,
            "status": status_icon,
            "reasoning": output.get("reasoning"),
            "tools_called": output.get("tools_called", []),
        })

        # Print result line
        print(f"  [{status_icon:4s}] {case_id}: {title[:40]:<40}")
        print(f"         Pred: {pred_action:<40} | GT: {gt_action}")
        if not is_pass:
            if not verdict_match:
                print(f"         X Verdict mismatch")
            if not refund_match:
                print(f"         X Refund: ${pred_refund:.2f} (expected ${gt_refund:.2f})")
        if mode == "advanced" and output.get("tools_called"):
            print(f"         Tools: {', '.join(output['tools_called'])}")
        print()

    # ── Summary Scoreboard ──
    total_cases = len(case_files)
    verdict_acc = (correct_verdicts / total_cases) * 100
    refund_acc = (correct_refund_amounts / total_cases) * 100
    avg_latency = total_latency / total_cases
    avg_cost = total_cost / total_cases

    print("=" * 100)
    print(f"  SUMMARY SCOREBOARD — [{mode.upper()}] (micro1 Hackathon Rubric)")
    print("=" * 100)
    print(f"  * Total Benchmark Cases    : {total_cases}")
    print(f"  * Primary Verdict Accuracy : {correct_verdicts}/{total_cases} ({verdict_acc:.1f}%)")
    print(f"  * Financial Math Accuracy  : {correct_refund_amounts}/{total_cases} ({refund_acc:.1f}%)")
    print(f"  * Avg Latency per Task     : {avg_latency:.3f} seconds (vs ~10-15 mins human baseline)")
    print(f"  * Avg Estimated API Cost   : ${avg_cost:.4f} USD")
    print("=" * 100)

    if mode == "advanced":
        from agent import get_orchestrator
        orch = get_orchestrator()
        print(f"\n  Memory: {orch.memory.summary()}")
        print()

    return {
        "mode": mode,
        "total_cases": total_cases,
        "verdict_accuracy": correct_verdicts,
        "refund_accuracy": correct_refund_amounts,
        "avg_latency": avg_latency,
        "avg_cost": avg_cost,
        "results": results
    }


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "baseline"
    run_evaluation(mode=mode)
