import whisper

# Load Whisper model once
model = whisper.load_model("base")

def transcribe_audio(audio_path, output_path=None):
    """
    Transcribes audio file to text using Whisper.
    """
    result = model.transcribe(audio_path)
    transcript = result["text"]

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript)

    return transcript
