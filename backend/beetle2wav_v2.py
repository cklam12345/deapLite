import sounddevice as sd
import numpy as np
import wave
import time
import os
import threading
import queue
import argparse
import signal
import sys

def capture_audio(duration=10, output_dir="records", device_name="CABLE Output (VB-Audio Virtual Cable)", record_doa=True):
    """
    Captures audio and optionally DOA data from the specified device in chunks of 10 seconds.

    Args:
        duration (int): Duration of each recording chunk in seconds.
        output_dir (str): Directory to save the captured data.
        device_name (str): The name of the audio device.
        record_doa (bool): Whether to record DOA data (channel 2).
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        device_info = None
        devices = sd.query_devices()
        for device in devices:
            if device_name in device['name']:
                device_info = device
                break

        if device_info is None:
            print(f"Error: Device '{device_name}' not found.")
            return

        device_index = device_info['index']
        #samplerate = int(device_info['default_samplerate'])
        samplerate = 16000
        channels = 2 if record_doa else 1  # Adjust channels based on DOA recording

        audio_queue = queue.Queue()
        stop_event = threading.Event()

        def audio_callback(indata, frames, time, status):
            if status:
                print(status)
            audio_queue.put(indata.copy())

        def save_data():
            audio_data_all = []
            doa_data_all = []
            start_time = time.time()
            while time.time() - start_time < duration and not stop_event.is_set():
                try:
                    data = audio_queue.get(timeout=0.1)
                    audio_data_all.append(data)
                    if record_doa:
                        doa_data_all.append(data[:, 1])  # Extract channel 2 for DOA
                except queue.Empty:
                    pass

            audio_data_all = np.concatenate(audio_data_all, axis=0)
            if record_doa:
                doa_data_all = np.concatenate(doa_data_all, axis=0)

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            audio_filename = os.path.join(output_dir, f"audio_{timestamp}.wav")
            if record_doa:
                doa_filename = os.path.join(output_dir, f"doa_{timestamp}.txt")

            with wave.open(audio_filename, 'wb') as wf:
                wf.setnchannels(1)  # save only channel 1
                wf.setsampwidth(2)  # Assuming 16-bit audio
                wf.setframerate(samplerate)
                wf.writeframes((audio_data_all[:, 0] * 32767).astype(np.int16).tobytes())

            print(f"Saved audio to {audio_filename}")
            if record_doa:
                with open(doa_filename, 'w') as f:
                    for doa_value in doa_data_all:
                        f.write(f"{doa_value}\n")
                print(f"Saved DOA to {doa_filename}")

        while True:  # Run in a loop
            save_thread = threading.Thread(target=save_data)
            save_thread.start()

            with sd.InputStream(device=device_index, samplerate=samplerate, channels=channels, callback=audio_callback):
                time.sleep(duration)  # Let the recording run for the duration.
                stop_event.set()  # Signal save thread to stop.
                save_thread.join()  # Wait for save thread to finish.

            stop_event.clear() #reset stop event.

    except Exception as e:
        print(f"An error occurred: {e}")

def signal_handler(sig, frame):
    print("Stopping recording...")
    sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture audio and optionally DOA data.")
    parser.add_argument("--duration", type=int, default=10, help="Duration of each recording chunk in seconds.")
    parser.add_argument("--output_dir", type=str, default="records", help="Directory to save the captured data.")
    parser.add_argument("--device_name", type=str, default="CABLE Output (VB-Audio Virtual Cable)", help="The name of the audio device.")
    parser.add_argument("--no-doa", action="store_true", help="Disable DOA recording.")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler) #handle ctrl+c
    signal.signal(signal.SIGTERM, signal_handler) #handle taskkill

    capture_audio(duration=args.duration, output_dir=args.output_dir, device_name=args.device_name, record_doa=not args.no_doa)