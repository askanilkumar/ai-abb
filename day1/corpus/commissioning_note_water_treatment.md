# Commissioning Note — Raw Water Pump House, Kaveri Industrial Water, Hosur

**Project:** KIW-RWPH · **Commissioned:** 2026-03-09 to 2026-03-13 · **Engineer:** field services team
**System:** 1 × AX-900 (standard), 2 × AXIO-16 stations, 5 × VectorDrive 450 (frame C), 1 × OptiPanel 7

## As-left configuration

- Controller firmware 3.4 (shipped current). Storm guard enabled by default policy.
- All five pump drives on firmware 2.5, P-200 = 0 (V/f), P-125 = 15 Hz minimum frequency to protect against dry running, P-220 = 1 (flying start) on pumps 1–3 where the non-return valves leak back.
- Pump house ambient measured 41 °C in the afternoon. Drives are frame C at P-210 = 4 kHz; derating table in AXN-MAN-4501 checked — within limits, but cabinet extraction fan added to the recommendations.
- OptiPanel mounted at the operator desk on ETH1, 60 m shielded run.

## Issues found and resolved

1. **F-11 (earth fault) on pump 4 at first start.** Terminal box had taken rain during storage on site. Dried, megger test passed at 550 MΩ, no recurrence over the 72-hour run.
2. **W-21 (thermal derating) on the controller** during the afternoon of day 2. Cabinet was above 50 °C with the doors closed and no fan tray. Fitted AXN-FAN-2 from van stock; warning cleared.
3. **A-04 (supply phase imbalance) logged repeatedly** between 14:00 and 17:00 daily — traced to the site's borewell starters on the same feeder. Logged for the customer's electrical contractor; drives ride through, no trips.
4. **Panel certificate warning** after we upgraded the controller from 3.3 to 3.4 on day 1 (OPC UA certificate regenerated). Re-trusted per AXN-MAN-0701.

## Outstanding / handover items

- Customer to fit cabinet extraction fan before summer peak (quote attached to project file).
- Electrical contractor to investigate afternoon phase imbalance.
- Operators trained: fault log reading on the keypad, filter mat cleaning monthly, what A-07 (heatsink warm) means before it becomes F-07.
