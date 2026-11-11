# AX-900 Programmable Logic Controller — Product Overview

**Document ID:** AXN-MAN-0901 · **Revision:** G · **Applies to:** AX-900 series, hardware rev 2 and later

## Description

The Axion Controls AX-900 is a rack-mounted programmable logic controller for medium and large automation systems: conveyor and sortation lines, batching plants, water treatment, and discrete manufacturing cells. The controller executes IEC 61131-3 programs (ladder, structured text, function block) with a guaranteed scan class of 1 ms for up to 2,000 I/O points.

## Key specifications

| Parameter | Value |
|---|---|
| CPU | Dual-core 800 MHz, lockstep option on AX-900R |
| Program memory | 64 MB |
| I/O capacity | 4,096 points local, 16,384 distributed |
| Fieldbus | PROFINET, EtherNet/IP, Modbus TCP |
| Ethernet ports | 2 × 1 GbE (ETH1 service, ETH2 fieldbus) |
| Redundancy | Hot-standby with AX-RSM-1 sync module |
| Supply | 24 V DC ±20%, 18 W typical |
| Operating temperature | −10 °C to +60 °C |
| Certifications | CE, UL 508, IEC 61010-2-201 |

## Variants

- **AX-900** — standard CPU.
- **AX-900R** — redundant-capable CPU with lockstep diagnostics. Requires firmware 3.1 or later.
- **AX-900F** — fail-safe variant, SIL 2 certified, for safety-instrumented functions. Uses the separate SafetyBuilder tool for the safety program.

## Firmware

Current recommended firmware is **3.4** (see release notes AXN-RN-0934). Firmware below 3.3 is affected by the ETH2 port lockup described in **Service Bulletin SB-2026-01** and should be upgraded during the next maintenance window.

## System architecture notes

The AX-900 pairs with AXIO-16 remote I/O modules over PROFINET and drives VectorDrive 450 variable-frequency drives over the same network. A typical sortation line runs one AX-900, four to eight AXIO-16 stations, and one VectorDrive 450 per motor section. The OptiPanel 7 HMI connects to ETH1 and subscribes to controller tags via OPC UA.

## Ordering information

| Order code | Description |
|---|---|
| AXN-0900-STD | AX-900 standard CPU |
| AXN-0900-RED | AX-900R redundant CPU |
| AXN-0900-FS | AX-900F fail-safe CPU |
| AXN-RSM-1 | Redundancy sync module |
