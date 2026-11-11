#!/usr/bin/env python3
"""Generate the synthetic service-ticket corpus for the Axion Controls training case.

Deterministic (seeded). Produces corpus/service_tickets.csv with 200 tickets.
Planted patterns (used in labs and the M5 graph demo):
  - A cluster of F-07 overtemp tickets on VectorDrive 450 fw < 2.4.1 with P-210 >= 8 kHz  (SB-2025-04)
  - A burst of E-22 ETH2 lockup tickets on AX-900 fw <= 3.2 in early 2026                 (SB-2026-01)
  - Background noise across all products and fault codes
"""
import csv, random
from datetime import date, timedelta

random.seed(42)

SITES = [
    ("Meridian Logistics, Nagpur", "sortation"),
    ("Kaveri Industrial Water, Hosur", "water"),
    ("Deccan Beverages, Pune", "bottling"),
    ("SteelAxis Tubes, Raipur", "steel"),
    ("Everpack Foods, Coimbatore", "packing"),
    ("Nordwind Dairy, Esbjerg", "dairy"),
    ("Helios Components, Brno", "discrete"),
    ("Cascade Paper, Tampere", "paper"),
    ("Altona Chemicals, Hamburg", "chemicals"),
    ("Redstone Mining Services, Perth", "mining"),
    ("Bluegrass Bottling, Louisville", "bottling"),
    ("Sierra Cement, Monterrey", "cement"),
]

DRIVE_FW = ["2.2", "2.3", "2.4.0", "2.4.1", "2.5"]
PLC_FW = ["3.0", "3.1", "3.2", "3.3", "3.4"]

def d(start, end):
    s, e = date.fromisoformat(start), date.fromisoformat(end)
    return (s + timedelta(days=random.randint(0, (e - s).days))).isoformat()

tickets = []
tid = 10400

def add(dt, site, product, fw, fault, sev, status, subject, desc, resolution):
    global tid
    tid += random.randint(1, 9)
    tickets.append({
        "ticket_id": f"TKT-{tid}", "opened": dt, "customer_site": site,
        "product": product, "firmware_version": fw, "fault_code": fault,
        "severity": sev, "status": status, "subject": subject,
        "description": desc, "resolution": resolution,
    })

# --- Pattern 1: F-07 cluster (SB-2025-04). ~28 tickets, warm months, fw < 2.4.1, hi switching
f07_sites = ["Deccan Beverages, Pune", "Everpack Foods, Coimbatore", "Sierra Cement, Monterrey",
             "Bluegrass Bottling, Louisville", "SteelAxis Tubes, Raipur"]
for i in range(28):
    site = random.choice(f07_sites)
    fw = random.choice(["2.2", "2.3", "2.4.0"])
    khz = random.choice([8, 10, 12])
    dt = d("2024-11-01", "2025-09-30")
    resolved = dt > "2025-06-18"
    add(dt, site, "VectorDrive 450", fw, "F-07", random.choice(["Medium", "High"]),
        "Closed" if resolved else random.choice(["Closed", "Closed", "Open"]),
        "Drive trips F-07 overtemperature repeatedly under normal load",
        f"Drive on {random.choice(['conveyor section','packing line','mixer','extruder feed'])} trips F-07 every "
        f"{random.choice([45, 60, 75, 90])} minutes. Filters clean, fan passes power-up self-test. "
        f"Switching frequency P-210 is {khz} kHz for noise reasons. Cabinet ambient around "
        f"{random.choice([34, 36, 38, 40])} degC. Fan speed at trip logged below 80 percent.",
        ("Matched Service Bulletin SB-2025-04. Upgraded firmware to 2.4.1; no further trips in 2-week follow-up."
         if resolved else
         "Fan kit FAN-450 replaced on site; trips continued. Escalated to product support.")
    )

# --- Pattern 2: E-22 burst (SB-2026-01). ~14 tickets, Dec 2025 - Apr 2026, PLC fw <= 3.2
for i in range(14):
    site = random.choice([s for s, _ in SITES])
    fw = random.choice(["3.0", "3.1", "3.2"])
    dt = d("2025-12-01", "2026-04-30")
    resolved = dt > "2026-02-09"
    add(dt, site, "AX-900", fw, "E-22", "High",
        "Closed" if resolved else "Open",
        "All PROFINET devices lost at once, controller logs E-22",
        "Entire device network dropped simultaneously: AXIO stations show BF flashing, drives trip F-14 "
        "watchdog. HMI on ETH1 stayed connected. Diagnostic buffer shows W-13 jitter warnings before the "
        f"event. Site IT confirmed a {random.choice(['network scan','misconfigured CCTV camera','backup job'])} "
        "on the same VLAN at the time.",
        ("Matched Service Bulletin SB-2026-01. Upgraded controller firmware to 3.3, enabled storm guard, "
         "moved non-automation devices off the device VLAN." if resolved else
         "Power cycle restored the port. Monitoring; firmware upgrade scheduled.")
    )

# --- Background noise: ~158 tickets over all products
NOISE = [
    # (product, fault, subject, description, resolution, sev)
    ("VectorDrive 450", "F-01", "F-01 overcurrent at start",
     "Trips F-01 when the loaded conveyor restarts after an e-stop. Accel time P-110 currently {accel} s.",
     "Increased P-110 to {accel2} s and enabled flying start; no recurrence.", "Medium"),
    ("VectorDrive 450", "F-02", "F-02 overvoltage on stop",
     "High-inertia fan decelerates in {dec} s and trips F-02 roughly every third stop.",
     "Extended P-111 and quoted BRK-450 braking chopper; customer fitted chopper.", "Low"),
    ("VectorDrive 450", "F-05", "Nuisance F-05 motor overload",
     "F-05 trips under normal product load. Motor current parameter P-301 found at factory default.",
     "Set P-301 to nameplate value and re-ran auto-tune. Resolved.", "Low"),
    ("VectorDrive 450", "F-11", "F-11 earth fault after washdown",
     "F-11 appears after weekend washdown of the line. Terminal box gasket suspect.",
     "Megger test located moisture ingress; dried, resealed terminal box, replaced gasket.", "Medium"),
    ("VectorDrive 450", "F-14", "Drive drops to F-14 during shift change",
     "F-14 fieldbus watchdog on two drives, correlating with heavy traffic on the cell network.",
     "Raised P-610 to 1000 ms and moved CCTV off the device VLAN.", "Medium"),
    ("VectorDrive 450", "F-16", "F-16 internal fan failure",
     "Drive reports F-16; fan hours counter above 30000, A-10 had been active for months.",
     "Replaced fan kit FAN-450-{frame}. Advised acting on A-10 alarms.", "Low"),
    ("VectorDrive 450", "F-12", "F-12 encoder fault on closed-loop axis",
     "Intermittent F-12 on the {app} axis with ENC-01 card, cable run approx {cab} m.",
     "Re-terminated encoder cable, firmware updated to 2.5 which improves long-cable handling.", "Medium"),
    ("AX-900", "E-05", "AXIO station dropping intermittently",
     "Station {stn} drops and rejoins several times per shift. E-05 then automatic recovery in the log.",
     "Loose M12 bus connector reseated; motor cable moved to separate tray per AXN-MAN-0902.", "Medium"),
    ("AX-900", "E-08", "E-08 scan overrun after program update",
     "After adding recipe handling logic the CPU logs E-08 under peak load.",
     "Moved reporting logic to background task per manual; scan back within budget.", "Medium"),
    ("AX-900", "E-11", "Sporadic E-11 CRC errors on fieldbus",
     "E-11 counts rise during the day shift only. New VFD installed nearby last month.",
     "Motor cable shield was bonded at one end only; corrected 360-degree bonding both ends.", "Medium"),
    ("AX-900", "E-17", "E-17 network storm at power-up",
     "Controller stops fieldbus with E-17 after electrical contractor rewired the cabinet switch.",
     "ETH1 and ETH2 had been bridged via the office switch. Removed bridge, enabled storm guard.", "High"),
    ("AX-900", "E-19", "E-19 SD card write failure",
     "Data logging stopped; E-19 in diagnostics. Card is a consumer-grade card fitted by site.",
     "Replaced with AXN-SD-8 industrial card; advised archiving logs per W-09 guidance.", "Low"),
    ("AX-900", "E-01", "E-01 checksum error at boot",
     "CPU fails to start after a power cut, E-01 program checksum error shown.",
     "Reloaded project from archive. SD card showed wear; replaced under advance-exchange.", "High"),
    ("AXIO-16", "SF", "SF LED steady red after module swap",
     "Replaced a failed expansion unit; station now shows SF steady red.",
     "Fitted module type did not match configuration; corrected hardware config in project.", "Low"),
    ("AXIO-16", "UF", "Outputs off, UF LED dark on station",
     "All outputs on station {stn} off. Logic still communicating with the PLC.",
     "Field supply fuse blown by a shorted solenoid; fuse replaced, solenoid rewired.", "Medium"),
    ("AXIO-16", "BF", "BF flashing on new station",
     "Newly added station will not join the bus, BF flashing.",
     "Station name mismatch between device and project; corrected name, joined immediately.", "Low"),
    ("OptiPanel 7", "-", "Panel shows #### on several tags",
     "After a PLC program update, several faceplates show #### instead of values.",
     "Panel project was stale; redeployed from OptiDesigner after PLC changes.", "Low"),
    ("OptiPanel 7", "-", "Panel reboots during afternoon shift",
     "Panel restarts two or three times between 14:00 and 16:00. THERMAL_RESET entries in service log.",
     "Enclosure ambient above 50 degC; relocated panel and added vent kit.", "Medium"),
    ("OptiPanel 7", "-", "Connection refused BadMaxConnectionsReached",
     "Second panel added to the line will not connect; error BadMaxConnectionsReached.",
     "OPC UA session limit reached; moved data logger to slower poll group, planned fw 3.4 upgrade "
     "which raises the session limit to 12.", "Low"),
    ("OptiPanel 7", "-", "Certificate warning after controller upgrade",
     "Panel warns about an untrusted server certificate since the PLC firmware upgrade.",
     "Controller regenerated its OPC UA certificate; re-trusted in panel security settings.", "Low"),
]

for i in range(158):
    product, fault, subject, desc, res, sev = random.choice(NOISE)
    site = random.choice([s for s, _ in SITES])
    fw = random.choice(DRIVE_FW) if product == "VectorDrive 450" else (
         random.choice(PLC_FW) if product == "AX-900" else "-")
    desc = desc.format(accel=random.choice([3, 5]), accel2=random.choice([8, 12]),
                       dec=random.choice([4, 6]), frame=random.choice("ABCD"),
                       app=random.choice(["winder", "cutter", "indexing"]),
                       cab=random.choice([25, 40, 60]), stn=random.randint(1, 8))
    res = res.format(accel2=random.choice([8, 12]), frame=random.choice("ABCD"))
    status = random.choices(["Closed", "Open", "In Progress"], weights=[8, 1, 1])[0]
    add(d("2024-09-01", "2026-10-31"), site, product, fw, fault, sev, status,
        subject, desc, res if status == "Closed" else "")

tickets.sort(key=lambda t: t["opened"])
with open("corpus/service_tickets.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(tickets[0].keys()))
    w.writeheader()
    w.writerows(tickets)

print(f"Wrote {len(tickets)} tickets to corpus/service_tickets.csv")
f07 = [t for t in tickets if t["fault_code"] == "F-07" and t["firmware_version"] in ("2.2", "2.3", "2.4.0")]
e22 = [t for t in tickets if t["fault_code"] == "E-22"]
print(f"  SB-2025-04 pattern (F-07, fw<2.4.1): {len(f07)}")
print(f"  SB-2026-01 pattern (E-22): {len(e22)}")
