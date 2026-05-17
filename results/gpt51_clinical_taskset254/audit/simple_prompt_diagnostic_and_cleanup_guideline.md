# Simple Prompt Diagnostic and Clinical Task Cleanup Guideline

This file preserves the working guideline for interpreting the simple-prompt run and planning the cleanup of the 254 clinical tasks.

---

可以。我们只看 **simple prompt 版本** 的话，我目前的理解是：

simple 版本并不是“更差的 baseline”，它其实很有诊断价值。它把问题从“复杂结构化 prompt 是否误导模型”转移到了一个更基础的问题：

> 如果只给模型一个简短、自然、接近人工指令的任务描述，再加 input preview 和 required output，模型到底会怎么理解这个 benchmark contract？

目前看下来，simple 版本说明了三件事。

---

## 1. simple prompt 能减少一部分“格式性负担”，但不能自动恢复 hidden reference contract

clinical taskset254 里，simple prompt 的 strict pass@1 是：

```text
1 / 254 = 0.0039
```

唯一通过的是 `pharmaverse/admiral/filter_exist`。current prompt 是 0/254，simple prompt 是 1/254，所以从 strict pass@1 看，提升几乎没有。

但 simple prompt 的状态分布发生了变化：

| prompt variant          | PASS | FAIL | NO_OUTPUT | TIMEOUT | EXEC_FAIL |
| ----------------------- | ---: | ---: | --------: | ------: | --------: |
| current prompt + inputs |    0 |   83 |        81 |      88 |         2 |
| simple prompt + inputs  |    1 |  113 |        52 |      88 |         0 |

也就是说，simple prompt 把一部分 `NO_OUTPUT` 推到了 `FAIL/output_bad`，说明它更容易让模型写出某种输出文件，但这些输出通常还是不符合 reference。

所以 simple 的真实作用不是“让模型更会做题”，而是：

```text
更容易产出代码和 artifact
但不一定产出 benchmark 想要的 artifact
```

这对诊断很重要，因为它说明很多失败不是单纯 prompt 太复杂导致的。

---

## 2. simple prompt 暴露了：很多 clinical task 的“自然语义”和“reference 语义”不一致

simple prompt 通常长这样：

```text
Create R script to perform xxx using the xxx clinical task contract.
Input: ...
Output: result.csv
Read files from inputs/ and write the required files under outputs/.
```

这类 prompt 很像人会给模型的最小任务说明。它的问题是：如果 task 本身的 reference 行为很特殊，simple prompt 不可能让模型猜出来。

比如 `tidytlg/check_file`。

simple prompt 只说做 `check file`，输入 `arg.tsv`，输出 `result.csv`。但 reference solution 实际上不是输出 TRUE/FALSE，而是最后 `result <- arg`，也就是输出输入值本身。

这种情况下，simple prompt 失败不是因为模型差，而是因为：

```text
自然任务语义：检查文件是否存在
reference 实际语义：输出输入 arg 本身
```

这说明 simple prompt 对 benchmark 是一个很好的“诚实测试”：

> 如果 simple prompt 下模型做了自然合理的事却失败，说明 task 的 reference contract 可能不是自然语义 contract。

---

## 3. simple prompt 更容易暴露模型的“领域语义误解”

simple prompt 的另一个价值是，它减少了结构化 prompt 的强约束，所以更容易看出模型自己怎么理解函数名。

例如 `sdtm.oak/str_to_anycase`。

current prompt 明确解释了 `str_to_anycase()` 是生成 case-insensitive regex，所以 current generated code 至少方向接近，只是输出路径错了。可是 simple prompt 下，模型把 “anycase” 理解成了 PascalCase / snake_case 这种命名风格转换，结果语义完全错了。

这类 case 才比较接近真正的 model semantic error：

```text
prompt/input/reference 基本可理解
但模型对函数名或任务语义理解错
```

所以 simple prompt 有一个优点：它能把模型的默认理解暴露出来。缺点是：如果任务需要 package-specific 语义，simple prompt 很可能不够。

---

## 4. simple prompt 对 artifact path 有一定帮助，但仍然不稳定

有些 simple prompt 会明确写：

```text
Output: result.csv
```

这比 current prompt 里“save as appropriate file format”更接近 grader contract。

但是它仍然不够。因为很多 task 实际还需要 `summary.csv`，或者 reference 输出的 schema 很特殊。比如 `replace_na_with_blank` 的 expected artifacts 是 `outputs/result.csv, outputs/summary.csv`，但 reference prompt 里又只显式写了 `outputs/result.csv`，evaluation 里却检查 `summary.csv`。simple 版本没有稳定解决这个问题。

所以 simple prompt 暴露了一个更底层的问题：

> artifact contract 不能只靠自然语言“Output: result.csv”来表达，必须从 task metadata / evaluator / reference output 自动生成严格、完整的输出要求。

---

## 5. simple prompt 在 bio controls 上表现更能说明问题

bio/omics controls 里，clean tasks 可以稳定 PASS。例如：

`S102_log_transform_proteomics`：prompt 明确要求读 `inputs/counts.tsv`，做 `log2(x+1)`，写 `outputs/log_proteomics.tsv`，5/5 PASS。

`S103_normalize_proteomics`：prompt 明确要求用 `limma::normalizeBetweenArrays(method='quantile')`，写 `outputs/normalized_proteomics.tsv`，5/5 PASS。

这和 clinical simple prompt 形成很强对比：

```text
bio simple/direct contract clean → GPT-5.1 可以 pass
clinical simple/direct contract 不足 → 因为 hidden reference / fixture / artifact 不一致仍然 fail
```

所以 simple 版本最大的价值是：它证明不是“simple prompt 一定不行”，而是 clinical taskset 的 simple prompt 无法恢复那些隐藏合同。

---

## 6. 目前我对 simple 版本的总体判断

我会这样总结：

> simple prompt is a diagnostic baseline, not a strong prompting strategy.

它的意义不在于提高 pass@1，而在于提供一个接近自然任务描述的 baseline，帮助我们判断失败到底来自哪里。

目前 simple 版本揭示了：

1. **如果 task contract 干净，simple/direct prompt 可以工作**。bio controls 证明了这一点。
2. **如果 reference 行为隐藏在 solution.R 里，simple prompt 无法猜出来**。clinical 的很多失败属于这一类。
3. **如果 fixture 语义错位，simple prompt 会被输入诱导到错误任务**。比如 `count_vals`。
4. **如果函数名有领域特定含义，simple prompt 可能暴露模型的语义误解**。比如 simple `str_to_anycase`。
5. **simple prompt 可以增加 artifact 产出，但不能保证 exact schema / exact file contract**。

所以我现在不会把 simple 版本解释成“弱 prompt baseline”。我会把它解释成：

```text
A natural-language contract probe:
它测试的是，在不注入复杂结构化约束的情况下，
模型能否仅凭 task name、input files、output name 和 input preview
恢复 benchmark 期望的 executable behavior。
```

而 clinical taskset254 的结果说明：**很多 clinical tasks 的 executable behavior 并不能从 simple prompt 中恢复出来。**

这正好支持我们后面的主张：

> final evaluation 不能只比较 current prompt vs simple prompt 的 strict pass@1，而应该先做 task-contract preflight，确认哪些任务的 executable behavior 可以从 prompt/input/artifact contract 中被公平推断出来。

可以。我给你一个 **面向 254 条 clinical tasks 的完整清洗规划**。但先说清楚边界：目前我们有完整 strict result、50 条 rich audit sample、bio controls 对照；还没有对 254 条逐条跑完 contract preflight。因此我现在能给的是 **工程上可执行的全量处理方案 + 当前可确定的改/删规则 + 50 条样本中的明确例子**，不能诚实地把 254 条逐条列成“删/改/保留”最终名单。

我的总体建议是：**不要直接删很多 task。先把 254 条分成四个发布层级。**

---

# 总体目标

这 254 条 clinical tasks 不能再作为一个同质 benchmark 直接发布。它们现在混合了至少五种东西：

```text
1. 真正可测的 clinical coding tasks
2. prompt 生成错误的 tasks
3. reference / evaluator / expected artifact 不一致的 tasks
4. fixture 语义错误或疑似复制错位的 tasks
5. 不适合作为 code generation benchmark 的 wrapper/no-op/internal-helper tasks
```

所以目标不是“修到所有都能 pass”，而是建立一个 **task validity pipeline**：

```text
254 raw tasks
↓
contract preflight
↓
分类：keep / repair / quarantine / delete
↓
生成 corrected simple prompt
↓
小样本 rerun
↓
发布 contract-valid subset + defect appendix
```

---

# 第一层：直接保留 Keep

## 判定标准

一个 task 可以直接保留，如果满足：

```text
1. task.json instruct_prompt、solution.R、expected artifacts、evaluator 对齐
2. input fixtures 的列名和值符合函数语义
3. reference solution 没有隐藏 overwrite / no-op / fallback 行为
4. prompt 中可以自然推断出应该调用什么 API 或做什么变换
5. output path 和 schema 明确
```

这类任务即使模型失败，也可以作为公平模型错误。

## 当前样本中的例子

50 条 clinical audit 里这种很少。`replace_na_with_blank`、`squote`、`str_to_anycase`、`extract_unit`、`ggsurvfit/scale_ggsurvfit` 被 audit 归为 `llm_wrong`，说明它们相对更接近“合同 coherent，但模型错”。在 rich case index 中，明确归为 `llm_wrong` 的有 5/50。

但注意，其中有些仍然需要轻微修 prompt，例如强制输出 `outputs/result.csv`，否则会被 artifact path drift 污染。比如 `squote` 里 current generated code 调用了 `squote(x)`，但写成 `outputs/x_quoted.csv`，strict fail 是因为没有生成 `outputs/result.csv`。

所以这类不是“完全不用改”，而是：

```text
Keep, with prompt/output contract tightening.
```

---

# 第二层：修 prompt 后保留 Repair-Prompt

这是最大的类别。

## 判定标准

如果 `solution.R` 本身能表达一个确定任务，input 也能支持，但 current/simple prompt 没有保留 reference contract，就应该修 prompt，不删 task。

典型问题：

```text
1. prompt 把 reference-specific behavior 改写成 public API
2. prompt 没写 internal helper / namespace access
3. prompt 说 “save as appropriate”，但 grader 要固定 result.csv / summary.csv
4. prompt 没写 reference 里的 fallback / scalar extraction / wrapper behavior
5. prompt 太泛，导致模型按函数名猜任务
```

## 当前样本中的例子

`aNCA/get_conversion_factor` 应该属于 repair-prompt，而不是删。reference 明确要求用 `units::set_units` 计算 numeric conversion factor，并且不要依赖 exported `aNCA::get_conversion_factor`；但 current prompt 反而要求调用 public `aNCA::get_conversion_factor`。

修法不是让模型“更聪明”，而是把 prompt 改回 executable contract：

```text
Read initial_unit.tsv and target_unit.tsv.
Extract unit strings.
Use units::set_units(1, initial_unit, mode="standard") then convert to target_unit.
Return numeric conversion factor.
If conversion fails, return NA unless units are identical, then return 1.
Write outputs/result.csv and outputs/summary.csv exactly.
```

再比如 `aNCA/g_pkcg01_log`、`g_pkcg02_lin`、`g_pkcg03_log`、`calculate_f`、`add_qmd_plot`、`get_imputation_target_date` 等，audit summary 里明确说很多 aNCA/admiral 任务 reference 需要 internal helper 或 reference-specific workaround，但 generated prompt 却要求 public routine 或 generic transformation。

这类应该大规模进入：

```text
Repair-Prompt queue
```

而不是删除。

---

# 第三层：修 fixture 后再判断 Repair-Fixture

## 判定标准

如果任务描述和 reference 可以成立，但 input fixture 的列名、值、对象类型明显来自另一个任务，或者不符合目标函数语义，就不能直接评分模型。

典型信号：

```text
1. scalar value fixture 里出现 exprs(...)
2. unit fixture 里出现 AVAL / AVISITN / USUBJID
3. gpar object 任务里出现 clinical placeholder
4. log object 任务里出现普通 TSV placeholder
5. 参数名像 by_vars / set_values_to，但 task 是 count scalar
```

## 当前样本中的例子

`admiral/count_vals` 是典型。reference prompt 要求 `var.tsv` 是 vector，`val.tsv` 是 scalar value，调用 `admiral::count_vals(var, val)`。但 actual input preview 是：

```text
val.tsv: set_values_to / exprs(AVAL = mean(...))
var.tsv: by_vars / USUBJID / AVISIT
```

这更像 summary derivation task 的参数，而不是 count_vals 的输入。模型被诱导去解析表达式、构造 ADaM dataset、寻找 analysis dataset，这是被错误 fixture 带偏。

这类不应直接删，因为有些函数本身可以测。但必须重建 fixtures。

50 条 audit 中明确归为 `data_or_fixture_issue` 的有 6 条，包括：

```text
admiral/count_vals
admiral/derive_param_rr
gridify/gpar_args
logrx/parse_log
admiraldev/assert_unit
tidytlg/add_indent
```

rich case index 里这些都被标成 `data_or_fixture_issue`。

处理策略：

```text
Repair-Fixture first.
修完 fixture 后重新跑 reference solution。
如果 reference output 合理，再保留。
如果 reference solution 本身也不合理，再转入 quarantine/delete。
```

---

# 第四层：reference/evaluator 合同冲突，先隔离 Quarantine-Contract

## 判定标准

如果 task.json、prompt、solution.R、expected artifacts、evaluator 之间互相不一致，就不要马上修 prompt，也不要直接删。应该先隔离，逐条判定到底保留哪个合同。

典型问题：

```text
1. prompt 说输出 TRUE/FALSE，reference 输出输入本身
2. task metadata 说一个 artifact，solution.R 写另一个 artifact
3. evaluator 比较的文件不在 expected.artifacts
4. solution.R 中途计算一个结果，最后又 result <- input 覆盖
5. reference 构造 in-script hidden dataset，不使用 prompt 暴露的 input
```

## 当前样本中的例子

`tidytlg/check_file` 是最典型的 quarantine，而不是 repair-prompt。current prompt 说用 `check_file` 返回 TRUE/FALSE，但 reference solution 里最后 `result <- arg`，实际输出输入值。

这类 task 的问题不是 prompt 少写几句话，而是你必须先决定：

```text
A. 我们到底想测 tidytlg::check_file 的真实语义？
B. 还是想测当前 solution.R 的 wrapper 行为？
```

如果选 A，就要重写 reference solution 和 expected output。
如果选 B，就要把 prompt 写成“输出输入 arg 本身”，但这会变成一个很奇怪的 benchmark task。

所以我的建议是：

```text
check_file / check_req_arg 这类 helper-check task 应优先删除或移入 appendix，不进主 benchmark。
```

50 条 audit 中 `prompt_reference_mismatch` 有 11 条；rich case index 里包括 `check_file`、`check_req_arg`、`derive_vars_joined`、`dose_profile_duplicates`、`get_imputation_targets`、`assert_same_type`、`dthcaus_source` 等。

这类不能急着修。要先 quarantine。

---

# 第五层：建议删除 Delete / Exclude from Main Benchmark

不是所有 task 都值得救。我的删除标准比较严格：只有当它不适合作为公平 code generation benchmark 时才删。

## 删除标准

建议删除或至少移出 main benchmark 的 task 类型：

```text
1. reference 行为是 no-op / echo input / wrapper artifact，不测真实函数能力
2. 任务核心依赖 internal helper，但 prompt 又无法合理公开描述
3. 需要复杂外部对象、环境状态、交互式文档/plot/ppt/qmd 生成，难以稳定比较
4. evaluator 检查的是 reference side effect，而不是有明确语义的结果
5. fixture 无法自然构造，修复成本高于任务价值
6. task 本质是 assertion/check helper，输出只是错误/TRUE/FALSE/输入回显，信息量低
```

## 当前样本里我会优先考虑删除/移出主集的类型

### A. helper check / assertion 类

例如：

```text
tidytlg/check_file
tidytlg/check_req_arg
admiraldev/assert_same_type
admiraldev/assert_expr
admiraldev/assert_unit
admiral/assert_valid_queries
```

不是说这些函数没用，而是它们作为 benchmark task 很容易变成“猜 wrapper 行为”。例如 `check_file` reference 最后输出 arg，而不是自然的 check result。

建议：

```text
主 benchmark 删除或降级为 diagnostic appendix。
```

### B. 文档/幻灯片/QMD/PPTX 生成类

例如：

```text
aNCA/create_html_dose_slides
aNCA/create_pptx_doc
aNCA/create_qmd_doc
```

这些任务很容易受环境、side effect、文件格式、stub 层影响；如果最终只比较一个 summary CSV，又会偏离真实任务。rich case index 中这些多数是 `prompt_wrong` 或 output_bad。

建议：

```text
如果没有专门的 document artifact evaluator，就不要放 main pass@1。
```

### C. internal plotting/helper 类

例如：

```text
aNCA/g_pkcg01_log
aNCA/g_pkcg02_lin
aNCA/g_pkcg03_log
aNCA/add_qmd_plot
aNCA/add_qmd_sl_plot
aNCA/add_qmd_sl_plottabletable
```

这些未必全部删除，但需要判断 reference 是否依赖 non-exported internal helper。如果依赖 internal helper 且 prompt 不能自然说明，建议不进 main benchmark。audit summary 明确指出许多 aNCA tasks 需要 internal helpers 或 reference-specific behavior，但 prompt 要求 generic/public API。

建议：

```text
优先 quarantine。
能改成明确 exported workflow 的保留；
只能靠 internal hidden helper 的移出主集。
```

---

# 对 254 条的推荐处理比例

根据 50 条 audit 样本估计，问题很严重：prompt/contract/data 问题占 44/50，明确 LLM implementation error 只有 5/50。

不能机械外推，但可以作为规划估计：

| 类别                             |   预计比例 | 对 254 条的粗略规模 | 处理                                           |
| ------------------------------ | -----: | -----------: | -------------------------------------------- |
| Keep / minor prompt tightening | 10–20% |        25–50 | 保留，补严格 output contract                       |
| Repair-Prompt                  | 35–50% |       90–125 | 从 reference/instruct_prompt 重写 simple prompt |
| Repair-Fixture                 | 10–20% |        25–50 | 重建 input fixtures，再 rerun                    |
| Quarantine-Contract            | 15–25% |        40–65 | 人工决定保留哪个合同                                   |
| Delete / appendix only         | 10–20% |        25–50 | 从主 benchmark 移除                              |

我倾向于保守一点：**第一版 contract-valid clinical subset 不要追求 254 全保留**。先做一个 120–170 条左右的干净 subset，更适合发表和复现实验。剩下的作为 “excluded/quarantined task appendix” 透明列出。

---

# 具体执行流程

## Step 1：为 254 条生成 contract manifest

每条 task 生成一个 JSON：

```json
{
  "task_id": "...",
  "package": "...",
  "function": "...",
  "expected_artifacts_task_json": [],
  "artifacts_written_by_solution": [],
  "artifacts_compared_by_evaluator": [],
  "input_files_declared": [],
  "input_files_read_by_solution": [],
  "input_columns_used_by_solution": [],
  "functions_called_by_solution": [],
  "functions_requested_by_prompt": [],
  "uses_internal_helper": true,
  "uses_hidden_in_script_data": false,
  "overwrites_result": true,
  "fixture_semantic_flags": [],
  "contract_status": "..."
}
```

这个是关键基础设施。

---

## Step 2：自动分类

自动分为：

```text
A_KEEP
B_REPAIR_PROMPT
C_REPAIR_FIXTURE
D_QUARANTINE_CONTRACT
E_DELETE_CANDIDATE
F_RERUN_TIMEOUT
```

判定规则可以这样写：

### A_KEEP

```text
artifact 一致
input 一致
solution 函数和 prompt 函数一致
无 hidden overwrite
fixture 无异常 placeholder
```

### B_REPAIR_PROMPT

```text
solution 可执行且合理
fixture 基本合理
但 prompt 没有保留 internal helper / output path / fallback / exact schema
```

### C_REPAIR_FIXTURE

```text
fixture columns 或 values 与 function contract 明显不符
但 reference task 本身可以成立
```

### D_QUARANTINE_CONTRACT

```text
task.json / solution.R / evaluator / prompt 互相冲突
需要人工决定哪个合同是 canonical
```

### E_DELETE_CANDIDATE

```text
no-op/echo/assertion/helper/doc-generation/internal-only
或修复后仍然不构成有意义 code-generation task
```

### F_RERUN_TIMEOUT

```text
timeout 但无足够 stderr/code trace
需要加 diagnostics rerun
```

---

## Step 3：对不同类别采取不同动作

| 类别                    | 动作                                                                              |
| --------------------- | ------------------------------------------------------------------------------- |
| A_KEEP                | 保留，重新生成 corrected simple prompt                                                 |
| B_REPAIR_PROMPT       | 从 `task.json instruct_prompt + solution.R behavior + exact artifacts` 生成 prompt |
| C_REPAIR_FIXTURE      | 重建 fixtures，重新生成 reference outputs                                              |
| D_QUARANTINE_CONTRACT | 人工审查，决定 rewrite reference / rewrite prompt / delete                             |
| E_DELETE_CANDIDATE    | 移出 main benchmark，保留到 excluded_tasks.md                                         |
| F_RERUN_TIMEOUT       | 加日志 rerun，再归类                                                                   |

---

# corrected simple prompt 应该长什么样

simple 版本不要再只是：

```text
Create R script to perform xxx.
Input: ...
Output: result.csv.
```

应该是 **contract-simple prompt**，短，但不能丢合同：

```text
Write an R script for the task below.

Inputs:
- inputs/x.tsv: TSV with header. Use read.delim(..., check.names=FALSE, stringsAsFactors=FALSE).

Computation:
- Extract column x as a character vector.
- Apply admiraldev::squote(x).

Required outputs:
- outputs/result.csv exactly.
- The CSV must contain columns: x, result.
- Use write.csv(..., row.names=FALSE).
- Create outputs/ if needed.

Do not write alternative filenames.
Do not require any input files other than those listed above.
```

这个比 current prompt 简单，但比旧 simple prompt 更严格。

我建议叫：

```text
simple_contract_prompt
```

不要叫 structured prompt。它是“短 prompt + 不可丢失的 executable contract”。

---

# 对删改策略的最终建议

如果要我给一个明确决策，我会这样定：

## 主 benchmark 只放三类

```text
1. clean exported API tasks
2. clean data transformation tasks
3. clean package workflow tasks with deterministic tabular/RDS outputs
```

## 暂不放主 benchmark

```text
1. assertion/helper/check tasks
2. internal helper tasks
3. document/PPT/QMD generation tasks
4. hidden wrapper/no-op tasks
5. fixture 明显不合法的 tasks
```

## 可以保留但必须重写 prompt/fixture 的

```text
1. aNCA numeric/scalar/table transformation tasks
2. admiral date/unit/string derivation tasks
3. sdtm.oak/metatools/logrx 简单 deterministic transformation tasks
4. tidytlg 简单 table transformation tasks
```

---

# 最终发布形态

我建议最终不要发布一个单表 “254 tasks”。而是：

```text
Clinical-main-clean: contract-valid tasks
Clinical-repaired: 修复 prompt/fixture 后可用 tasks
Clinical-quarantine: 有合同冲突，暂不计入主分数
Clinical-excluded: 删除/移出主 benchmark 的任务及理由
Bio-controls: proteomics 对照组
```

最终报告主表：

| split                   |                 tasks | strict pass@1 | normalized artifact pass@1 | notes                |
| ----------------------- | --------------------: | ------------: | -------------------------: | -------------------- |
| clinical raw 254        |                   254 |        frozen |                   optional | only reproducibility |
| clinical contract-valid |                     N |   main metric |                  secondary | fair denominator     |
| clinical repaired       |                     N |  rerun metric |                  secondary | after repair         |
| bio controls            | 14 tasks / 70 samples |      contrast |                          — | sanity check         |

这样最稳。

---

# 一句话结论

这 254 条不要简单问“哪些删、哪些改”。正确做法是：

> 先用 contract preflight 把 254 条拆成 keep / repair prompt / repair fixture / quarantine / delete 五类；主 benchmark 只保留 contract-valid subset；assertion、hidden wrapper、internal helper、document-generation、fixture 错位严重的任务应移出主集或删除；其余大部分通过 corrected simple contract prompt 和 fixture 修复来救。

目前 50 条 audit 已经足够证明：**大多数任务不是该删，而是不能在当前 contract 状态下评分模型。**
