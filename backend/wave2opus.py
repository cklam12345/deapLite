import asyncio
import wave
import os
from datetime import datetime
from bleak import BleakClient, BleakScanner
import opuslib

from flask import Flask, request, jsonify
import threading
app = Flask(__name__)

# Initialize the flag
stop_process = 0
start_process = 0

@app.route('/stop', methods=['POST'])
def stop():
    global stop_process
    stop_process = 1
    return jsonify({"message": "Process stopped", "stop_process": stop_process})

@app.route('/start', methods=['POST'])
def start():
    global start_process
    start_process = 1
    return jsonify({"message": "Process started", "start_process": start_process})

def run_flask():
    app.run(port=5005)


# Device settings
DEVICE_NAME = "Friend"

# UUIDs from the Dart code 19B10000-E8F2-537E-4F6C-D104768A1214
# 
SERVICE_UUID = "19b10000-e8f2-537e-4f6c-d104768a1214"
#SERVICE_UUID = "19B10000-E8F2-537E-4F6C-D104768A1214"
AUDIO_DATA_STREAM_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
AUDIO_CODEC_UUID = "19b10002-e8f2-537e-4f6c-d104768a1214"

# Audio settings
SAMPLE_RATE = 16000  # Adjust as per your device's specifications
CHANNELS = 1  # Adjust as per your device's specifications
SAMPLE_WIDTH = 2  # Adjust as per your device's specifications
DURATION = 10  # Duration in seconds
RECORD_DIR = "records"

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
            audio_frames.append(self.pending)  # Save frame
            self.pending = content  # Start new frame
            self.last_frame_id = internal  # Update internal frame id
            self.last_packet_index = index  # Update packet id
            return

        self.pending.extend(content)
        self.last_frame_id = internal  # Update internal frame id
        self.last_packet_index = index  # Update packet id

    def decode_frames(self):
        pcm_data = bytearray()
        frame_size = 960  # Adjust frame size as per Opus settings (e.g., 960 for 20ms frames at 48kHz)

        for frame in audio_frames:
            try:
                decoded_frame = self.opus_decoder.decode(bytes(frame), frame_size)
                pcm_data.extend(decoded_frame)
            except Exception as e:
                print(f"Error decoding frame: {e}")
        return pcm_data


frame_processor = FrameProcessor(SAMPLE_RATE, CHANNELS)


async def find_device_by_name(name=DEVICE_NAME):
 #    devices = await bleak.discover(timeout=2.0)
 #    for device in devices:
 #       if device.name:
 #           print(device.name, device.address)
 #       if device.name == DEVICE_NAME:
 #           return device
 #    return None

    while True:
        devices = await BleakScanner.discover()

        if not devices:
            print("No Bluetooth devices found. Retrying...")
            await asyncio.sleep(5)  # Wait for 5 seconds before retrying
            continue

        print("Found devices:")
        for device in devices:
            if device.name and name.lower() in device.name.lower():
                if device.name.strip():  # Ensure the device name is not blank
                    print(f"Name: {device.name}, Address: {device.address}")
                    return device

        print(f"Device with name '{name}' not found. Retrying...")
        await asyncio.sleep(5)  # Wait for 5 seconds before retrying

#    devices = await BleakScanner.discover()
#    if not devices:
#        print("No Bluetooth devices found.")
#        return None

#    print("Found devices:")
#    for device in devices:
#        print(f"Name: {device.name}, Address: {device.address}")

#    for device in devices:
#        if name in device.name:
#            print(f"Name: {device.name}, Address: {device.address}")
#            return device
   # return None


async def connect_to_device(device):
    def disconnect_handler(client):
        print("Device disconnected")
        asyncio.get_event_loop().stop()

    async with BleakClient(device, disconnected_callback=disconnect_handler) as client:
        print(f"Connected: {client.is_connected}")

        def audio_data_handler(sender, data):
            frame_processor.store_frame_packet(data)

        # Start notification on the audio data stream characteristic
        await client.start_notify(AUDIO_DATA_STREAM_UUID, audio_data_handler)
        #fileCounter=0
        try:
            #while fileCounter!=5:
            #while True:
            while stop_process!=1:
                #fileCounter+=1
                print("Listening for audio data...")
                await asyncio.sleep(DURATION)
                # Decode the Opus data to PCM
                pcm_data = frame_processor.decode_frames()
                frame_processor.pending = bytearray()
                del audio_frames[:]

                # Save the PCM data to a WAV file with a timestamp
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


async def main():
    device = await find_device_by_name()
    if device is None:
        print("Device with the name 'Friend' not found.")
        return

    await connect_to_device(device)


if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    try:
        asyncio.run(main())
    except:
        print("Program interrupted by user, shutting down...")