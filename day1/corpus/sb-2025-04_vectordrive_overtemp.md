# Service Bulletin SB-2025-04 — VectorDrive 450 nuisance F-07 trips at high switching frequency

**Issued:** 2025-06-18 · **Severity:** Medium · **Products affected:** VectorDrive 450, all frames, **firmware 2.4.0 and earlier** · **Fixed in:** firmware **2.4.1** (released 2025-05-30)

## Summary

VectorDrive 450 units running firmware 2.4.0 or earlier can trip **F-07 (heatsink overtemperature)** repeatedly when the switching frequency (parameter **P-210**) is set to **8 kHz or higher**, even with clean filters and a working fan. Field reports cluster in warm cabinets (ambient above 35 °C) on conveyor and packing-hall applications where high switching frequencies are used for acoustic reasons.

## Root cause

The cooling-fan ramp algorithm in firmware ≤ 2.4.0 estimates heatsink temperature from a thermal model instead of the fastest sensor when switching frequency exceeds 7.5 kHz. The model under-reads by up to 12 °C during sustained load, so the fan ramps late. The heatsink then crosses the trip threshold before the fan reaches full speed, latching F-07. After cool-down the drive resets and the cycle repeats — typically every 40–90 minutes under steady load.

## Identifying affected units

An affected unit shows **all** of the following:

1. Firmware version below 2.4.1 (keypad: MENU → INFO → FW).
2. P-210 set to 8 kHz or above.
3. F-07 entries in the fault log where logged heatsink temperature at trip is within 5 °C of the trip threshold and fan speed at trip is below 80%.

Units on firmware 2.4.1 or later display alarm **A-12 (firmware update recommended)** = never for this issue; units on older firmware with P-210 ≥ 8 kHz raise A-12 at every power-up.

## Corrective action

- **Permanent fix:** upgrade to firmware **2.4.1 or later** using AxionStudio Drive Manager. Parameters are preserved. Upgrade takes about 4 minutes per drive and requires the motor to be stopped.
- **Interim workaround:** reduce P-210 to 4 kHz. Acoustic noise increases slightly; thermal margin is restored immediately.
- Hardware replacement is **not** required. Fan kits replaced for this symptom have shown a <3% actual fan failure rate — check firmware before ordering FAN-450 kits.

## Warranty note

Repeat site visits for F-07 on firmware ≤ 2.4.0 with P-210 ≥ 8 kHz are covered as a firmware defect under the standard warranty. Reference this bulletin number in the ticket.
