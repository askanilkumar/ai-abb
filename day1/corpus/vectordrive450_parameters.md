# VectorDrive 450 — Parameter Quick Reference

**Document ID:** AXN-MAN-4502 · **Revision:** D

Parameters are set from the keypad, AxionStudio Drive Manager, or over PROFINET acyclic services. Defaults suit a standard 4-pole induction motor on a conveyor duty.

## Motor data (P-3xx) — set these first

| Param | Name | Default | Notes |
|---|---|---|---|
| P-301 | Motor rated current | frame-dependent | From the motor nameplate. Wrong values cause nuisance F-05 trips |
| P-302 | Motor rated voltage | 400 V | Nameplate |
| P-303 | Motor rated frequency | 50 Hz | Nameplate |
| P-304 | Motor rated speed | 1,450 rpm | Nameplate |
| P-310 | Auto-tune | 0 | Set 1 and press RUN for standstill auto-tune; required for vector modes |

## Ramps and limits (P-1xx)

| Param | Name | Default | Notes |
|---|---|---|---|
| P-110 | Acceleration time | 10 s | 0 → rated frequency |
| P-111 | Deceleration time | 10 s | Short decel on high-inertia loads causes F-02 |
| P-120 | Current limit | 150% | Of P-301 |
| P-125 | Minimum frequency | 0 Hz | Pumps: set ≥ 15 Hz to avoid dry-running |
| P-126 | Maximum frequency | 50 Hz | |

## Control and switching (P-2xx)

| Param | Name | Default | Notes |
|---|---|---|---|
| P-200 | Control mode | 0 (V/f) | 1 = sensorless vector, 2 = closed-loop (needs ENC-01) |
| P-210 | Switching frequency | 4 kHz | 2–12 kHz. Above 8 kHz: quieter motor, more heatsink load — **on firmware below 2.4.1 see SB-2025-04 before raising this** |
| P-220 | Flying start | 0 | Set 1 for fans that windmill |

## Fieldbus (P-6xx)

| Param | Name | Default | Notes |
|---|---|---|---|
| P-601 | PROFINET station name | vd450-xx | Must match the AX-900 project |
| P-610 | Watchdog timeout | 500 ms | F-14 after this |
| P-611 | Watchdog action | 1 (ramp stop) | 0 = coast, 2 = hold last speed |

## Common recipes

- **Conveyor section:** P-200 = 1 (sensorless vector), auto-tune, P-110/P-111 = 5 s, P-210 = 4 kHz.
- **Quiet area (packing hall):** P-210 = 8–10 kHz **only after confirming firmware ≥ 2.4.1**; check derating table in AXN-MAN-4501.
- **Centrifugal pump:** P-200 = 0, P-125 = 15 Hz, P-220 = 1 if non-return valve leaks back.
