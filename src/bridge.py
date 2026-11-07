import json
import logging
import sys
import uuid

import requests
import paho.mqtt.client as mqtt

CSE = "http://127.0.0.1:7579/Mobius"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("evidence/lab1/bridge.log", encoding="utf-8"),
    ],
)

http = requests.Session()
http.trust_env = False

def on_connect(client, userdata, flags, reason_code, properties):
    logging.info("MQTT connection: %s", reason_code)
    if reason_code == 0:
        client.subscribe("campus/+/telemetry")

def on_subscribe(client, userdata, mid, reason_codes, properties):
    logging.info(
        "MQTT subscription acknowledged: %s",
        [str(code) for code in reason_codes],
    )

def on_message(client, userdata, msg):
    device = msg.topic.split("/")[1]
    try:
        payload = json.loads(msg.payload)
        response = http.post(
            f"{CSE}/{device}/telemetry",
            headers={
                "X-M2M-Origin": "C" + device,
                "X-M2M-RI": "lab1-" + uuid.uuid4().hex,
                "X-M2M-RVI": "3",
                "Content-Type": "application/json;ty=4",
                "Accept": "application/json",
            },
            json={"m2m:cin": {"con": payload}},
            timeout=5,
        )
        rsc = response.headers.get("X-M2M-RSC")
        logging.info(
            "%s: HTTP %s; X-M2M-RSC %s",
            device, response.status_code, rsc,
        )
        if response.status_code != 201 or rsc != "2001":
            logging.error("Mobius response: %s", response.text)
    except (ValueError, UnicodeDecodeError, requests.RequestException) as error:
        logging.error("%s forwarding failed: %s", device, error)

c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="bridge")
c.on_connect = on_connect
c.on_subscribe = on_subscribe
c.on_message = on_message

logging.info("Starting bridge: MQTT 127.0.0.1:1883 -> %s", CSE)
c.connect("127.0.0.1", 1883)

try:
    c.loop_forever()
except KeyboardInterrupt:
    logging.info("Bridge stopped")
finally:
    c.disconnect()
    http.close()
