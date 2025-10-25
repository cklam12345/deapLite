from flask import Flask, jsonify
import asyncio
from bleak import BleakScanner
import threading

app = Flask(__name__)
DEVICE_NAME = "Friend"

# Async function to scan and get RSSI
async def get_device_rssi():
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name and DEVICE_NAME.lower() in device.name.lower():
            return {
                "name": device.name,
                "address": device.address,
                "rssi": device.rssi,
                "status": "device found"
            }
    return {"status": "device not found", "rssi": None}

# Flask endpoint to get RSSI
@app.route('/rssi', methods=['GET'])
def rssi():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(get_device_rssi())
    return jsonify(result)

# Run Flask server
def run_flask():
    app.run(port=5006)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
``
