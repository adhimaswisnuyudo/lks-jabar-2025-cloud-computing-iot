import time
import json
import random
import ssl
import paho.mqtt.client as mqtt

# AWS IoT Config
ENDPOINT = "(Sesuaikan dengan endpoint AWS IoT Anda)"
PORT = 8883
CLIENT_ID = "(Sesuaikan dengan ID Klien Anda)"
TOPIC = "(Sesuaikan dengan topik yang Anda gunakan)"

CA_PATH = "(Sesuaikan dengan path CA Anda)"
CERT_PATH = "(Sesuaikan dengan path certificate Anda)"
KEY_PATH = "(Sesuaikan dengan path private key Anda)"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to AWS IoT Core!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published.")

def generate_payload():
    payload = {
        "device_id": CLIENT_ID,
        "lux": random.randint(100, 1000),
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }
    return json.dumps(payload)

def main():
    client = mqtt.Client(client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.tls_set(ca_certs=CA_PATH,
                   certfile=CERT_PATH,
                   keyfile=KEY_PATH,
                   tls_version=ssl.PROTOCOL_TLSv1_2)

    print(f"Connecting to {ENDPOINT} ...")
    client.connect(ENDPOINT, PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            message = generate_payload()
            result = client.publish(TOPIC, message, qos=1)
            status = result.rc
            if status == 0:
                print(f"Sent: {message}")
            else:
                print(f"Failed to send message, status code: {status}")
            time.sleep(20)

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()

