from faster_whisper import WhisperModel
from typing import BinaryIO

def get_transcription(model: WhisperModel, audio_file: BinaryIO) -> str:
    
    segments,info = model.transcribe(audio_file, language="es")
    transcription = " ".join(segment.text for segment in segments)
    return transcription