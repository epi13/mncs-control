# RFC 0001: Control foundation

Status: Draft

## Principles

- Sample period, deadlines and timing source are explicit.
- State, measurement and actuator quantities preserve units.
- Saturation, anti-windup and failure behavior are defined rather than incidental.
- Real-time contracts include bounded allocation and execution expectations.
- Plant/controller/estimator separation enables deterministic simulation and replay.
- Hardware effects remain behind typed adapters.

## Pressure objectives

Fixed-size matrices, compile-time dimensions, generic numeric scalars, deterministic real-time scheduling, allocation control, monotonic clocks/deadlines, state-machine ergonomics, saturation arithmetic, tracing/replay, FFI/hardware adapters and isolation between async application work and real-time loops.
