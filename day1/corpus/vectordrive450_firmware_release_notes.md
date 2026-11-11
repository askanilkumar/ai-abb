# VectorDrive 450 Firmware — Release Notes

**Document ID:** AXN-RN-4525 · Covers firmware 2.0 → 2.5

## Firmware 2.5 (2026-04-02) — current recommended

- Adds energy-counter tags (kWh, cost estimate) readable over PROFINET for FinOps/energy reporting.
- Flying start (P-220) now works in closed-loop vector mode.
- Fixes: F-12 nuisance encoder faults on long encoder cables with ENC-01 rev B.

## Firmware 2.4.1 (2025-05-30)

- **Fixes the cooling-fan ramp fault behind nuisance F-07 heatsink overtemperature trips at switching frequencies ≥ 8 kHz — see Service Bulletin SB-2025-04.** Fan control now uses direct sensor reading at all switching frequencies.
- Adds alarm A-12 (firmware update recommended): the drive checks its version against open service bulletins stored in the drive database file loaded by AxionStudio.

## Firmware 2.4.0 (2025-02-17)

- Adds Modbus RTU slave on the keypad port.
- Improves auto-tune (P-310) accuracy for PM motors.
- Known issue found post-release: fan ramp under-reads heatsink temperature above 7.5 kHz switching (fixed in 2.4.1).

## Firmware 2.3 (2024-09-01)

- Adds closed-loop vector control with ENC-01 card.
- PROFINET watchdog action configurable (P-611).

## Firmware 2.2 (2024-03-15)

- EMC category C2 filter control refinements; lower conducted emissions at 2 kHz switching.
- Fixes: F-20 parameter checksum errors after brown-out during parameter save.

## Firmware 2.0 (2023-07-20)

- Baseline release for VectorDrive 450 frames A–D.

## Upgrade guidance

Upgrades are performed with AxionStudio Drive Manager over PROFINET or the keypad USB-C port. All parameters are preserved from 2.2 onward. The motor must be stopped; a frame-D drive takes about 6 minutes, smaller frames about 4. Fleet note: sites with mixed firmware should prioritise units with P-210 ≥ 8 kHz (SB-2025-04) and any unit showing A-12 at power-up.
