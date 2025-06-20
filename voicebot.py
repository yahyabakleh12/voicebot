from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import openai
import whisper
import os
import tempfile

app = FastAPI()

openai.api_key = "YOUR_OPENAI_API_KEY"
whisper_model = whisper.load_model("base")

@app.post("/voicebot")
async def voicebot(audio: UploadFile = File(...)):
    # Save the audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(await audio.read())
        audio_filepath = tmp.name

    # Transcribe audio to text using Whisper
    transcription = whisper_model.transcribe(audio_filepath)
    user_message = transcription["text"]
    
    # Remove temporary file
    os.unlink(audio_filepath)

    # Generate response using OpenAI GPT
    system_prompt = "You are Parkonic's helpful assistant bot."
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    bot_response_text = completion.choices[0].message.content

    # Convert response text to speech using OpenAI TTS
    tts_response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=bot_response_text
    )

    audio_response_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    audio_response_file.write(tts_response.content)
    audio_response_file.seek(0)

    return StreamingResponse(open(audio_response_file.name, "rb"), media_type="audio/mpeg")
