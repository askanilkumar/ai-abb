# AXIO-16 Remote I/O Module — Manual Extract

**Document ID:** AXN-MAN-1601 · **Revision:** C

## Description

The AXIO-16 is a DIN-rail remote I/O station for the AX-900 PLC over PROFINET. Each base unit carries 16 configurable channels; up to four expansion units (AXIO-16E) daisy-chain for 80 channels per station.

## Specifications

| Parameter | Value |
|---|---|
| Channels | 16 per base: DI 24 V, DO 0.5 A, AI 4–20 mA / 0–10 V, AO 4–20 mA — mixed per 4-channel group |
| Update rate | 1 ms PROFINET cycle supported |
| Supply | 24 V DC, separate logic (US) and field (UF) feeds |
| Temperature | −20 °C to +60 °C |
| Mounting | 35 mm DIN rail, spring-clamp terminals |

## Diagnostics

Channel-level diagnostics report to the AX-900 as PROFINET channel diagnoses and appear in AxionStudio with plain-text causes:

| LED pattern | Meaning | Action |
|---|---|---|
| SF red steady | Station fault — configuration mismatch | Compare configured vs fitted modules |
| BF red flashing | No PROFINET connection | Check cable, station name |
| Channel LED red | Wire break (AI 4–20 mA) or short (DO) | Field wiring check |
| US LED off | Logic supply missing | Check 24 V US feed |
| UF LED off | Field supply missing — outputs are off | Check UF fuse; outputs resume when restored |

## Wiring notes

- Keep UF (field) and US (logic) on separate breakers so a field short does not drop the station from the bus.
- Analog inputs: use shielded twisted pair, shield bonded at the cabinet entry only.
- A station that drops and rejoins the bus repeatedly (AX-900 logs E-05 then recovery) usually has a loose M12 bus connector or EMC coupling from a VectorDrive motor cable routed in the same tray — see the grounding section of AXN-MAN-0902.

## Hot swap

Base and expansion electronics unplug from the terminal block carrier. Field wiring stays in place. Replacing electronics takes under two minutes and the AX-900 reparameterises the new unit automatically.
