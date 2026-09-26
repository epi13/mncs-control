# Scientific verification

Pinned by 18 native `mncs test` declarations (4/4 suites PASS via
`scripts/run_tests.py`) and cross-checked by `tools/oracle_pid.py`
(exact `Fraction` arithmetic plus IEEE-754 bit checks, zero shared
code). Dyadic trajectories assert exact `==`; no `approx` was needed
in this slice.

## Closed-loop trajectories (plant a=0.5, b=0.5, dt=1, r=4)

P-only (Kp=1): u = [4, 2], y = [0 → 2 → 2] — settles at exactly half
the setpoint. The droop is the correct P-only expectation, asserted
as `y == 2.0`, not as a failure.

PI (Kp=1, Ki=0.5): u = [6, 3.5, 3.625, 3.71875],
y = [3, 3.25, 3.4375, 3.578125] — climbing toward r=4, integral
eliminating droop. Oracle confirms each lane bit-for-bit.

## Element properties

- Saturation: clamp values exact at/inside/outside limits;
  inverted (`lo > hi`) and degenerate (`lo == hi`) limits rejected.
- PID: P action, I accumulation, D kick (`Kd=2`, error step 4→2 gives
  exactly −4), integrator freeze under saturating error, integrator
  release when error opposes saturation (trial accepted while output
  still clamps).
- Plant: iterated steps equal the closed-form `step_once`/`step_twice`
  comparators; DC equilibrium `b·u/(1−a)` holds its value;
  unforced a=0.5 decay halves per sample; unstable a=2 growth is
  observed data (1→2→4→8), never a trap.
- Loop: guard propagation (`BadDt`/`BadLimits` survive routing
  through `loop_step`); saturated aggressive loop (Kp=8, ±1
  authority) stays bounded with every sample flagged.

## Replay

Two identical 4-sample runs (P+I+D gains, nonzero initial state)
agree bit-for-bit on plant state, integral, and previous error:
deterministic replay without stored histories.

## Degenerate / invalid models (all structured)

Zero/negative dt → `BadDt`; inverted/degenerate limits →
`BadLimits` (propagated through PID and loop layers); instability is
observable trajectory data. No NaN, no bare "control failed".

## Timing discipline

`dt` is validated data (`dt > 0`), never a clock read. Per-sample
work is bounded (fixed arithmetic, no allocation). Wall-clock
deadline enforcement is explicitly out of the native contract
(pressure C-002); the real-time claim proved here is determinism +
boundedness + replay, not measured jitter.

## What is NOT claimed

No observer/filter verification, no MPC, no second-order or
constrained control, no measured real-time performance, no
hardware-in-the-loop evidence, no stability proofs beyond the
pinned trajectories. The evidence record states exactly this.
