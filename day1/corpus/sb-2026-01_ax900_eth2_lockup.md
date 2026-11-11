# Service Bulletin SB-2026-01 — AX-900 ETH2 port lockup under multicast burst

**Issued:** 2026-02-09 · **Severity:** High · **Products affected:** AX-900, AX-900R, AX-900F with **firmware 3.2 and earlier** · **Fixed in:** firmware **3.3** (released 2026-01-22)

## Summary

On firmware 3.2 and earlier, the AX-900 ETH2 (fieldbus) port can stop forwarding frames after sustained multicast bursts above approximately 8,000 packets per second — for example when a misconfigured IP camera or a network scan floods the device VLAN. The controller logs fault **E-22 (ETH2 port lockup)**; PROFINET devices drop (AXIO-16 stations show BF flashing, VectorDrive 450 drives trip **F-14 fieldbus watchdog** and perform their P-611 action).

## Root cause

A receive-descriptor exhaustion bug in the ETH2 MAC driver. Under multicast burst the driver's recovery path can deadlock, leaving the port electrically up but not passing traffic.

## Identifying affected systems

- Firmware 3.2 or earlier (AxionStudio → Online → CPU Info).
- Diagnostic buffer shows E-22, often preceded by W-13 (fieldbus jitter high).
- All stations on ETH2 lost simultaneously, while ETH1 (HMI/service) stays reachable.

## Corrective action

- **Permanent fix:** upgrade controller firmware to **3.3 or later** (current recommended: 3.4). The upgrade requires a maintenance stop of approximately 10 minutes.
- **Interim mitigations:** enable storm guard in the project (Project → Controller → Network → Storm Guard), keep non-automation devices off the device VLAN, rate-limit multicast at the cell switch.
- A power cycle restores the port but does not prevent recurrence.

## Interaction with redundancy

On AX-900R pairs, E-22 on the active CPU triggers failover; if both CPUs sit on the same flooded VLAN the standby locks up within seconds as well. Hot-standby is therefore **not** a mitigation for this issue — upgrade both CPUs.
