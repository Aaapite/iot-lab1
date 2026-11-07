# 7. Baseline findings table from Lab 1

Our baseline tests confirmed anonymous MQTT access, readable MQTT payloads, fake telemetry reaching Mobius, and read/create access using an unregistered origin. F5 records the services found on the selected local ports. F6 records a negative result within the source files reviewed.

## Test environment and scope

We used the simulated track on one Windows 11 laptop: two Python 3.13.14 devices (`sensor01` and `sensor02`), Eclipse Mosquitto 2.0.22, a Python MQTT-to-HTTP bridge, Mobius 3.0.1 on Node.js 24.12.0, and MySQL 8.4.11. Mosquitto and MySQL ran in Docker. The published broker/database ports and the Mobius HTTP listener were bound to `127.0.0.1`. All test targets belonged to our own testbed.

Testing took place on 7–8 November 2026, Malaysia time (UTC+08:00). The device readings were simulated temperature and humidity values. Flask, SQLite and the dashboard were outside this baseline.

| # | Finding and actual result | Evidence file | MTSFB threat / weakness | Fixed in |
|---|---|---|---|---|
| F1 | **Confirmed — anonymous MQTT subscription.** A client without credentials subscribed to `#` and received eight telemetry messages covering both sensor01 and sensor02. Subscriber exit code: 0. | `A_sub_all.png`; `F1_anonymous_subscribe.txt` | T-Sec-3 / R-Sec-5 | Lab 3 |
| F2 | **Confirmed — plaintext MQTT telemetry.** A captured PUBLISH packet displayed `campus/sensor02/telemetry` and readable JSON containing `"temp":31.4` and `"hum":50`. | `lab1_plain_mqtt.pcapng`; `F2_readable_payload.png` | T-Sec-4 / R-Sec-3 | Lab 3 |
| F3 | **Confirmed — fake telemetry accepted and stored.** With the genuine sensor01 process stopped, an anonymous client published `{"device":"sensor01","temp":99.9,"hum":0}`. The broker acknowledged it, and Mobius returned the same fake values through the latest resource (HTTP 200; X-M2M-RSC 2000). | `F3_mqtt_injection.txt`; `F3_mobius_latest.txt`; `F3_injection_stored.png` | Proposed: T-Sec-3 / R-Sec-6 | Labs 3 and 5 |
| F4 | **Confirmed — unregistered origin could read and create.** Requests using `X-M2M-Origin: Chacker` read sensor01's latest resource (HTTP 200; X-M2M-RSC 2000) and created a contentInstance in its telemetry container (HTTP 201; X-M2M-RSC 2001). The created resource recorded `cr: Chacker`. | `F4_spoof_read.txt`; `F4_spoof_write.txt`; `F4_spoofed_origin_read.png`; `F4_spoofed_origin_write.png` | Proposed: T-Sec-3 / R-Sec-7 | Lab 5 |
| F5 | **Observed — selected local services were open.** Nmap identified 1883/tcp: Mosquitto 2.0.22; 3306/tcp: MySQL 8.4.11; and 7579/tcp: HTTP, Node.js Express framework. Both scans completed successfully. This is a service inventory observation; an open port alone does not establish a vulnerability. | `nmap_gateway.txt`; `nmap_server.txt` | Proposed review category: T-Sec-3 / R-Sec-6 | Lab 4 |
| F6 | **Not observed within the reviewed scope.** The credential-keyword scan returned zero candidate lines across `sensor_sim.py`, `bridge.py` and `register_resources.py`. The three checked private paths were ignored by Git, with zero tracked private paths. Wi-Fi credentials were not needed for this simulated track. | `F6_source_review.txt`; `F6_git_exclusions.txt`; `F6_credential_review.png` | Category screened, not detected: T-Sec-3 / R-Sec-1 (proposed) | Lab 3 preventive review; no hardcoded credential issue established in this scope |

## Interpretation and limits

The "Fixed in" column identifies the lecturer's planned follow-up labs. It does not mean these weaknesses have already been fixed.

F4 establishes the result for the tested sensor01 resources and the two tested operations. It does not establish that every resource or every origin is accepted.

For F5, gateway and platform roles were on the same laptop. We deliberately scanned only ports 1883, 3306 and 7579 on `127.0.0.1` to keep the scan within our lab services and avoid unrelated projects. This adapts the guide's wider port ranges. The results are not a complete host port inventory and do not demonstrate LAN or Internet exposure.

F6 used a credential-keyword scan, which can miss secrets written in other forms. Its Git check covered `.secrets/mysql-root.txt`, `Mobius/conf.json` and `Mobius/conf.seal.json` at the time of review. Vendor source, dependencies, all other files, chat history and historical disclosures were outside this check. The result does not certify that the entire testbed is free of credentials or default values.

## Mapping basis

The F1 and F2 mappings are supplied directly in the lecturer's Lab 1 findings table. F3–F6 are proposed mappings, using the same course notation and the corresponding category order and descriptions in the MTSFB July 2026 public draft. The draft itself does not print the course's T-Sec/R-Sec aliases.

The relevant categories are weak configurations/open services (T-Sec-3), communication interception (T-Sec-4), weak or hardcoded passwords (R-Sec-1), insecure data transfer/storage (R-Sec-3), insecure defaults (R-Sec-5), insecure network services (R-Sec-6), and insecure ecosystem interfaces (R-Sec-7). F5's category is for exposure review; F6's category was screened without establishing a positive finding.

Sources:

- [Lecturer's official Lab 1 guide](https://vle.unikl.edu.my/mod/book/tool/print/index.php?id=103283450), Parts C–D and baseline findings table; consulted through the supplied saved VLE HTML.
- [MTSFB July 2026 public draft](https://mtsfb.org.my/wp-content/uploads/2026/07/MTSFB2511R0_Internet-of-Things-IoT-Safety-Security-and-Privacy-Management.pdf), Tables 1 and 3, for the proposed category mappings.

## Setup evidence

| Checkpoint | Recorded result | Screenshot |
|---|---|---|
| A1 | MQTT test publication was received as `campus/test hello`. | `A1.png`; `A1_publisher.png` |
| B1 | Telemetry from both simulated devices was received. | `B1.png` |
| C1 | The bridge reported HTTP 201 and X-M2M-RSC 2001 for both devices. | `C1.png` |
| C2 | Mobius returned sensor01's latest stored reading with HTTP 200 and X-M2M-RSC 2000. | `C2.png`; `C2_latest_sensor01.txt` |

All evidence filenames above refer to `evidence/lab1/`. The saved capture is 31,932 bytes. Both Nmap reports and the source/Git review reports were checked against their saved contents.

