# AX-900 PLC — Diagnostics and Fault Code Reference

**Document ID:** AXN-MAN-0903 · **Revision:** J

The AX-900 reports faults on the front-panel display, in the AxionStudio diagnostics view, and over OPC UA (node `Diag.ActiveFaults`). Faults are prefixed **E-** (stop or degrade the controller) and warnings **W-** (informational, controller keeps running).

## Fault codes (E-)

| Code | Name | Cause | Action |
|---|---|---|---|
| E-01 | Program checksum error | Corrupted program load, failing SD card | Reload project; replace SD card if it recurs |
| E-03 | Supply undervoltage | 24 V dip longer than 10 ms | Check PSU sizing; fit AXN-UPS-24 buffer |
| E-05 | I/O bus timeout | AXIO-16 station lost | Check PROFINET cabling, station power |
| E-08 | Scan overrun | Program exceeds scan class budget | Move heavy logic to background task |
| E-11 | Fieldbus CRC errors | EMC coupling from drive cables | Fix motor cable shielding; separate routing |
| E-14 | Redundancy sync lost | AX-RSM-1 fibre broken or partner CPU down | Inspect sync fibre; check partner state |
| E-17 | Network storm detected | ETH1/ETH2 bridged externally; loop in topology | Remove loop; enable storm guard in project |
| E-19 | SD card write failure | Card worn out or write-protected | Replace with AXN-SD-8 industrial card |
| E-22 | ETH2 port lockup | Firmware below 3.3 under sustained >8,000 pps multicast | **Upgrade to firmware 3.3 or later — see SB-2026-01.** Power cycle clears it temporarily |
| E-25 | Fail-safe mismatch | Safety program CRC differs between CPUs | Re-download safety program with SafetyBuilder |

## Warning codes (W-)

| Code | Name | Meaning |
|---|---|---|
| W-02 | Clock not set | RTC lost after >14 days unpowered |
| W-09 | SD card nearly full | Archive and clear data logs |
| W-13 | Fieldbus jitter high | PROFINET update jitter above 30% of cycle |
| W-21 | Thermal derating active | Cabinet above 50 °C without fan tray |
| W-27 | Certificate expiring | OPC UA server certificate within 30 days of expiry |

## Diagnostic buffer

The CPU keeps the last 2,048 diagnostic events with 1 ms timestamps in non-volatile memory. Export via AxionStudio → Online → Diagnostic Buffer → Export CSV. When raising a support case, always attach this export and the project archive; tickets without the buffer export take on average three extra days to resolve.

## Escalation

If a fault persists after the listed action, raise a ticket with Axion Support (support.axioncontrols.example) quoting the fault code, firmware version, and diagnostic buffer export. Hardware with fault E-01 or E-19 recurring within 30 days is replaced under the advance-exchange programme.
