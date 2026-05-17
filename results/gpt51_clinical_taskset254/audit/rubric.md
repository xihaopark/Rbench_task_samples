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
