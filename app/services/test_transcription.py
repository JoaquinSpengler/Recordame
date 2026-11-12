from faster_whisper import WhisperModel
from pathlib import Path

model = WhisperModel("base", device="cpu", compute_type="int8")


audio_path = str(Path("5165635421203335591.ogg"))
segments, info = model.transcribe(audio_path, language="es")

print("Archivo leído:", Path(audio_path).resolve())

for segment in segments:
    print(segment.text)