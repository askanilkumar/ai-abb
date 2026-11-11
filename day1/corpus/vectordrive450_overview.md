# VectorDrive 450 Variable-Frequency Drive — Product Overview

**Document ID:** AXN-MAN-4501 · **Revision:** F · **Applies to:** VectorDrive 450, frame sizes A–D

## Description

The VectorDrive 450 is a general-purpose variable-frequency drive for three-phase induction and permanent-magnet motors from 0.75 kW to 160 kW. It is the standard drive companion to the AX-900 PLC on conveyor, pump, fan and mixer applications, controlled over PROFINET or via hard-wired I/O.

## Key specifications

| Parameter | Value |
|---|---|
| Power range | 0.75–160 kW (frames A–D) |
| Supply | 380–480 V AC, 3-phase, 50/60 Hz |
| Control modes | V/f, sensorless vector, closed-loop vector (with ENC-01 option) |
| Switching frequency | 2–12 kHz, parameter P-210 |
| Overload | 150% for 60 s (heavy duty) |
| Fieldbus | PROFINET (built-in), Modbus RTU |
| Ambient | −10 °C to +50 °C; derate 1.5%/°C above 40 °C at >8 kHz switching |
| Protection | IP20 (cabinet mount), IP55 variant frame B only |
| Standards | CE, UL 61800-5-1, EMC category C2 with built-in filter |

## Frame sizes

| Frame | Power | Width |
|---|---|---|
| A | 0.75–7.5 kW | 72 mm |
| B | 11–30 kW | 115 mm |
| C | 37–90 kW | 190 mm |
| D | 110–160 kW | 290 mm |

## Firmware

Current recommended firmware is **2.5** (see release notes AXN-RN-4525). Drives shipped before March 2025 carry firmware 2.3 or earlier. **Firmware below 2.4.1 is affected by the cooling-fan control fault described in Service Bulletin SB-2025-04**: at switching frequencies of 8 kHz and above, the fan ramp algorithm underestimates heatsink temperature, which can lead to repeated **F-07 (heatsink overtemperature)** trips in warm cabinets. Upgrade via the AxionStudio Drive Manager; the upgrade keeps all parameters.

## Options

- **ENC-01** — encoder feedback card for closed-loop vector control.
- **BRK-450** — braking chopper, frames A–C (frame D has it built in).
- **KPD-450R** — remote-mount keypad with 3 m cable, IP65 front.
