import os
import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')  # Required for server-side rendering
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def generate_spectrogram(audio_path, output_dir, filename_prefix="spec"):
    """
    Generate and save spectrogram image from audio file
    
    Args:
        audio_path (str): Path to input audio file
        output_dir (str): Directory to save spectrogram image
        filename_prefix (str): Prefix for output filename
        
    Returns:
        str: Path to generated spectrogram image
    """
    try:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Load audio file
        y, sr = librosa.load(audio_path)
        
        # Set up figure with dark theme
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 4), facecolor='none')
        
        # Generate spectrogram
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=2048)), ref=np.max)
        img = librosa.display.specshow(D, y_axis='log', x_axis='time', 
                                     ax=ax, cmap='magma', sr=sr)
        
        # Customize appearance
        ax.set(title='', xlabel='', ylabel='')
        ax.grid(False)
        plt.tight_layout(pad=0)
        
        # Save spectrogram
        output_path = os.path.join(output_dir, f"{filename_prefix}_{os.path.basename(audio_path)}.png")
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=100, transparent=True)
        plt.close()
        
        return output_path
        
    except Exception as e:
        print(f"Spectrogram generation failed: {str(e)}")
        return None