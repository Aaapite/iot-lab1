import uuid
from pathlib import Path

import requests

CSE = "http://127.0.0.1:7579/Mobius"
LOG = Path("evidence/lab1/resource_registration.txt")

def create(device, parent, resource_type, body):
    label = "AE" if resource_type == 2 else "telemetry container"
    headers = {
        "X-M2M-Origin": "C" + device,
        "X-M2M-RI": "lab1-" + uuid.uuid4().hex,
        "X-M2M-RVI": "3",
        "Content-Type": f"application/json;ty={resource_type}",
        "Accept": "application/json",
    }
    response = requests.post(
        parent, headers=headers, json=body, timeout=10
    )
    rsc = response.headers.get("X-M2M-RSC")
    summary = f"{device} {label}: HTTP {response.status_code}; X-M2M-RSC {rsc}"
    print(summary, flush=True)

    with LOG.open("a", encoding="utf-8") as log:
        log.write(
            f"{response.headers.get('Date', '')}\n"
            f"{summary}\n{response.text}\n\n"
        )

    if response.status_code != 201 or rsc != "2001":
        print(response.text, flush=True)
        raise SystemExit("Unexpected result. Share this output before continuing.")

for device in ("sensor01", "sensor02"):
    create(device, CSE, 2, {
        "m2m:ae": {
            "rn": device,
            "api": "Nlab1.campus",
            "rr": True,
            "srv": ["3"],
        }
    })
    create(device, f"{CSE}/{device}", 3, {
        "m2m:cnt": {
            "rn": "telemetry",
            "mni": 1000,
        }
    })

print("Responses saved to evidence/lab1/resource_registration.txt")
