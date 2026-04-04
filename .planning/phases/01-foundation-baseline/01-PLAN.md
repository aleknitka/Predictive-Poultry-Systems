---
phase: 01-foundation-baseline
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: [pyproject.toml, .pre-commit-config.yaml, tests/test_env.py, main.py, tests/test_main.py]
autonomous: true
requirements: [SETUP-01, SETUP-02, SETUP-03, SIM-CORE-01]
must_haves:
  truths:
    - "Environment is reproducible via uv sync"
    - "Code quality is enforced project-wide via prek hooks (linting and formatting)"
    - "Simulation baseline executes with observable salabim trace"
  artifacts:
    - path: "pyproject.toml"
      provides: "Dependency management"
      contains: ["salabim", "greenlet", "Pillow"]
    - path: ".pre-commit-config.yaml"
      provides: "Quality gate configuration"
      contains: ["ruff-format", "ruff"]
    - path: "main.py"
      provides: "Simulation entry point"
      contains: ["salabim.Environment", "env.run"]
  key_links:
    - from: ".pre-commit-config.yaml"
      to: "ruff"
      via: "hook definition"
    - from: "main.py"
      to: "salabim"
      via: "import and environment creation"
---

<objective>
Establish a stable Python 3.13 environment with all required dependencies, quality gates, and a functional salabim simulation baseline.

Purpose: Provide a solid foundation for the Digital Twin simulation, ensuring dependencies are correct and the core loop is verifiable.
Output: Updated dependencies, active git hooks, environment tests, and a working main.py simulation.
</objective>

<execution_context>
@$HOME/.gemini/get-shit-done/workflows/execute-plan.md
@$HOME/.gemini/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/phases/01-foundation-baseline/01-RESEARCH.md
@pyproject.toml
@main.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: Setup environment and quality gates</name>
  <files>pyproject.toml, .pre-commit-config.yaml</files>
  <action>
    1. Add "Pillow>=10.0.0" to dependencies in pyproject.toml and run `uv sync` (per SETUP-03).
    2. Update `.pre-commit-config.yaml` to include ruff hooks for both linting (`id: ruff`) and formatting (`id: ruff-format`) using the `https://github.com/astral-sh/ruff-pre-commit` repository (per SETUP-02).
    3. Initialize prek hooks by running `uv run prek install`.
    4. Verify compliance by running `uv run ruff check .` and `uv run ruff format --check .`.
  </action>
  <verify>
    <automated>uv run ruff check . && uv run ruff format --check . && uv run prek run --all-files</automated>
  </verify>
  <done>All dependencies are installed and git hooks (ruff linting and formatting) are actively enforcing project standards.</done>
</task>

<task type="auto">
  <name>Task 2: Create environment verification tests</name>
  <files>tests/test_env.py</files>
  <action>
    Create a `tests/` directory if it doesn't exist.
    Create `tests/test_env.py` that verifies:
    - salabim.Environment can be instantiated.
    - pydantic.BaseModel can be used for data modeling.
    - PIL (Pillow) is available for future animation support.
  </action>
  <verify>
    <automated>uv run pytest tests/test_env.py</automated>
  </verify>
  <done>Basic environment sanity is confirmed via automated tests.</done>
</task>

<task type="auto" tdd="true">
  <name>Task 3: Implement core simulation baseline in main.py</name>
  <files>main.py, tests/test_main.py</files>
  <behavior>
    - main.py should initialize a salabim.Environment (per SIM-CORE-01).
    - A SimulationManager component should be created that runs for 100 time units.
    - The simulation should print "Fulfillment node simulation initializing..." at start and "Simulation finished" at the end.
    - The test should verify that the simulation clock reaches the specified 'till' value.
  </behavior>
  <action>
    1. Update main.py with the salabim simulation loop using the process-based modeling pattern.
    2. Create `tests/test_main.py` to verify the simulation execution.
  </action>
  <verify>
    <automated>uv run main.py | grep -E "initializing|finished" && uv run pytest tests/test_main.py</automated>
  </verify>
  <done>A functional and tested discrete event simulation baseline is established.</done>
</task>

</tasks>

<verification>
### Phase 1 Foundation Verification
- [ ] `uv run python --version` returns 3.13.x.
- [ ] `uv run python -c "import salabim; import PIL; import greenlet"` exits 0.
- [ ] `uv run ruff check .` returns 0.
- [ ] `uv run ruff format --check .` returns 0.
- [ ] `uv run prek run --all-files` returns 0.
- [ ] `uv run pytest` passes 100% (both test_env.py and test_main.py).
- [ ] `uv run main.py` prints expected simulation lifecycle logs.
</verification>

<success_criteria>
- Project dependencies (salabim, greenlet, Pillow) are correctly managed by uv.
- Code quality is enforced by prek/ruff hooks (both linting and formatting).
- Core salabim simulation loop is implemented and verified.
</success_criteria>

<output>
After completion, create `.planning/phases/01-foundation-baseline/01-SUMMARY.md`
</output>
