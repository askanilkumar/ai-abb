# VectorDrive 450 — Fault Codes and Troubleshooting

**Document ID:** AXN-MAN-4503 · **Revision:** H

Faults are prefixed **F-** and latch until reset (keypad STOP/RESET, digital input, or fieldbus reset bit). Alarms are prefixed **A-** and clear automatically. The drive stores the last 32 faults with timestamps, output current, DC-bus voltage and heatsink temperature at the moment of trip — read them from the keypad under MENU → DIAG → FAULT LOG, or from AxionStudio Drive Manager.

## Fault codes (F-)

| Code | Name | Typical cause | Action |
|---|---|---|---|
| F-01 | Overcurrent | Acceleration too fast, shorted motor cable | Increase P-110 accel time; megger the motor cable |
| F-02 | DC bus overvoltage | Deceleration too fast, regenerative load | Increase P-111 decel time or fit BRK-450 chopper |
| F-03 | DC bus undervoltage | Supply dip or phase loss | Check incoming supply; see A-04 history |
| F-05 | Motor overload (I²t) | Mechanical jam, undersized motor | Check load; verify P-301 motor current setting |
| F-07 | Heatsink overtemperature | Blocked filter mats, fan failure, high ambient — **or firmware below 2.4.1 at ≥8 kHz switching, see SB-2025-04** | Clean filters, verify fan spins at power-up self-test; if firmware <2.4.1 and P-210 ≥ 8 kHz, upgrade firmware to 2.4.1+ |
| F-09 | Motor overtemperature | PTC/thermistor input open | Check motor thermistor wiring at terminals T1/T2 |
| F-11 | Earth fault | Insulation failure, moisture in terminal box | Megger motor and cable; dry out terminal box |
| F-12 | Encoder fault | ENC-01 feedback lost | Check encoder cable and supply; falls back to sensorless if P-402 = 1 |
| F-14 | Fieldbus watchdog | PROFINET connection lost longer than P-610 | Check network; drive performs P-611 action (coast/ramp/hold) |
| F-16 | Internal fan failure | Main cooling fan below minimum speed | Replace fan kit FAN-450-x for the frame size |
| F-20 | Parameter checksum | EEPROM corruption | Restore parameter backup; replace drive if recurring |

## Alarm codes (A-)

| Code | Name | Meaning |
|---|---|---|
| A-02 | Current limit active | Output held at limit; check mechanics |
| A-04 | Supply phase imbalance | One phase >5% low — log and watch |
| A-07 | Heatsink warm | Within 10 °C of F-07 trip level; pre-warning |
| A-10 | Fan service due | Cumulative fan hours above 30,000 |
| A-12 | Firmware update recommended | Drive detects it is on a version with an open service bulletin |

## The F-07 decision path

1. Read the fault log: trip temperature and ambient at trip time.
2. Physical checks: filter mats, fan self-test at power-up, cabinet ventilation.
3. **Check firmware and P-210.** If firmware is below 2.4.1 **and** P-210 (switching frequency) is 8 kHz or higher, the fan-control fault in SB-2025-04 is the likely cause — upgrade firmware before replacing hardware.
4. If trips continue on 2.4.1+ with clean airflow, reduce P-210 to 4 kHz (acoustic noise rises slightly) and raise a support ticket with the fault log export.

## Spare parts

| Kit | Covers |
|---|---|
| FAN-450-A/B/C/D | Main fan, per frame |
| CAP-450-C/D | DC bus capacitor bank, frames C–D |
| KPD-450 | Replacement keypad |
