# Architecture

## Layers

1. **Models** — state, input/output, continuous/discrete dynamics and units.
2. **Controllers** — PID, state feedback and future MPC abstractions.
3. **Estimation** — observers/filters and measurement models.
4. **Execution** — fixed-rate loops, deadlines, saturation and deterministic scheduling.
5. **Adapters** — simulated plants plus typed sensor/actuator/hardware boundaries.
6. **Verification** — stability/response cases, replay, timing evidence and bounded-execution tests.

## First milestones

1. Fixed-size state-space primitives.
2. PID plus simulation harness.
3. Deterministic fixed-rate execution.
4. Observer/estimator foundation.
5. Trajectory/MPC pressure cases and hardware-adapter experiments.
