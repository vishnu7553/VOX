import torch
import librosa
import numpy as np
from transformers import Wav2Vec2FeatureExtractor, AutoModelForAudioClassification

# Configuration
CHUNK_LENGTH_SEC = 5  # Adjust based on GPU memory (e.g., 3-10 seconds)
MODEL_NAME = "Heem2/Deepfake-audio-detection"

# Initialize model and processor
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME).to(device)

# --- Core Functions ---
def _process_audio_chunk(chunk):
    """Helper: Predict a single audio chunk."""
    inputs = processor(chunk, sampling_rate=16000, return_tensors="pt").to(device)
    with torch.no_grad():
        logits = model(**inputs).logits
    return torch.softmax(logits, dim=-1).cpu().numpy()[0]

def predict_audio_file(file_path):
    """
    Predict if a pre-recorded audio file is AI-generated or human.
    Args:
        file_path (str): Path to the audio file (WAV/MP3).
    Returns:
        dict: {
            "prediction": "AIVoice" or "HumanVoice",
            "ai_prob": float (0-1),
            "human_prob": float (0-1),
            "chunks_processed": int
        }
    """
    try:
        audio, _ = librosa.load(file_path, sr=16000)  # Resample to 16kHz
        chunk_size = int(16000 * CHUNK_LENGTH_SEC)
        chunks = [audio[i:i+chunk_size] for i in range(0, len(audio), chunk_size)]
        
        probs = np.array([_process_audio_chunk(chunk) for chunk in chunks])
        avg_probs = probs.mean(axis=0)

        return {
            "prediction": model.config.id2label[np.argmax(avg_probs)],
            "ai_prob": float(avg_probs[0]),
            "human_prob": float(avg_probs[1]),
            "chunks_processed": len(chunks)
        }
    except Exception as e:
        return {"error": str(e)}

def predict_realtime_audio(audio_stream, sample_rate=16000):
    """
    Predict real-time audio stream (e.g., from microphone).
    Args:
        audio_stream (np.ndarray): Raw audio data (1D array).
        sample_rate (int): Sample rate of the stream (default: 16000).
    Returns:
        dict: Same as `predict_audio_file()`.
    """
    try:
        if sample_rate != 16000:
            audio_stream = librosa.resample(audio_stream, orig_sr=sample_rate, target_sr=16000)
        
        chunk_size = int(16000 * CHUNK_LENGTH_SEC)
        chunks = [audio_stream[i:i+chunk_size] for i in range(0, len(audio_stream), chunk_size)]
        
        probs = np.array([_process_audio_chunk(chunk) for chunk in chunks])
        avg_probs = probs.mean(axis=0)

        return {
            "prediction": model.config.id2label[np.argmax(avg_probs)],
            "ai_prob": float(avg_probs[0]),
            "human_prob": float(avg_probs[1]),
            "chunks_processed": len(chunks)
        }
    except Exception as e:
        return {"error": str(e)}