from faster_whisper import WhisperModel
from pathlib import Path
from app.services.transcription import get_transcription


model = WhisperModel("small", device="cpu", compute_type="int8")

audio_path = Path(__file__).with_name("test.ogg")

with open(audio_path, "rb") as audio_file:
    print(get_transcription(model, audio_file))