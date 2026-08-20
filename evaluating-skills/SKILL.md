---
name: evaluating-skills
description: Use when measuring an agent skill's trigger activation, task-output quality, or instruction performance, comparing versions, or selecting an evidence-backed description or body revision before deployment. Use writing-skills for authoring SKILL.md and writing-for-agents for document information architecture.
---

# Evaluating Skills

Evaluate an existing skill with evidence. The evaluation target can be its task performance, trigger description, invocation reliability, or a candidate revision.

## Scope Boundary

This skill owns measurement and comparison.

- Use `writing-skills` to author or revise the `SKILL.md` body and test instruction compliance under pressure.
- Use `writing-for-agents` for pointers, information hierarchy, disclosure, and document splits.
- Use this skill to define evaluations, run baselines, compare candidates, analyze trigger and task-output failures, and select evidence-backed improvements.

Task-performance evaluation measures whether the user's requested result improves. Instruction-compliance testing belongs to `writing-skills`.

Do not treat a good final output as proof that a skill triggered correctly. Measure activation separately from task quality.

## Evaluation Contract

Every evaluation names the target skill, the user intent being tested, the expected activation state, the success criteria, and the runtime used.

- Preserve the current skill as a baseline before changing it.
- Keep positive and negative trigger cases separate.
- Include realistic small tasks, indirect wording, typos, and near-miss prompts.
- Test neighboring skills together when their descriptions can compete.
- Keep held-out prompts that the candidate revision cannot see.
- Report runtime limitations instead of presenting results from a different harness as equivalent evidence.

## Start With Evaluation

Use representative failures to decide whether a skill needs a new instruction, a narrower description, a supporting reference, or no change. Do not add guidance for a failure that has not been observed.

## Evaluation Modes

### Task Performance

Use task evaluations when the skill changes how an agent performs work.

- Run the same task without the skill and with the current skill.
- For an existing skill revision, compare the previous body with the candidate body.
- Save outputs and transcripts under an iteration workspace.
- Grade objective expectations with evidence from the outputs.
- Review subjective quality separately instead of forcing it into binary assertions.

### Trigger Accuracy

Use trigger evaluations when the question is whether the model loads a skill.

- Create 20 realistic queries for each skill under test.
- Include 8 to 10 should-trigger queries.
- Include 8 to 10 should-not-trigger near misses.
- Include indirect wording and meaningful small-task cases.
- Repeat each query at least three times when the runtime permits.
- Measure recall, precision, false-trigger rate, and repeatability.

Descriptions are pointers. They should identify what the skill covers and when it applies without copying the workflow from the body.

## Description Contract

Every new or modified skill must have an optimized description before deployment.

- Start with `Use when...` for this catalog.
- State what the skill handles and its distinct trigger branches.
- Include concrete keywords and indirect wording.
- Include the smallest meaningful task the skill still owns.
- State the boundary against its nearest competing skills.
- Describe expected co-triggering when a domain skill and output-format skill should both load.
- Keep the description under 1024 characters and target under 500 when possible.
- Test the description against positive, negative, and competing prompts.

Prefer a held-out result over a training result. A description that memorizes the eval set is not optimized.

## Trigger Evaluation Workflow

### 1. Capture the Baseline

Record the current description and body before editing. Keep the snapshot outside the skill directory.

### 2. Build The Eval Set

Save trigger queries in JSON using this shape.

```json
[
  {"query": "A realistic request that needs the skill", "should_trigger": true},
  {"query": "A realistic near miss for a neighboring skill", "should_trigger": false}
]
```

Use concrete details such as file names, paths, tools, URLs, error symptoms, or user context. Avoid abstract prompts that do not require a skill.

### 3. Run The Current Candidate

Use `scripts/run_eval.py` for Claude-compatible trigger instrumentation or `scripts/run_loop.py` for repeated description candidates.

The bundled evaluator detects Claude Code tool calls. It is not OpenCode evidence unless the OpenCode runtime is explicitly connected to the same instrumentation. For OpenCode, verify the loaded catalog with its native diagnostic command and use a runtime-native model test when credentials and telemetry are available.

### 4. Grade The Results

Use `agents/grader.md` for output assertions. Save `grading.json` with `text`, `passed`, and `evidence` fields. Use programmatic checks for objective assertions.

### 5. Aggregate The Benchmark

Run the aggregation script from this skill directory.

```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
```

Use the generated benchmark to compare pass rate, timing, token use, precision, recall, and variance. Read `agents/analyzer.md` for the analyst pass.

### 6. Review Qualitative Results

Generate the review viewer before deciding which candidate to keep.

```bash
python eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "<name>" \
  --benchmark <workspace>/iteration-N/benchmark.json
```

In a headless environment, use the viewer's static output mode. Read user feedback before another iteration.

### 7. Select The Candidate

Prefer the candidate with the best held-out result. Reject candidates that improve recall by creating broad false positives, or improve precision by missing indirect valid requests.

Return the selected description and the evidence used to select it. Send body edits to `writing-skills` and structural edits to `writing-for-agents`.

## Completion Criteria

An evaluation is complete only when the following are recorded.

- The baseline and candidate are identified.
- The positive and negative eval cases are saved.
- The runtime and instrumentation limits are stated.
- Objective assertions have evidence.
- Held-out results have been checked.
- Neighboring skill collisions have been reviewed.
- The selected change has a clear reason.

## Supporting Files

- `scripts/run_eval.py` measures trigger decisions.
- `scripts/run_loop.py` iterates description candidates.
- `scripts/aggregate_benchmark.py` aggregates benchmark results.
- `agents/grader.md` defines output grading.
- `agents/analyzer.md` defines benchmark analysis.
- `references/schemas.md` defines result formats.
- `eval-viewer/generate_review.py` creates the qualitative review interface.
