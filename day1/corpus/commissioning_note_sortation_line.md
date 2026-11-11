# Commissioning Note — Parcel Sortation Line 2, Meridian Logistics, Nagpur

**Project:** MLN-SORT-2 · **Commissioned:** 2025-11-03 to 2025-11-14 · **Engineer:** field services team
**System:** 1 × AX-900R (redundant pair), 6 × AXIO-16 stations, 14 × VectorDrive 450 (frames A/B), 2 × OptiPanel 7

## As-left configuration

- Controller firmware 3.2 on both CPUs (3.3 was not yet released at commissioning). **Flagged for upgrade at first service visit — see SB-2026-01.**
- Drives: 11 units shipped with firmware 2.4.1, three older stock units with 2.3. The three 2.3 units are on induction sections where P-210 = 4 kHz, so SB-2025-04 does not bite, but they are listed in the upgrade register.
- All drive sections: P-200 = 1 (sensorless vector), auto-tuned, P-110/P-111 = 5 s.
- Merge and divert sections run P-210 = 8 kHz for noise reasons (adjacent to the returns office). **Both are on firmware 2.4.1 — verified against SB-2025-04 before setting.**

## Issues found and resolved during commissioning

1. **Repeated E-11 (fieldbus CRC) on AXIO station 4.** Motor cable for divert 3 was routed in the same tray as the station's bus drop. Re-routed with 150 mm separation; errors cleared. Matches the guidance in AXN-MAN-0902.
2. **E-17 (network storm) on first power-up.** The site electrician had patched ETH1 and ETH2 into the same office switch "to make everything reachable". Removed the bridge, enabled storm guard, documented the two-network rule on the cabinet door.
3. **OptiPanel sessions exhausted** during FAT replay: two panels + AxionStudio + the customer's OPC UA data logger + a test client hit the 8-session limit. Moved the data logger to a 5 s poll group and documented that firmware 3.4 raises the limit to 12.
4. **Nuisance F-05 on induction 1.** P-301 had the default, not nameplate, motor current. Corrected; no trips since.

## Outstanding / handover items

- Upgrade both AX-900R CPUs to firmware 3.3+ at the next maintenance window (standby first, then failover — per AXN-RN-0934).
- Upgrade the three firmware-2.3 drives to 2.5 in the same window.
- Spare parts on site: one AXIO-16 base, one FAN-450-B kit, one AXN-SD-8 card.
- Customer trained on diagnostic buffer export; shown where fault codes are in AXN-MAN-0903.
