from pydub import AudioSegment

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)  # Load MP3 file
    audio.export(wav_path, format="wav")     # Save as WAV file
    print(f"Converted {mp3_path} to {wav_path}")


if __name__ == "__main__" :
# Example: Convert an MP3 file
    convert_mp3_to_wav("/home/vishnu/projects/FakeVoiceDetect/sample-audios/pMgjwBgCZIw.mp3", "test_audio1.wav")