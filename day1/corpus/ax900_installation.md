# AX-900 PLC — Installation and Wiring Guide

**Document ID:** AXN-MAN-0902 · **Revision:** E

## Mounting

Mount the AX-900 rack horizontally on a 35 mm DIN rail or panel. Leave **80 mm clearance above and below** the rack for convection cooling. Ambient above 50 °C requires the AXN-FAN-2 fan tray; without it the CPU derates its scan class and logs warning **W-21 (thermal derating active)**.

## Power wiring

- Supply: 24 V DC from a Class 2 / SELV source. Use 1.5 mm² (16 AWG) minimum.
- Connect functional earth (FE) terminal to the panel earth bar with a lead no longer than 300 mm.
- The CPU tolerates supply dips up to 10 ms. For longer dips fit the AXN-UPS-24 buffer module; unbuffered brownouts cause a cold restart and fault **E-03 (supply undervoltage)**.

## Ethernet wiring

- **ETH1** is the service and HMI port. Connect engineering laptops and OptiPanel 7 HMIs here.
- **ETH2** is the fieldbus port for PROFINET/EtherNet/IP device traffic. Do not bridge ETH1 and ETH2 through an external switch — this creates a loop and triggers fault **E-17 (network storm detected)**, which stops the fieldbus stack.
- Use shielded Cat 5e or better. Bond the shield at the cabinet entry.

## Grounding and noise

Route 24 V signal wiring at least 100 mm away from motor cables. VectorDrive 450 motor cables must be shielded and the shield bonded 360° at both ends; unshielded drive cables are the most common cause of sporadic **E-11 (fieldbus CRC errors)** on nearby AXIO-16 stations.

## Commissioning checklist (abbreviated)

1. Verify supply voltage at the CPU terminals: 22.8–28.8 V DC.
2. Confirm firmware version matches the project file (AxionStudio shows a yellow banner on mismatch).
3. Set the station name and IP on ETH2 before connecting devices.
4. Run the I/O wiring test from AxionStudio → Online → Wiring Check.
5. Save the as-commissioned project archive to the SD card.

## Replacement procedure

A failed CPU can be swapped in under 10 minutes: power down, remove terminal blocks (they are keyed), fit the new CPU, insert the SD card from the old unit. The CPU restores program, parameters and station name from the SD card on first boot. **The SD card is the configuration master** — label it with the line ID, not the CPU serial number.
