# Lab 1: Simulated Baseline Architecture

```mermaid
flowchart TD
    subgraph Laptop["One Windows laptop - simulated track"]
        S1["sensor01 - Python simulator"]
        S2["sensor02 - Python simulator"]
        Q["Mosquitto in Docker - 127.0.0.1:1883"]
        B["Python MQTT-to-HTTP bridge"]
        M["Mobius - 127.0.0.1:7579"]
        DB["MySQL in Docker - 127.0.0.1:3306"]

        S1 -->|"Plain MQTT: campus/sensor01/telemetry"| Q
        S2 -->|"Plain MQTT: campus/sensor02/telemetry"| Q
        Q -->|"Subscription: campus/+/telemetry"| B
        B -->|"Plain HTTP: create contentInstance"| M
        M -->|"Database connection"| DB
    end
```

The simulators generated temperature and humidity readings.
Testing targeted the local testbed on 127.0.0.1.
Flask, SQLite and the dashboard were outside this baseline.
This diagram records the Lab 1 setup before security hardening.
