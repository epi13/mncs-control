# Control model and ownership boundary

## The disambiguation that shapes this repository

Two different meanings of "control" coexist in MNCS and must not be
merged:

1. **Control engineering** (`mncs-control`, this repo): feedback
   controllers, dynamical-system models, estimators, actuators,
   real-time loop structure, replayable behavior.
2. **Orchestration control plane** (`mncs-control-mcp`): MCP access
   to workspace tools (files, terminal, Git, projects) plus thin
   consumer boundaries to Harness/Fabric/Forge adapters.

The campaign verified firsthand: this repo's README, AGENTS.md,
ARCHITECTURE.md, and RFC 0001 unanimously charter meaning 1, while
`mncs-control-mcp`'s README documents meaning 2 (Bubblewrap sandbox,
`WorkspacePolicy`, `FileService`/`GitService`/`ProcessManager`).
A "typed capability/command surface routing subsystem operations"
was never this repository's charter, and building one here would
duplicate Forge/Actions authority. That architecture is rejected by
the evidence, not just by principle.

Consequence: `mncs-control-mcp` needs **no integration follow-up**
from this campaign. It is a thin protocol adapter over workspace
capabilities; nothing in it duplicates control-engineering math, and
nothing here routes subsystem operations. The one real action is
naming hygiene: future work should avoid using "control" for new
orchestration concepts without qualifying which meaning applies.

## Responsibility classification (verified against current owners)

- **Still legitimate Control**: fixed-size state-space/transfer
  primitives, PID + simulation harness, fixed-rate loop steps,
  saturation/anti-windup arithmetic, observer/filter foundations,
  trajectory/MPC formulations, typed sensor/actuator/sim adapters,
  control replay/verification cases, control pressure ledger.
- **Forge**: workflow, execution, admission, queues, retry,
  cancellation state, receipts. Control requests nothing of Forge
  today; if a future tuning campaign needs managed execution, the
  pattern will be Control request → Forge → ExecutionId (no private
  task tables, ever).
- **Actions**: provider/action definitions and admission. No overlap:
  a PID step is not an Action, and Control defines no providers.
- **Fabric**: bounded execution substrate. No subprocess/process-tree
  machinery in Control (none exists; none planned).
- **Commons/Store**: project relationships and persistence. Control
  persists nothing; replay evidence is derived from deterministic
  re-execution, not stored histories.
- **Doctor/Test/Debug/Harness**: generic check/harness semantics.
  Control owns only its saturation/timing/failure *cases*, run
  through the shared `mncs test` mechanism.
- **RAVEL**: plans and obligations. No planning logic in Control;
  operation identities here are stable enough to plan against if
  RAVEL ever needs to.
- **Interface layers** (MCP/CLI/TUI): thin consumers. They do not
  exist for control-engineering yet; when they do, they must not
  duplicate control math, timing, or saturation logic.
- **Obsolete scaffolding**: none found — the repo was docs-only, so
  there is no legacy control plane to remove and none was built.

## What Control owns (implemented)

- **Saturation** — `Limits` validation, total clamp, saturation-as-data.
- **Controllers** — discrete PID step with guarded dt, validated
  limits, conditional-integration anti-windup.
- **Plants** — first-order discrete dynamics with closed-form
  comparators (step response, equilibrium).
- **Execution** — one-sample closed-loop step; fixed-rate structure
  with dt-as-data; bounded work per sample; replay by determinism.
- **Results** — `PidOut`/`LoopOut` outcomes; `BadDt`/`BadLimits` for
  invalid timing/authority; instability as observable data.

## Explicitly not owned

Orchestration, dispatch, repository management, process execution,
authorization models, policy engines, event buses, project
registries, workflow composition, result-model duplication. A system
having an operation does not make it a Control operation.

## Deliberately out of scope (future layers, not claims)

Observers/filters, trajectory/MPC, second-order plants, output maps,
hardware adapters, autotuning, safety policy (always a separate
explicit layer per AGENTS.md — never inferred from correctness).

## Read vs mutate, query vs refresh, long-running work

These distinctions apply to orchestration control planes, not to
this repository: every Control operation here is a pure bounded
function over explicit inputs (a read with no side effects by
construction). There are no long-running operations, no background
tasks, no cancellation, and no query/refresh ambiguity — replay *is*
re-execution. If Control ever requests managed execution from Forge,
that handoff will carry Forge execution identities.
