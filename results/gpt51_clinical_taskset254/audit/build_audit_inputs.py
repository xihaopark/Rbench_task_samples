#!/usr/bin/env python3
import csv
import json
import random
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPORT = Path("/tmp/gpt51_clinical_taskset254_export")
TASK_ROOT = ROOT / "tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks"
OUT = ROOT / "analysis/gpt51_taskset254_audit"
SEED = 20260517
N = 50


def load_jsonl(path):
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def index_by_task(rows):
    return {row["task_id"]: row for row in rows}


def task_dir(task_id):
    parts = task_id.split("/")
    if len(parts) != 3 or parts[0] != "pharmaverse":
        return None
    return TASK_ROOT / parts[1] / parts[2]


def short_text(value, limit=500):
    if value is None:
        return ""
    value = str(value)
    value = value.replace("\r", "")
    return value if len(value) <= limit else value[:limit] + "\n...[truncated]"


def case_summary(row):
    cases = row.get("test_cases") or []
    if not cases:
        return {}
    case = cases[0]
    comparison = case.get("comparison") or {}
    compare_bits = []
    for name, payload in comparison.items():
        compare_bits.append(f"{name}: match={payload.get('match')} reason={payload.get('reason', '')}")
    return {
        "case": case.get("case", ""),
        "case_status": case.get("status", ""),
        "tier": case.get("tier", ""),
        "message": case.get("message", ""),
        "returncode": case.get("returncode", ""),
        "stderr": short_text(case.get("stderr", ""), 1200),
        "comparison": " | ".join(compare_bits),
    }


def read_task_meta(tdir):
    task_json = tdir / "task.json"
    solution = tdir / "solution.R"
    meta = {}
    if task_json.exists():
        with task_json.open() as f:
            data = json.load(f)
        meta["reference_prompt"] = data.get("instruct_prompt", "")
        meta["expected_artifacts"] = ", ".join(a.get("path", "") for a in data.get("expected", {}).get("artifacts", []))
        meta["packages"] = ", ".join(data.get("packages", []))
        meta["function_name"] = data.get("function_name", "")
    else:
        meta["reference_prompt"] = ""
        meta["expected_artifacts"] = ""
        meta["packages"] = ""
        meta["function_name"] = ""
    meta["reference_solution_head"] = solution.read_text(errors="replace")[:3000] if solution.exists() else ""
    return meta


def artifact_from_archive(row, filename):
    archive = row.get("candidate_archive")
    if not archive:
        return ""
    path = ROOT / archive / filename
    return path.read_text(errors="replace") if path.exists() else ""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    current_gen = index_by_task(load_jsonl(EXPORT / "current_prompt/generated_solutions.jsonl"))
    simple_gen = index_by_task(load_jsonl(EXPORT / "simple_prompt/generated_solutions.jsonl"))
    current_eval = index_by_task(load_jsonl(EXPORT / "current_prompt/evaluation_results.jsonl"))
    simple_eval = index_by_task(load_jsonl(EXPORT / "simple_prompt/evaluation_results.jsonl"))

    task_ids = list(current_eval)
    sample = random.Random(SEED).sample(task_ids, N)

    manifest_rows = []
    for i, task_id in enumerate(sample, 1):
        tdir = task_dir(task_id)
        current_row = current_eval[task_id]
        simple_row = simple_eval[task_id]
        current_case = case_summary(current_row)
        simple_case = case_summary(simple_row)
        meta = read_task_meta(tdir) if tdir and tdir.exists() else {
            "reference_prompt": "",
            "expected_artifacts": "",
            "packages": "",
            "function_name": "",
            "reference_solution_head": "",
        }
        current_prompt = current_gen.get(task_id, {}).get("prompt", "")
        simple_prompt = simple_gen.get(task_id, {}).get("prompt", "")
        current_solution = current_gen.get(task_id, {}).get("solution", "")
        simple_solution = simple_gen.get(task_id, {}).get("solution", "")

        row = {
            "idx": i,
            "task_id": task_id,
            "task_dir": str(tdir.relative_to(ROOT)) if tdir and tdir.exists() else "",
            "package": current_row.get("package", ""),
            "function_name": meta["function_name"],
            "expected_artifacts": meta["expected_artifacts"],
            "current_status": current_row.get("status", ""),
            "current_tier": current_case.get("tier", ""),
            "current_message": current_case.get("message", current_row.get("message", "")),
            "current_comparison": current_case.get("comparison", ""),
            "simple_status": simple_row.get("status", ""),
            "simple_tier": simple_case.get("tier", ""),
            "simple_message": simple_case.get("message", simple_row.get("message", "")),
            "simple_comparison": simple_case.get("comparison", ""),
        }
        manifest_rows.append(row)

        sample_file = OUT / f"sample_{i:02d}.md"
        sample_file.write_text(
            "\n".join([
                f"# Sample {i:02d}: {task_id}",
                "",
                f"- task_dir: `{row['task_dir']}`",
                f"- package/function: `{row['package']}` / `{row['function_name']}`",
                f"- expected_artifacts: `{row['expected_artifacts']}`",
                f"- current_status: `{row['current_status']}` tier=`{row['current_tier']}`",
                f"- simple_status: `{row['simple_status']}` tier=`{row['simple_tier']}`",
                "",
                "## Reference Prompt",
                "```text",
                meta["reference_prompt"],
                "```",
                "",
                "## Current Prompt",
                "```text",
                current_prompt,
                "```",
                "",
                "## Simple Prompt",
                "```text",
                simple_prompt,
                "```",
                "",
                "## Current Evaluation",
                "```text",
                json.dumps(current_case, indent=2, ensure_ascii=False),
                "```",
                "",
                "## Simple Evaluation",
                "```text",
                json.dumps(simple_case, indent=2, ensure_ascii=False),
                "```",
                "",
                "## Reference Solution Head",
                "```r",
                meta["reference_solution_head"],
                "```",
                "",
                "## Current Solution",
                "```r",
                current_solution[:5000],
                "```",
                "",
                "## Simple Solution",
                "```r",
                simple_solution[:5000],
                "```",
                "",
                "## Current Candidate Prompt File",
                "```text",
                artifact_from_archive(current_row, "prompt.txt")[:3000],
                "```",
                "",
                "## Simple Candidate Prompt File",
                "```text",
                artifact_from_archive(simple_row, "prompt.txt")[:3000],
                "```",
            ]),
            encoding="utf-8",
        )

    with (OUT / "sample_manifest.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(manifest_rows[0]))
        writer.writeheader()
        writer.writerows(manifest_rows)

    groups = []
    for start in range(0, N, 10):
        group = manifest_rows[start:start + 10]
        group_path = OUT / f"group_{start // 10 + 1}.txt"
        group_path.write_text("\n".join(f"{r['idx']:02d}\t{r['task_id']}\t{r['task_dir']}" for r in group) + "\n")
        groups.append(str(group_path.relative_to(ROOT)))

    rubric = textwrap.dedent(
        """
        # Audit Rubric

        For each sampled task, assign one primary cause:

        - prompt_wrong: generated prompt contradicts task.json/reference or asks for the wrong API/output.
        - prompt_reference_mismatch: task.json/current prompt/reference solution/expected artifacts disagree.
        - data_or_fixture_issue: inputs are malformed, missing, unusable, or inconsistent with reference expectations.
        - evaluator_or_stub_issue: Docker/stub/comparator behavior appears inconsistent with reference or masks task behavior.
        - llm_wrong: prompt/reference/data look coherent; generated code made an implementation/output/API mistake.
        - unclear_needs_rerun: the available artifact is insufficient; rerun or deeper execution is needed.

        Record both current_prompt and simple_prompt when they differ, but choose the primary root cause for the task.
        Include a short evidence quote or file/path pointer.
        """
    ).strip()
    (OUT / "rubric.md").write_text(rubric + "\n")

    print(f"Wrote {OUT / 'sample_manifest.csv'}")
    print("Groups:")
    for group in groups:
        print(group)


if __name__ == "__main__":
    main()
