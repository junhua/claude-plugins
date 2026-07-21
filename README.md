<p align="center">
  <img src="./assets/teaser.png" alt="junhua-plugins — A Claude Code Marketplace" width="100%" />
</p>

# junhua-plugins

A Claude Code marketplace hosting plugins by [@junhua](https://github.com/junhua).

## Install

```
/plugin marketplace add junhua/claude-plugins
/plugin install super-ralph@junhua-plugins
/plugin install forth-ai-harness@junhua-plugins
```

## Plugins

### super-ralph

Design-first autonomous development workflow.

- `/super-ralph:design` produces implementation-ready epics with `[STORY]` + `[BE]` + `[FE]` + `[INT]` sub-issues, full Gherkin AC (≥3 scenarios including `[SECURITY]`), Shared Contracts, and exact TDD tasks that the build phase copies verbatim.
- **`--local` mode** (v0.11.0) writes the entire epic + all stories into a single `docs/epics/<slug>.md` file and skips GitHub issue creation — useful for iterative design, spikes, and internal work.
- **`/super-ralph:improve-design "<prompt>"`** (v0.11.0) takes a single natural-language prompt, autonomously resolves the target epic (local or GitHub), interprets feedback into structured changes, applies conservative edits, and re-validates. Shipped stories are immutable.
- `/build-story`, `/e2e`, `/review-design`, `/build` auto-detect local vs GitHub from the argument shape (`docs/epics/<slug>.md#story-N` vs `#123`).
- Fire-and-forget pipelines: build → review-fix → verify → finalise → release. Domain-aware repair with hotfix flow.

- Source: [junhua/super-ralph](https://github.com/junhua/super-ralph)
- Category: development

### forth-ai-harness

A product-lifecycle harness for a solo founder plus AI engineering. The human owns product decisions and validates at product level; agents do everything else. Every feature travels one path: a one-page contract in the human's own words, a locked-test build, an independent verification with per-criterion evidence, and a gated ship.

- **Six commands, two human moments.** `/fspec` (interview → one-page contract, EARS acceptance criteria — **you approve**) → `/fbuild` (worktree, red-lock-green TDD with a hard gate that every acceptance criterion has a locked test, concurrent builds in separate terminals never corrupt each other, a bug/defect issue gets an inline fast-lane micro-spec instead of a bounce to `/fspec`, fresh-context evaluator, PR) → `/fverify` (independent verifier exercises every criterion on the real stack, mocks off — local by default or a deployed staging host via `--staging` with gated magic-OTP login — posts a product-only UAT checklist plus a technical acceptance brief for the tech lead) → `/fship` (asks both acceptances, merge, deploy verification — **you and the tech lead each accept your lens, either one handoff-able**). Plus `/fstatus` (read-only sweep naming who each item is waiting on, every concurrent build shown with its AC coverage) and `/flessons` (turns recent ships into at most five concrete process diffs, each previewed as the exact edit, applied only with your approval).
- **The law: no `n/a` escapes.** Nothing merges until the feature has been exercised on a real running stack by an agent that did not build it, with an evidence bundle a human can inspect. Environment unavailable means status `blocked`, never a silent pass. And a human is never asked to re-execute what an agent already proved — the UAT checklist is strictly product-level; a technical acceptance brief covers the engineering side instead.
- **Hook-enforced, not prose-enforced.** `test-lock.sh` blocks editing test files after the red checkpoint; `bash-gates.sh` blocks AI-authored commit trailers and blocks merging harness PRs until evidence is posted and accepted; `build-stop-gate.sh` blocks an agent from ending its turn mid-build with failing checks, session-bound so a build running in another terminal never gates this one.
- **Builder ≠ verifier.** Different agents, different context — the verifier never reads the implementation, only the contract and the running app.
- **GitHub is SSoT.** Contracts, evidence bundles, and state (`fh:contract` → `fh:approved` → `fh:building` → `fh:evidence` → `fh:accepted` → closed/shipped) live on the issue itself. A prose `LESSONS.md` in your project compounds learning across runs.
- **Domain skills included.** `agent-layer` and `memory-layer` evaluator skills load automatically for stories touching the WorkOS agent layer or DIKW memory pipeline.

First run of `/fspec` or `/fbuild` interviews you and writes per-project config to `.claude/fh.config.json` — nothing is guessed silently.

- Source: [Forth-AI/forthai-harness](https://github.com/Forth-AI/forthai-harness)
- Category: development

## About

This marketplace is a thin pointer layer. Each plugin lives in its own GitHub repository so it can be versioned, tagged, and installed independently. The `.claude-plugin/marketplace.json` file is the manifest Claude Code reads when you run `/plugin marketplace add`.

## License

MIT
