#!/usr/bin/env python3
"""Build a first-pass contract manifest for the clinical taskset254 run.

This is a static/archival preflight. It does not execute R. It merges:

- task metadata and reference solution files from RBioBench
- current/simple generated prompts and strict evaluation results in this export
- lightweight regex evidence from solution.R, prompts, and comparison records

The output is intended for triage, not as a final keep/delete decision.
"""

from __future__ import annotations

import csv
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


AUDIT_DIR = Path(__file__).resolve().parent
RESULT_ROOT = AUDIT_DIR.parent
RBIOBENCH_ROOT = Path(
    os.environ.get(
        "RBIOBENCH_ROOT",
        "/mnt/workspace-storage/lab_workspace/projects/RBioBench",
    )
)
TASK_ROOT = RBIOBENCH_ROOT / "tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks"

CURRENT_GEN = RESULT_ROOT / "current_prompt/generated_solutions.jsonl"
CURRENT_EVAL = RESULT_ROOT / "current_prompt/evaluation_results.jsonl"
SIMPLE_GEN = RESULT_ROOT / "simple_prompt/generated_solutions.jsonl"
SIMPLE_EVAL = RESULT_ROOT / "simple_prompt/evaluation_results.jsonl"

OUT_JSONL = AUDIT_DIR / "contract_manifest.jsonl"
OUT_CSV = AUDIT_DIR / "contract_manifest.csv"
OUT_SUMMARY = AUDIT_DIR / "contract_manifest_summary.md"


DELETE_NAME_PATTERNS = [
    r"(^|/)assert_",
    r"(^|/)check_",
    r"(^|/)print\.",
    r"create_html",
    r"create_pptx",
    r"create_qmd",
    r"pptx",
    r"qmd",
    r"_doc$",
    r"add_qmd",
]

INTERNAL_HINT_PATTERNS = [
    r":::",
    r"asNamespace\s*\(",
    r"get\s*\(\s*['\"][A-Za-z0-9_.]+['\"]\s*,\s*envir\s*=\s*asNamespace",
]

SUSPICIOUS_PREVIEW_TOKENS = {
    "clinical_placeholders": ["AVAL", "AVISITN", "USUBJID", "PARAMCD", "ADT"],
    "rlang_expr_placeholders": ["exprs(", "quo(", "quos(", "!!", ":="],
    "derivation_placeholders": ["by_vars", "set_values_to", "analysis_value", "mean("],
    "generic_placeholders": ["test_value", "item_a", "item_b", "active"],
    "unit_mismatch_placeholders": ["SYSBP", "DIABP", "PULSE", "WEIGHT", "HEIGHT"],
}

SCALARISH_FILE_PATTERNS = [
    "arg",
    "val",
    "unit",
    "date_imputation",
    "month",
    "format",
    "library",
    "name",
    "label",
    "target",
    "source",
]

CSV_FIELDS = [
    "task_id",
    "package",
    "function_name",
    "level",
    "contract_status",
    "status_reasons",
    "current_status",
    "current_tier",
    "simple_status",
    "simple_tier",
    "expected_artifacts_task_json",
    "artifacts_written_by_solution",
    "artifacts_compared_by_current_eval",
    "artifacts_compared_by_simple_eval",
    "input_files_declared",
    "input_files_read_by_solution",
    "input_files_previewed_current",
    "functions_called_by_solution",
    "functions_requested_by_task_prompt",
    "uses_internal_helper",
    "uses_hidden_in_script_data",
    "result_assignment_count",
    "overwrites_result",
    "fixture_semantic_flags",
    "task_dir",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def index_by_task(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {row["task_id"]: row for row in rows}


def task_dir(task_id: str) -> Path | None:
    parts = task_id.split("/")
    if len(parts) != 3 or parts[0] != "pharmaverse":
        return None
    return TASK_ROOT / parts[1] / parts[2]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def unique_sorted(values: list[str]) -> list[str]:
    return sorted({v for v in values if v})


def artifact_paths_from_expected(task_json: dict[str, Any]) -> list[str]:
    expected = task_json.get("expected") or {}
    artifacts = expected.get("artifacts") or []
    checks = expected.get("checks") or []
    paths = [a.get("path", "") for a in artifacts]
    paths.extend(c.get("target", "") for c in checks if c.get("type") == "file_exists")
    return unique_sorted(paths)


def artifact_paths_from_solution(code: str) -> list[str]:
    paths: list[str] = []
    dir_vars = {
        match.group(1)
        for match in re.finditer(
            r"(?m)^\s*([A-Za-z][A-Za-z0-9_.]*)\s*<-\s*['\"]outputs['\"]",
            code,
        )
    }
    patterns = [
        r"['\"](outputs/[^'\"]+)['\"]",
        r"file\.path\s*\(\s*['\"]outputs['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, code):
            value = match.group(1)
            if not value.startswith("outputs/"):
                value = f"outputs/{value}"
            if re.search(r"\.(csv|tsv|rds|txt|json|html|qmd|pptx|png|pdf)$", value):
                paths.append(value)
    for var in dir_vars:
        pattern = rf"file\.path\s*\(\s*{re.escape(var)}\s*,\s*['\"]([^'\"]+)['\"]\s*\)"
        for match in re.finditer(pattern, code):
            value = f"outputs/{match.group(1)}"
            if re.search(r"\.(csv|tsv|rds|txt|json|html|qmd|pptx|png|pdf)$", value):
                paths.append(value)
    return unique_sorted(paths)


def artifacts_compared(eval_row: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for case in eval_row.get("test_cases") or []:
        comparison = case.get("comparison") or {}
        for name in comparison:
            paths.append(f"outputs/{name}" if not name.startswith("outputs/") else name)
    return unique_sorted(paths)


def input_files_from_text(text: str) -> list[str]:
    paths = re.findall(r"inputs/[A-Za-z0-9_.-]+\.(?:tsv|csv|rds|txt|json|qmd|pptx)", text)
    paths.extend(
        f"inputs/{m}"
        for m in re.findall(
            r"file\.path\s*\(\s*['\"]inputs['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)",
            text,
        )
    )
    return unique_sorted(paths)


def parse_prompt_previews(prompt: str) -> dict[str, list[str]]:
    previews: dict[str, list[str]] = {}
    marker = "## Inputs preview"
    if marker not in prompt:
        return previews
    tail = prompt.split(marker, 1)[1]
    current_name = None
    current_lines: list[str] = []
    for raw in tail.splitlines():
        line = raw.rstrip("\n")
        heading = re.match(r"^###\s+(.+?)\s+\(\d+\s+bytes\)", line)
        if heading:
            if current_name:
                previews[current_name] = [x for x in current_lines if x.strip()][:12]
            current_name = heading.group(1).strip()
            current_lines = []
            continue
        if current_name:
            if line.startswith("## "):
                break
            current_lines.append(line)
    if current_name:
        previews[current_name] = [x for x in current_lines if x.strip()][:12]
    return previews


def functions_from_code(code: str) -> list[str]:
    calls = re.findall(r"\b([A-Za-z][A-Za-z0-9_.]*)::([A-Za-z][A-Za-z0-9_.]*)\s*\(", code)
    funcs = [f"{pkg}::{fn}" for pkg, fn in calls]
    internal_gets = re.findall(
        r"get\s*\(\s*['\"]([A-Za-z][A-Za-z0-9_.]*)['\"]\s*,\s*envir\s*=\s*asNamespace\s*\(\s*['\"]([A-Za-z][A-Za-z0-9_.]*)['\"]\s*\)",
        code,
    )
    funcs.extend(f"{pkg}::{fn}" for fn, pkg in internal_gets)
    return unique_sorted(funcs)


def functions_from_prompt(task_json: dict[str, Any]) -> list[str]:
    prompt = task_json.get("instruct_prompt", "")
    funcs = [f"{task_json.get('package')}::{task_json.get('function_name')}"]
    calls = re.findall(r"\b([A-Za-z][A-Za-z0-9_.]*)::([A-Za-z][A-Za-z0-9_.]*)", prompt)
    funcs.extend(f"{pkg}::{fn}" for pkg, fn in calls)
    return unique_sorted(funcs)


def columns_from_solution(code: str) -> list[str]:
    cols = re.findall(r"\$([A-Za-z][A-Za-z0-9_.]*)", code)
    cols.extend(re.findall(r"['\"]([A-Z][A-Z0-9_]{1,20})['\"]\s*%in%\s*names", code))
    cols.extend(re.findall(r"names\s*\([^)]*\)\s*==\s*['\"]([A-Z][A-Z0-9_]{1,20})['\"]", code))
    return unique_sorted(cols)


def current_tier(eval_row: dict[str, Any]) -> str:
    for case in eval_row.get("test_cases") or []:
        if case.get("tier"):
            return case["tier"]
    return ""


def uses_internal_helper(code: str, prompt: str) -> bool:
    haystack = f"{code}\n{prompt}"
    return any(re.search(pattern, haystack) for pattern in INTERNAL_HINT_PATTERNS)


def hidden_data_flag(code: str, input_reads: list[str]) -> bool:
    if input_reads:
        return False
    return bool(re.search(r"\b(data\.frame|tibble|tribble|c)\s*\(", code))


def result_assignment_count(code: str) -> int:
    return len(re.findall(r"(?m)^\s*result\s*(?:<-|=)", code))


def overwrites_result_flag(code: str) -> bool:
    assignments = result_assignment_count(code)
    if assignments <= 1:
        return False
    bare_assignments = re.findall(r"(?m)^\s*result\s*<-\s*([A-Za-z][A-Za-z0-9_.]*)\s*$", code)
    return bool(bare_assignments)


def fixture_flags(previews: dict[str, list[str]]) -> list[str]:
    flags: list[str] = []
    for filename, lines in previews.items():
        text = "\n".join(lines)
        lower_name = filename.lower()
        for label, tokens in SUSPICIOUS_PREVIEW_TOKENS.items():
            if any(token in text for token in tokens):
                flags.append(label)
        if any(pat in lower_name for pat in SCALARISH_FILE_PATTERNS):
            if any(token in text for token in ["AVAL", "AVISITN", "USUBJID", "exprs(", "by_vars", "set_values_to"]):
                flags.append(f"scalarish_input_has_complex_placeholder:{filename}")
        if "unit" in lower_name and any(token in text for token in ["AVAL", "AVISITN", "USUBJID", "SYSBP", "DIABP"]):
            flags.append(f"unit_input_has_non_unit_values:{filename}")
    return unique_sorted(flags)


def delete_candidate(task_id: str, function_name: str, prompt: str) -> bool:
    haystack = f"{task_id}/{function_name} {prompt}"
    return any(re.search(pattern, haystack, flags=re.IGNORECASE) for pattern in DELETE_NAME_PATTERNS)


def artifact_mismatch_reasons(
    expected: list[str],
    written: list[str],
    current_compared: list[str],
    simple_compared: list[str],
) -> list[str]:
    reasons: list[str] = []
    expected_set = set(expected)
    written_set = set(written)
    compared_set = set(current_compared) | set(simple_compared)
    if expected_set and written_set and not expected_set <= written_set:
        reasons.append("solution_missing_expected_artifact")
    if compared_set - expected_set:
        reasons.append("evaluator_compares_artifact_not_in_task_json")
    if expected_set - compared_set and compared_set:
        reasons.append("task_json_expected_artifact_not_compared_in_results")
    return reasons


def classify(
    task_id: str,
    function_name: str,
    prompt: str,
    artifact_reasons: list[str],
    fixture_reasons: list[str],
    internal: bool,
    hidden_data: bool,
    overwrite: bool,
    delete_like: bool,
    current_eval: dict[str, Any],
    simple_eval: dict[str, Any],
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if artifact_reasons:
        reasons.extend(artifact_reasons)
    if overwrite:
        reasons.append("result_overwrite_or_echo_suspected")
    if hidden_data:
        reasons.append("hidden_in_script_data_suspected")
    if fixture_reasons:
        reasons.extend(fixture_reasons)
    if internal:
        reasons.append("uses_internal_helper_or_namespace_access")
    if delete_like:
        reasons.append("helper_assertion_doc_or_internal_only_candidate")
    both_timeout = current_eval.get("status") == "TIMEOUT" and simple_eval.get("status") == "TIMEOUT"
    if both_timeout:
        reasons.append("current_and_simple_timeout")

    if artifact_reasons or overwrite or hidden_data:
        return "D_QUARANTINE_CONTRACT", unique_sorted(reasons)
    if fixture_reasons:
        return "C_REPAIR_FIXTURE", unique_sorted(reasons)
    if delete_like:
        return "E_DELETE_CANDIDATE", unique_sorted(reasons)
    if both_timeout:
        return "F_RERUN_TIMEOUT", unique_sorted(reasons)
    if internal or "Required outputs" not in prompt or "outputs/" not in prompt:
        return "B_REPAIR_PROMPT", unique_sorted(reasons or ["needs_explicit_contract_prompt_review"])
    return "A_KEEP_CANDIDATE", unique_sorted(reasons)


def task_record(
    task_id: str,
    current_eval: dict[str, Any],
    simple_eval: dict[str, Any],
    current_gen: dict[str, Any],
    simple_gen: dict[str, Any],
) -> dict[str, Any]:
    tdir = task_dir(task_id)
    task_json = read_json(tdir / "task.json") if tdir else {}
    solution_code = read_text(tdir / "solution.R") if tdir else ""
    task_prompt = task_json.get("instruct_prompt", "")
    current_prompt = current_gen.get("prompt", "")
    simple_prompt = simple_gen.get("prompt", "")
    previews = parse_prompt_previews(current_prompt) or parse_prompt_previews(simple_prompt)

    expected = artifact_paths_from_expected(task_json)
    written = artifact_paths_from_solution(solution_code)
    current_compared = artifacts_compared(current_eval)
    simple_compared = artifacts_compared(simple_eval)
    input_declared = input_files_from_text(task_prompt)
    input_read = input_files_from_text(solution_code)
    input_previewed = [f"inputs/{name}" if not name.startswith("inputs/") else name for name in previews]
    internal = uses_internal_helper(solution_code, task_prompt)
    hidden_data = hidden_data_flag(solution_code, input_read)
    overwrite = overwrites_result_flag(solution_code)
    fix_flags = fixture_flags(previews)
    artifact_reasons = artifact_mismatch_reasons(expected, written, current_compared, simple_compared)
    delete_like = delete_candidate(task_id, task_json.get("function_name", ""), task_prompt)
    status, reasons = classify(
        task_id=task_id,
        function_name=task_json.get("function_name", ""),
        prompt=task_prompt,
        artifact_reasons=artifact_reasons,
        fixture_reasons=fix_flags,
        internal=internal,
        hidden_data=hidden_data,
        overwrite=overwrite,
        delete_like=delete_like,
        current_eval=current_eval,
        simple_eval=simple_eval,
    )

    return {
        "task_id": task_id,
        "package": task_json.get("package") or current_eval.get("package", ""),
        "function_name": task_json.get("function_name", ""),
        "level": task_json.get("level", ""),
        "packages": task_json.get("packages", []),
        "input_factory": task_json.get("input_factory", ""),
        "contract_status": status,
        "status_reasons": reasons,
        "current_status": current_eval.get("status", ""),
        "current_tier": current_tier(current_eval),
        "current_message": current_eval.get("message", ""),
        "simple_status": simple_eval.get("status", ""),
        "simple_tier": current_tier(simple_eval),
        "simple_message": simple_eval.get("message", ""),
        "expected_artifacts_task_json": expected,
        "artifacts_written_by_solution": written,
        "artifacts_compared_by_current_eval": current_compared,
        "artifacts_compared_by_simple_eval": simple_compared,
        "input_files_declared": input_declared,
        "input_files_read_by_solution": input_read,
        "input_files_previewed_current": unique_sorted(input_previewed),
        "input_preview_excerpt_current": previews,
        "input_columns_used_by_solution": columns_from_solution(solution_code),
        "functions_called_by_solution": functions_from_code(solution_code),
        "functions_requested_by_task_prompt": functions_from_prompt(task_json),
        "uses_internal_helper": internal,
        "uses_hidden_in_script_data": hidden_data,
        "result_assignment_count": result_assignment_count(solution_code),
        "overwrites_result": overwrite,
        "fixture_semantic_flags": fix_flags,
        "task_dir": str(tdir) if tdir else "",
    }


def csv_value(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(str(x) for x in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def write_outputs(records: list[dict[str, Any]]) -> None:
    with OUT_JSONL.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow({field: csv_value(record.get(field, "")) for field in CSV_FIELDS})

    status_counts = Counter(r["contract_status"] for r in records)
    package_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        package_counts[record["package"]][record["contract_status"]] += 1

    reason_counts = Counter()
    for record in records:
        reason_counts.update(record.get("status_reasons") or [])

    lines = [
        "# Contract Manifest Summary",
        "",
        "This is a first-pass static preflight for all 254 clinical taskset results. It is generated by `build_contract_manifest.py` and should be treated as triage, not a final manual decision.",
        "",
        "## Outputs",
        "",
        "- `contract_manifest.jsonl` - full structured per-task records.",
        "- `contract_manifest.csv` - compact spreadsheet-friendly subset.",
        "- `contract_manifest_summary.md` - this summary.",
        "",
        "## Initial Contract Status Counts",
        "",
        "| status | tasks |",
        "|---|---:|",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Package by Status", "", "| package | " + " | ".join(sorted(status_counts)) + " | total |"])
    lines.append("|---|" + "|".join("---:" for _ in sorted(status_counts)) + "|---:|")
    for package in sorted(package_counts):
        total = sum(package_counts[package].values())
        cells = [str(package_counts[package].get(status, 0)) for status in sorted(status_counts)]
        lines.append(f"| `{package}` | " + " | ".join(cells) + f" | {total} |")

    lines.extend(["", "## Top Status Reasons", "", "| reason | tasks |", "|---|---:|"])
    for reason, count in reason_counts.most_common(25):
        lines.append(f"| `{reason}` | {count} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `A_KEEP_CANDIDATE`: no obvious static contract defect was detected; still needs manual spot check.",
            "- `B_REPAIR_PROMPT`: likely salvageable by a stricter `simple_contract_prompt`.",
            "- `C_REPAIR_FIXTURE`: input preview contains suspicious placeholders or fixture/task semantic mismatch signals.",
            "- `D_QUARANTINE_CONTRACT`: task metadata, reference solution, evaluator artifacts, hidden data, or result assignment behavior conflict.",
            "- `E_DELETE_CANDIDATE`: helper/assertion/document/internal-only style task that may not belong in the main benchmark.",
            "- `F_RERUN_TIMEOUT`: both current and simple runs timed out without stronger static contract flags.",
            "",
            "These labels intentionally err toward quarantine when artifact contracts disagree. The next step is manual review of each bucket, starting with `A_KEEP_CANDIDATE` and `D_QUARANTINE_CONTRACT`.",
            "",
            "Note: `contract_status` is a primary triage bucket, not the only signal. For example, many helper/assertion/document-style delete candidates are counted under `C_REPAIR_FIXTURE` or `D_QUARANTINE_CONTRACT` when they also have stronger fixture or artifact-contract defects; inspect `status_reasons` for those secondary signals.",
        ]
    )
    OUT_SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    current_eval = index_by_task(load_jsonl(CURRENT_EVAL))
    simple_eval = index_by_task(load_jsonl(SIMPLE_EVAL))
    current_gen = index_by_task(load_jsonl(CURRENT_GEN))
    simple_gen = index_by_task(load_jsonl(SIMPLE_GEN))
    task_ids = sorted(current_eval)
    missing = [task_id for task_id in task_ids if task_id not in simple_eval]
    if missing:
        raise SystemExit(f"Missing simple eval rows for {len(missing)} tasks")

    records = [
        task_record(
            task_id=task_id,
            current_eval=current_eval[task_id],
            simple_eval=simple_eval[task_id],
            current_gen=current_gen.get(task_id, {}),
            simple_gen=simple_gen.get(task_id, {}),
        )
        for task_id in task_ids
    ]
    write_outputs(records)
    print(f"Wrote {len(records)} records")
    print(OUT_JSONL)
    print(OUT_CSV)
    print(OUT_SUMMARY)


if __name__ == "__main__":
    main()
