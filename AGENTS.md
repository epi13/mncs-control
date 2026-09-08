# Agent and contributor contract

- Prefer `mncs-language` for implementation.
- State sample period, units, saturation, deadlines and model assumptions explicitly.
- Real-time paths must have bounded work/allocation behavior where promised.
- Keep plant, controller, estimator and hardware adapter boundaries distinct.
- Test deterministic replay, saturation, timing and failure cases in addition to nominal responses.
- Record language/compiler/runtime pressure in `docs/LANGUAGE_PRESSURES.md`.
- Do not infer safety from controller correctness; safety policy is a separate explicit layer.
