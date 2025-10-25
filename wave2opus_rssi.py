from flask import Flask, request, jsonify
import asyncio
from bleak import BleakScanner
import threading

app = Flask(__name__)

DEVICE_NAME = "Friend"
RSSI_THRESHOLD = -70  # Minimum acceptable RSSI

# Function to find device and check RSSI
async def check_rssi_and_start():
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name and DEVICE_NAME.lower() in device.name.lower():
            rssi = device.rssi
            if rssi >= RSSI_THRESHOLD:
                # Simulate starting recording
                print("Starting recording...")
                return {"status": "recording started", "rssi": rssi}
            else:
                return {"status": "signal too weak", "rssi": rssi}
    return {"status": "device not found", "rssi": None}

@app.route('/start', methods=['POST'])
def start():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(check_rssi_and_start())
    return jsonify(result)

# Run Flask in a separate thread
def run_flask():
    app.run(port=5005)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
