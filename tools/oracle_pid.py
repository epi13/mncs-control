#!/usr/bin/env python3
"""Independent oracle for the mncs-control foundation slice.

Recomputes every committed expectation with exact rational arithmetic
(Fraction) plus IEEE-754 bit cross-checks, independent of the MNCS
implementation. Fails loudly on any mismatch.

Usage:
    python3 tools/oracle_pid.py
"""

from fractions import Fraction as Q
import struct

FAILURES = []


def check(name, got, want):
    ok = got == want
    print("%-42s got=%s want=%s %s" % (name, got, want, "OK" if ok else "MISMATCH"))
    if not ok:
        FAILURES.append(name)


def bits(x):
    return struct.pack("<d", x)


def pid_run(kp, ki, kd, r, y0, dt, lo, hi, steps):
    integ, prev, y = Q(0), Q(0), Q(y0)
    ys, us, sats, integs = [], [], [], []
    for _ in range(steps):
        err = Q(r) - y
        raw = Q(kp) * err + Q(ki) * (integ + err * Q(dt)) + Q(kd) * (err - prev) / Q(dt)
        u = min(max(raw, Q(lo)), Q(hi))
        sat = u != raw
        if not (sat and err * raw > 0):
            integ = integ + err * Q(dt)
        prev = err
        ys.append(y)
        us.append(u)
        sats.append(sat)
        integs.append(integ)
    return ys, us, sats, integs


def main():
    # --- P-only droop: Kp=1, plant a=b=1/2, r=4 ---------------------------
    ys, us, sats, _ = pid_run(1, 0, 0, 4, 0, 1, -100, 100, 3)
    y = Q(0)
    for k in range(3):
        u = Q(4) - y
        y = Q(1, 2) * y + Q(1, 2) * u
        check("P-only y[%d]" % (k + 1), y, [Q(2), Q(2), Q(2)][k])
    check("P-only droop = r/2", y, Q(2))

    # --- PI convergence: Kp=1, Ki=1/2 --------------------------------------
    ys, us, sats, integs = pid_run(1, Q(1, 2), 0, 4, 0, 1, -100, 100, 4)
    check("PI u0", us[0], Q(6))
    check("PI y1", Q(1, 2) * Q(0) + Q(1, 2) * us[0], Q(3))
    # full closed loop recomputed stepwise
    y = Q(0)
    integ = Q(0)
    traj = []
    for _ in range(4):
        err = Q(4) - y
        integ = integ + err
        u = err + Q(1, 2) * integ
        y = Q(1, 2) * y + Q(1, 2) * u
        traj.append((u, y, integ))
    for k, (u, yy, ii) in enumerate(traj):
        check("PI step%d u" % k, u, [Q(6), Q(7, 2), Q(29, 8), Q(119, 32)][k])
        check("PI step%d y-next" % k, yy, [Q(3), Q(13, 4), Q(55, 16), Q(229, 64)][k])
    # double-precision bit check of the same ops
    yf, intf = 0.0, 0.0
    for _ in range(4):
        err = 4.0 - yf
        intf = intf + err
        u = err + 0.5 * intf
        yf = 0.5 * yf + 0.5 * u
    check("PI y4 float==Fraction float", bits(yf), bits(float(traj[3][1])))

    # --- D kick: Kd=2, error step 4 -> 2, dt=1 ------------------------------
    check("D kick", Q(2) * (Q(2) - Q(4)) / Q(1), Q(-4))

    # --- anti-windup freeze --------------------------------------------------
    ys, us, sats, integs = pid_run(0, 1, 0, 4, 0, 1, -1, 1, 2)
    check("frozen u", us[0], Q(1))
    check("frozen sat", sats[0], True)
    integ = Q(5)
    err = Q(4)
    raw = integ + err
    check("freeze keeps integ", (integ if (min(max(raw, -1), 1) != raw and err * raw > 0) else raw), Q(5))

    # --- saturation clamp -----------------------------------------------------
    check("clamp hi", min(max(Q(9), Q(-1)), Q(1)), Q(1))
    check("clamp lo", min(max(Q(-9), Q(-1)), Q(1)), Q(-1))

    # --- open-loop step response -----------------------------------------------
    a, b, x0, u = Q(1, 2), Q(1, 2), Q(1), Q(3)
    check("step_once", a * x0 + b * u, Q(2))
    check("step_twice", a * (a * x0 + b * u) + b * u, Q(5, 2))
    check("equilibrium b*u/(1-a)", b * u / (1 - a), Q(3))
    # unstable growth stays bounded over the pinned horizon
    x = Q(1)
    for _ in range(3):
        x = Q(2) * x + Q(0)
    check("unstable a=2 growth", x, Q(8))

    print("----")
    if FAILURES:
        print("ORACLE FAIL: %d mismatches: %s" % (len(FAILURES), FAILURES))
        raise SystemExit(1)
    print("ORACLE PASS")


if __name__ == "__main__":
    main()
