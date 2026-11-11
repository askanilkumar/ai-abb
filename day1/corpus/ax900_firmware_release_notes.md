# AX-900 Controller Firmware — Release Notes

**Document ID:** AXN-RN-0934 · Covers firmware 3.0 → 3.4

## Firmware 3.4 (2026-06-10) — current recommended

- Improves OPC UA server throughput by ~25%; supports 12 concurrent sessions (up from 8).
- Adds scan-class telemetry counters readable at `Diag.ScanStats` for performance monitoring.
- Diagnostic buffer export now includes fan-tray and cabinet temperature history.
- Fixes: W-27 certificate expiry warning now fires 30 days ahead (was 7); E-08 scan overrun reporting now names the offending task.

## Firmware 3.3 (2026-01-22)

- **Fixes E-22 ETH2 port lockup under multicast burst — see Service Bulletin SB-2026-01.** Rewritten receive-descriptor recovery path in the ETH2 MAC driver.
- Adds storm guard option (Project → Controller → Network) with configurable packet-rate threshold.
- Adds support for AXIO-16E expansion unit hardware rev 3.

## Firmware 3.2 (2025-08-04)

- Adds OPC UA method-call support for recipe handling.
- Faster redundancy sync on AX-900R: failover time reduced from 120 ms to 80 ms.
- Fixes: E-14 sporadic redundancy sync loss when sync fibre length exceeds 40 m.

## Firmware 3.1 (2025-03-11)

- First version supporting the AX-900R redundant CPU (lockstep diagnostics).
- Adds TLS 1.3 for OPC UA; older clients fall back to TLS 1.2.
- Fixes: E-19 false SD-card write failures with AXN-SD-8 cards manufactured after 2024-10.

## Firmware 3.0 (2024-11-05)

- New baseline for hardware rev 2. Not installable on rev 1 hardware.
- PROFINET stack updated; supports 1 ms update for 128 devices (was 64).
- Known issues at release: ETH2 lockup under multicast burst (fixed in 3.3); scan overrun mis-reporting (fixed in 3.4).

## Upgrade guidance

Upgrade path from any 3.x version directly to 3.4 is supported. From 2.x, upgrade to 3.0 first (project conversion required in AxionStudio 12). Always export the diagnostic buffer and project archive before upgrading. Controllers in hot-standby pairs: upgrade standby first, fail over, upgrade the former active.
