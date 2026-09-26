# MNCS language pressure ledger

Record workload, observed behavior, required semantic, reproducer, owner, workaround and closure verification.

## Initial pressure targets

- fixed-size matrix/vector types with static shape checking
- compile-time state/input/output dimensions
- unit-aware control signals
- no-allocation/bounded real-time regions
- monotonic clocks, periods and deadlines
- deterministic scheduling and replay
- safe isolation between async and real-time execution
- saturation/checked arithmetic primitives
- hardware/FFI ownership and error boundaries
- efficient state-machine/pattern-match syntax
- low-overhead tracing and timing evidence
- diagnostics for dimension/unit/timing mismatches

## Campaign findings (2026-09-26, PID + first-order loop foundation)

- **C-001 (non-blocking, language): `next` is reserved and match
  patterns bind declared field names.** A payload field named `next`
  (natural for step outcomes) cannot be constructed or matched: the
  binding position fails to parse (MNP064), and renaming only the
  use-site fails elaboration (MNE177/MNE179/MNE140 — patterns must
  bind every declared payload field by its declared name). Workaround:
  fields named `state` (`PidOut.Value`) and `after`
  (`LoopOut.Value`). Minimal reproducer: an enum variant
  `Value { next: T }` matched as `Value { next }`. Owner: language
  (reserved-word set / diagnostic guidance).
- **C-002 (non-blocking, runtime/architecture): no clock observation
  in MNCS.** Fixed-rate execution is expressed as a semantic step
  contract with `dt` as validated data; monotonic clocks, deadline
  enforcement, and jitter measurement stay behind host adapters.
  This blocks measured real-time claims, not deterministic control.
  Owner: runtime/host-adapter boundary (typed FFI), not Control.
- **C-003 (non-blocking, language): controllers are f64-specific.**
  Generic-scalar PID needs generic numeric arithmetic — the same root
  cause as geometry pressure G-001. Cross-referenced, not duplicated;
  no new reproducer (the `fclamp` totality boundary already covers
  the saturation side).
- **C-004 (non-blocking, test): trap-adjacent arms need total
  stand-ins.** Impossible match arms use `u != u`-style total
  expressions (finite values only, by the float trap rule) rather
  than traps. Convention adopted from the math/geometry campaigns.

Deferred (decided, not pressure): generic quadrature-equivalent
(discretization-method choice for higher-order holds — ZOH vs
Tustin — deferred with the second-order plant); unit/dimension
typing (per-function documentation suffices at this scale);
observer/MPC/safety layers (future milestones, recorded as UNKNOWNs
in evidence, not pressures).
