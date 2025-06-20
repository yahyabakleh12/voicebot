from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import openai
import whisper
import os
import tempfile
import base64
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

openai.api_key = os.environ.get("OPENAI_API_KEY")
whisper_model = whisper.load_model("base")
conversations = {}

@app.post("/voicebot/{conversation_id}")
async def voicebot(conversation_id: str, audio: UploadFile = File(...)):
    # Save the audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(await audio.read())
        audio_filepath = tmp.name

    # Transcribe audio to text using Whisper
    transcription = whisper_model.transcribe(audio_filepath)
    user_message = transcription["text"]
    
    # Remove temporary file
    os.unlink(audio_filepath)

    # Prepare conversation history
    system_prompt = "You are Parkonic's helpful assistant bot."
    history = conversations.setdefault(conversation_id, [{"role": "system", "content": system_prompt}])
    history.append({"role": "user", "content": user_message})

    # Generate response using OpenAI GPT
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    bot_response_text = completion.choices[0].message.content
    history.append({"role": "assistant", "content": bot_response_text})

    # Convert response text to speech using OpenAI TTS
    tts_response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=bot_response_text
    )

    audio_response_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    audio_response_file.write(tts_response.content)
    audio_response_file.seek(0)

    audio_bytes = audio_response_file.read()
    encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")
    os.unlink(audio_response_file.name)

    return JSONResponse({"text": bot_response_text, "audio": encoded_audio, "user": user_message})
