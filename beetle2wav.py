import sounddevice as sd
import numpy as np
import wave
import time
import os
import threading
import queue

def capture_audio_and_doa(duration=10, output_dir="captured_data", device_name="Stereo Mix (Realtek(R) Audio)"):
    """
    Captures audio from the Soundskrit Demo Kit (channels 1 and 2) and saves the raw audio (channel 1)
    and DOA data (channel 2) to separate files.

    Args:
        duration (int): Duration of the recording in seconds.
        output_dir (str): Directory to save the captured data.
        device_name (str): The name of the Soundskrit Demo Kit device.
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
        samplerate = int(device_info['default_samplerate'])
        channels = 2  # Soundskrit demo kit has 2 channels

        audio_queue = queue.Queue()
        doa_queue = queue.Queue()
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
                    doa_data_all.append(data[:, 1]) # Extract channel 2 for DOA
                except queue.Empty:
                    pass

            audio_data_all = np.concatenate(audio_data_all, axis=0)
            doa_data_all = np.concatenate(doa_data_all, axis=0)

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            audio_filename = os.path.join(output_dir, f"audio_{timestamp}.wav")
            doa_filename = os.path.join(output_dir, f"doa_{timestamp}.txt")

            with wave.open(audio_filename, 'wb') as wf:
                wf.setnchannels(1)  # save only channel 1
                wf.setsampwidth(2)  # Assuming 16-bit audio
                wf.setframerate(samplerate)
                wf.writeframes((audio_data_all[:, 0] * 32767).astype(np.int16).tobytes())

            with open(doa_filename, 'w') as f:
                for doa_value in doa_data_all:
                    f.write(f"{doa_value}\n")

            print(f"Saved audio to {audio_filename}")
            print(f"Saved DOA to {doa_filename}")

        save_thread = threading.Thread(target=save_data)
        save_thread.start()

        with sd.InputStream(device=device_index, samplerate=samplerate, channels=channels, callback=audio_callback):
            time.sleep(duration) #let the recording run for the duration.
            stop_event.set() #signal save thread to stop.
            save_thread.join() #wait for save thread to finish.

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    capture_audio_and_doa(duration=10) #change duration as needed.
