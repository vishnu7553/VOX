import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
import time

def start_recording(output_folder="recordings", sample_rate=16000):
    """Start recording and return the stream object"""
    os.makedirs(output_folder, exist_ok=True)
    
    # Initialize empty recording buffer
    recording = []
    
    def callback(indata, frames, time, status):
        recording.append(indata.copy())
    
    stream = sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        callback=callback,
        dtype='float32'
    )
    stream.start()
    return stream, recording

def stop_and_predict(stream, recording, sample_rate=16000, output_folder="recordings"):
    """Stop recording, save to file, and return prediction"""
    stream.stop()
    stream.close()
    
    if not recording:
        raise ValueError("No audio was recorded")
    
    # Combine all chunks and convert to proper format
    audio_data = np.concatenate(recording)
    audio_data = (audio_data * 32767).astype(np.int16)  # Convert to 16-bit PCM
    
    # Save recording
    timestamp = int(time.time())
    filename = f"recording_{timestamp}.wav"
    filepath = os.path.join(output_folder, filename)
    write(filepath, sample_rate, audio_data)
    
    return filepath