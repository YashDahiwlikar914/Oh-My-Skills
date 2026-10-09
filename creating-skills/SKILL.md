---
name: creating-skills
description: Use when users explicitly ask to create a new skill, edit an existing skill, optimize a skill's description, write an eval, run skill tests, or benchmark skill performance.
---

# Creating Skills

## Overview

A skill for creating new skills and iteratively improving them. 
This skill merges the interactive evaluate-and-iterate loop with best practices for skill discovery and bulletproofing.

At a high level, the process of creating a skill goes like this:
1. **Capture Intent**: Decide what the skill should do and when it should trigger.
2. **Draft the Skill**: Write the initial `SKILL.md`.
3. **Set up Evals**: Create realistic test prompts.
4. **Run Evals**: Run both the baseline (without skill/old skill) and the new skill simultaneously.
5. **Evaluate**: Draft quantitative assertions, grade the outputs, aggregate benchmarks, and launch the Eval Viewer for human review.
6. **Iterate**: Refine the skill based on the human's feedback and transcript analysis. Repeat until satisfied.
7. **Optimize Description**: Run the automated trigger-optimization loop.
8. **Package**: Present the final `.skill` file.

## 1. Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture.
- What should this skill enable the model to do?
- When should this skill trigger? (Symptoms, situations, errors)
- What is the expected output format?
- What are the test cases/success criteria?

*Communication tip*: Gauge the user's technical level. Briefly explain terms like "evaluation" or "JSON" if they might be unfamiliar.

## 2. Draft the Skill

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines)
3. **Bundled resources** - As needed in `scripts/`, `references/`, etc.

### Skill Discovery Optimization (SDO)

**Critical for discovery:** The agent reads the description to decide which skills to load.
- **Description = When to Use, NOT What the Skill Does.**
- Start with "Use when..." to focus on triggering conditions.
- Include specific symptoms, error messages, and situations.
- **NEVER summarize the skill's process or workflow in the description.** (Agents might read the summary and skip reading the actual skill!).

### Bulletproofing and Shaping

Match the form of guidance to the failure type you expect:
- **Output has wrong shape/bloated?** Provide a strict recipe or template. (Do not use negative prohibitions like "Don't narrate" as they often backfire).
- **Rule skipping under pressure?** Close loopholes explicitly. ("Write code before test? Delete it. Start over. No exceptions.")
- **Rationalizations?** Build a rationalization table addressing common excuses. Provide a "Red Flags" list of thoughts that should trigger a stop-and-restart.
- **Conditional behavior?** Use conditionals keyed to observable predicates.

Explain the *why* behind rules to leverage the model's theory of mind, rather than relying solely on rigid MUSTs.

## 3. Set up Evals

Come up with 2-3 realistic test prompts based on the interview. Show them to the user for confirmation.
Save test cases to `evals/evals.json`.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 0,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

## 4. Run Evals (The Iteration Loop)

This is a continuous sequence. Put results in `<skill-name>-workspace/` (sibling to the skill). Organize by iteration (`iteration-1/`), and within that, by eval (`eval-0/`).

### Step 4a: Spawn Runs

For each test case, spawn two subagents in the *same turn*:
- **With-skill run**: Execute the task using the new `<path-to-skill>`. Save outputs to `<workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/`.
- **Baseline run**: Same prompt. If a new skill, use *no skill* (save to `without_skill/outputs/`). If improving an existing skill, use a snapshot of the *old version* (save to `old_skill/outputs/`).

Write an `eval_metadata.json` for each test case.

### Step 4b: Draft Assertions

While runs are in progress, draft objective, quantitative assertions for each test case and explain them to the user. Add them to the `eval_metadata.json` and `evals/evals.json`.

### Step 4c: Capture Timing

When subagent tasks complete, immediately capture `total_tokens` and `duration_ms` from the notification into `timing.json` in the respective run directory.

## 5. Evaluate and Review

1. **Grade**: Spawn a grader subagent (reads `agents/grader.md`) or write scripts to evaluate assertions against outputs. Save to `grading.json`.
2. **Aggregate Benchmark**: 
   `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>`
3. **Analyst Pass**: Analyze the benchmark data for high variance, token tradeoffs, or non-discriminating assertions (see `agents/analyzer.md`).
4. **Launch Viewer**:
   ```bash
   nohup python <creating-skills-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   *(For Cowork/headless, use `--static <output_path>` instead of starting a server).*
5. Point the user to the viewer to review outputs and leave feedback.

## 6. Iterate

Read `feedback.json` generated by the viewer. (Empty feedback means it looks good).
- Read the transcripts. If the agent wastes time or writes the same helper script in every eval, refactor the skill to bundle that script.
- Keep the prompt lean.
- Generalize from feedback so the skill doesn't overfit the evals.

Kill the viewer (`kill $VIEWER_PID 2>/dev/null`), apply improvements, and rerun the loop into `iteration-<N+1>/` until the user is satisfied.

## 7. Description Optimization

After the skill works well, optimize the trigger description.
1. Generate 20 eval queries (mix of should-trigger and should-not-trigger). Make them realistic and detailed.
2. Present for review using `assets/eval_review.html`. Export to `~/Downloads/eval_set.json`.
3. Run the optimization loop:
   ```bash
   python -m scripts.run_loop \
     --eval-set <path-to-trigger-eval.json> \
     --skill-path <path-to-skill> \
     --model <model-id-powering-this-session> \
     --max-iterations 5 \
     --verbose
   ```
4. Apply the `best_description` from the result to the `SKILL.md` frontmatter.

## 8. Package and Present

If the `present_files` tool is available (or packaging is requested):
```bash
python -m scripts.package_skill <path/to/skill-folder>
```
Direct the user to the resulting `.skill` file.

---

## Runtimes & Environments

- **Claude.ai**: No subagents. Run test cases sequentially yourself. Skip baselines and quantitative benchmarks. Present outputs inline. No description optimization loop.
- **Cowork**: You have subagents. Use `--static` for the eval viewer HTML. Feedback is downloaded as `feedback.json`. `run_loop.py` works via subprocess.

## Reference Files

- `agents/grader.md`, `comparator.md`, `analyzer.md`
- `references/schemas.md`, `testing-skills-with-subagents.md`, `anthropic-best-practices.md`, `persuasion-principles.md`
- `scripts/` for run_loop, quick_validate, aggregate_benchmark
