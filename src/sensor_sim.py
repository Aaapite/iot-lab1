import json
import random
import sys
import time

import paho.mqtt.client as mqtt

DEVICE = sys.argv[1] if len(sys.argv) > 1 else "sensor01"
BROKER = "127.0.0.1"

c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=DEVICE)
c.connect(BROKER, 1883)  # Lab 1 baseline: no TLS or credentials
c.loop_start()

try:
    while True:
        reading = {
            "device": DEVICE,
            "temp": round(random.uniform(24, 32), 1),
            "hum": random.randint(50, 80),
            "ts": int(time.time()),
        }
        c.publish(
            f"campus/{DEVICE}/telemetry",
            json.dumps(reading),
            qos=1,
        )
        print("sent", reading, flush=True)
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped", DEVICE, flush=True)
finally:
    c.disconnect()
    c.loop_stop()
