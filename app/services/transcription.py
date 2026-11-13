from faster_whisper import WhisperModel
from typing import BinaryIO

def get_transcription(model: WhisperModel, audio_file: BinaryIO) -> str:
    """
    Transcribe an audio file using the Whisper model.

    Args:
        model (WhisperModel): The Whisper model instance.
        audio_file (BinaryIO): The audio file to transcribe.

    Returns:
        str: The transcribed text.
    """
    
    segments,info = model.transcribe(audio_file, language="es")
    transcription = " ".join(segment.text for segment in segments)
    return transcription