# OptiPanel 7 HMI — Manual Extract

**Document ID:** AXN-MAN-0701 · **Revision:** B

## Description

The OptiPanel 7 is a 7-inch touch HMI for AX-900 systems. It connects to the controller's ETH1 port and reads tags over OPC UA. Screens are built in the OptiDesigner tool and deployed over the network or from USB.

## Specifications

| Parameter | Value |
|---|---|
| Display | 7" TFT, 1024 × 600, 400 cd/m², resistive touch |
| Interfaces | 1 × 100 Mb Ethernet, 2 × USB-A, 1 × USB-C (service) |
| Protocols | OPC UA client, Modbus TCP client |
| Supply | 24 V DC, 8 W |
| Front protection | IP65 |
| Operating temperature | 0 °C to +50 °C |

## Connectivity rules

- Connect the OptiPanel to **ETH1** of the AX-900, never to ETH2 (fieldbus). Panels on ETH2 add OPC UA traffic to the device network and can push PROFINET jitter above the W-13 threshold.
- One AX-900 serves up to 8 concurrent OPC UA sessions. Each OptiPanel uses one session; AxionStudio online uses another. Session exhaustion shows on the panel as "connection refused (BadMaxConnectionsReached)".

## Common issues

| Symptom | Cause | Fix |
|---|---|---|
| Tags show `####` | Tag renamed in PLC project, panel project stale | Redeploy panel project after PLC changes |
| Panel reboots in warm cabinets | Above 50 °C ambient | Relocate or ventilate; panel logs `THERMAL_RESET` in the service log |
| Slow screen changes | >500 tags on one screen | Split screens; use tag groups with slower poll rates for trends |
| Certificate warning after PLC firmware upgrade | PLC OPC UA server certificate regenerated | Re-trust the certificate in panel settings → Security |

## Service log

Export the service log from Settings → Maintenance → Export to USB. Include it with any support ticket about panel restarts or connectivity.
