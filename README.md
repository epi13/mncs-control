# mncs-control

<!-- MNCS:generated:begin -->
<!-- MNCS:generated:end -->

Machine-native control and dynamical-systems infrastructure for MNCS.

`mncs-control` is the canonical home of **feedback-control
engineering**: discrete controllers, plant models, saturation
semantics, fixed-rate loop execution, and replayable verification —
written in `mncs-language` (Profile 0.18). It is also a deliberate
language pressure project for fixed-size algebra, deterministic
real-time structure, saturation arithmetic, and replay.

## What "Control" means here (read first)

"Control" in this repository means **control of dynamical systems**
(state-space models, PID, observers, trajectories, MPC foundations),
not orchestration of MNCS subsystems. There is exactly one canonical
`mncs-control`; no `control-v2`/`native-control` forks exist.

The similarly named `mncs-control-mcp` is a different thing: a
workspace orchestration *control plane* (filesystem, terminal, Git,
project tools over MCP). It does not consume control-engineering
primitives, and this repository does not route subsystem operations.
See `docs/CONTROL_MODEL.md` for the full disambiguation and the
Forge/Actions/Fabric/RAVEL/Test/Doctor/Commons/Store boundary table.

## Ownership boundary

| Concern | Owner | Control relationship |
|---|---|---|
| Scalar arithmetic, clamp, `approx` | `mncs-numerics` | Consumed; never duplicated |
| Generic matrices, exact solvers | `mncs-math` | Not a dependency of this slice |
| Workflow/execution/admission | Forge | Control never schedules or queues |
| Provider/action model | Actions | Not duplicated |
| Bounded execution substrate | Fabric | No private subprocess machinery |
| Plans/obligations/evidence | RAVEL | No planning logic in Control |
| Test/Doctor/Debug semantics | Their repos | No duplicate result models |
| Persistence | Store | Control persists nothing |
| Workspace orchestration plane | `mncs-control-mcp` | Separate; thin, untouched |
| Controllers, plants, saturation, loop steps, replay checks | **`mncs-control`** | Canonical home |

## Current capability (foundation slice)

- `src/control/saturate.mncs` — validated `Limits`, total clamp,
  explicit saturation reporting.
- `src/control/pid.mncs` — discrete positional PID, dt-guarded
  derivative, conditional-integration anti-windup, `BadDt`/`BadLimits`.
- `src/control/plant.mncs` — first-order discrete plant plus
  closed-form step/equilibrium comparators.
- `src/control/loop.mncs` — one-sample closed loop
  (`LoopState`/`LoopOut`), full-state measurement, replay by
  determinism.

## Verification

18 native `mncs test` declarations across 4 suites
(`scripts/run_tests.py`), exact `==` on dyadic trajectories, plus the
independent exact-rational oracle `tools/oracle_pid.py`. See
`docs/VERIFICATION.md` and `evidence/control-capabilities.json`.

Timing note: `dt` is carried data; wall-clock deadline enforcement
stays behind host adapters (pressure C-002). The real-time contract
proved here is bounded deterministic per-sample work plus replay.

## Adding a controller/plant

1. Create `src/control/<name>.mncs` (`module mncs.control.<name>.v1`;
   file path must mirror module segments).
2. Validate timing/limits into data outcomes (never trap on bad models).
3. Keep plant/controller/estimator/adapter boundaries distinct.
4. Add a native suite under `tests/native/` + runner entry, with
   known-answer, saturation, replay, and failure cases plus an oracle
   cross-check. Do not infer safety from correctness.

## Layout

- `src/control/` — the library (`.mncs` only, no host semantics)
- `tests/native/` — in-language contracts via `mncs test`
- `scripts/run_tests.py` — canonical runner with revision-bound JSON evidence
- `tools/oracle_pid.py` — independent exact-arithmetic oracle
- `docs/ARCHITECTURE.md` — layers and milestones (standing plan)
- `docs/CONTROL_MODEL.md` — ownership, disambiguation, subsystem boundaries
- `docs/VERIFICATION.md` — trajectory/property evidence
- `docs/LANGUAGE_PRESSURES.md` — pressure ledger with reproducers
- `docs/rfcs/0001-foundation.md` — foundation principles
- `evidence/control-capabilities.json` — machine-readable capability record
