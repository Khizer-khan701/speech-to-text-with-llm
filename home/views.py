import os
from django.shortcuts import render
from .utils.transcriber import transcribe_audio
from .utils.cleaner import clean_text
from .utils.categorizer import predict_category
from pydub import AudioSegment  # for converting MPEG to MP3

# Folder to save uploaded files
UPLOAD_DIR = "audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = ('.mp3', '.wav', '.m4a', '.mpeg')

def upload_audio(request):
    context = {}

    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]
        file_name = audio_file.name.lower()

        # Validate file type
        if not file_name.endswith(ALLOWED_EXTENSIONS):
            context["error"] = "Only MP3, WAV, M4A, MPEG files are allowed."
            return render(request, "upload.html", context)

        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, audio_file.name)
        with open(file_path, "wb+") as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        # Convert MPEG to MP3 if needed
        if file_name.endswith(".mpeg"):
            mp3_path = file_path.rsplit('.', 1)[0] + ".mp3"
            sound = AudioSegment.from_file(file_path)
            sound.export(mp3_path, format="mp3")
            file_path = mp3_path  # use converted file for transcription

        # 1️⃣ Transcribe audio
        transcript = transcribe_audio(file_path, output_path=None)

        # 2️⃣ Clean the text
        cleaned = clean_text(transcript)

        # 3️⃣ Predict categories via LLM
        categories = predict_category(cleaned)

        # Pass results to template
        context.update({
            "file_name": audio_file.name,
            "transcript": transcript,
            "cleaned": cleaned,
            "categories": categories
        })

    return render(request, "upload.html", context)
