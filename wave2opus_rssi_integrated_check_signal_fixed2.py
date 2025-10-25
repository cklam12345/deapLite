import asyncio
import wave
import os
from datetime import datetime
from bleak import BleakClient, BleakScanner
import opuslib
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# Flags
stop_process = 0
recording_thread = None

# Device settings
DEVICE_NAME = "Friend"
SERVICE_UUID = "19b10000-e8f2-537e-4f6c-d104768a1214"
AUDIO_DATA_STREAM_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
AUDIO_CODEC_UUID = "19b10002-e8f2-537e-4f6c-d104768a1214"

# Audio settings
SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2
DURATION = 10
RECORD_DIR = "records"
RSSI_THRESHOLD = -150

if not os.path.exists(RECORD_DIR):
    os.makedirs(RECORD_DIR)

audio_frames = []

class FrameProcessor:
    def __init__(self, sample_rate, channels):
        self.opus_decoder = opuslib.Decoder(sample_rate, channels)
        self.last_packet_index = -1
        self.last_frame_id = -1
        self.pending = bytearray()
        self.lost = 0

    def store_frame_packet(self, data):
        index = data[0] + (data[1] << 8)
        internal = data[2]
        content = data[3:]

        if self.last_packet_index == -1 and internal == 0:
            self.last_packet_index = index
            self.last_frame_id = internal
            self.pending = content
            return

        if self.last_packet_index == -1:
            return

        if index != self.last_packet_index + 1 or (
            internal != 0 and internal != self.last_frame_id + 1
        ):
            print("Lost frame")
            self.last_packet_index = -1
            self.pending = bytearray()
            self.lost += 1
            return

        if internal == 0:
            audio_frames.append(self.pending)
            self.pending = content
            self.last_frame_id = internal
            self.last_packet_index = index
            return

        self.pending.extend(content)
        self.last_frame_id = internal
        self.last_packet_index = index

    def decode_frames(self):
        pcm_data = bytearray()
        frame_size = 960
        for frame in audio_frames:
            try:
                decoded_frame = self.opus_decoder.decode(bytes(frame), frame_size)
                pcm_data.extend(decoded_frame)
            except Exception as e:
                print(f"Error decoding frame: {e}")
        return pcm_data

frame_processor = FrameProcessor(SAMPLE_RATE, CHANNELS)

async def find_device_by_name(name=DEVICE_NAME):
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name and name.lower() in device.name.lower():
            if device.name.strip():
                print(f"Name: {device.name}, Address: {device.address}, RSSI: {device.rssi}")
                return device
    return None

async def connect_to_device(device):
    def disconnect_handler(client):
        print("Device disconnected")
        asyncio.get_event_loop().stop()

    async with BleakClient(device, disconnected_callback=disconnect_handler) as client:
        print(f"Connected: {client.is_connected}")

        def audio_data_handler(sender, data):
            frame_processor.store_frame_packet(data)

        await client.start_notify(AUDIO_DATA_STREAM_UUID, audio_data_handler)

        try:
            while stop_process != 1:
                print("Listening for audio data...")
                await asyncio.sleep(DURATION)
                pcm_data = frame_processor.decode_frames()
                frame_processor.pending = bytearray()
                del audio_frames[:]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_file = os.path.join(RECORD_DIR, f"{timestamp}.wav")
                with wave.open(audio_file, "wb") as wf:
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(SAMPLE_WIDTH)
                    wf.setframerate(SAMPLE_RATE)
                    wf.writeframes(pcm_data)
                print(f"Audio data saved to {audio_file}")
        except asyncio.CancelledError:
            print("Recording stopped")
        finally:
            print("Stopping notification and disconnecting...")
            await client.stop_notify(AUDIO_DATA_STREAM_UUID)
            print("Disconnected successfully")

def start_recording():
    global stop_process
    stop_process = 0

    async def handle_start():
        device = await find_device_by_name()
        if device is None:
            print("Device not found")
            return
        rssi = device.rssi
        if rssi < RSSI_THRESHOLD:
            print("Signal too weak")
            return
        await connect_to_device(device)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(handle_start())

@app.route('/start', methods=['POST'])
def start():
    global recording_thread
    if recording_thread and recording_thread.is_alive():
        return jsonify({"status": "already recording"})
    recording_thread = threading.Thread(target=start_recording)
    recording_thread.start()
    return jsonify({"status": "recording started"})

@app.route('/stop', methods=['POST'])
def stop():
    global stop_process
    stop_process = 1
    return jsonify({"message": "Process stopped", "stop_process": stop_process})

@app.route('/rssi', methods=['GET'])
def get_rssi():
    async def scan_rssi():
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name and DEVICE_NAME.lower() in device.name.lower():
                return {"name": device.name, "rssi": device.rssi}
        return {"error": "Device not found", "rssi": None}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(scan_rssi())
    return jsonify(result)

def run_flask():
    app.run(port=5005)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()