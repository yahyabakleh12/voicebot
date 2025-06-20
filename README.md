# Voicebot

This repository provides a simple FastAPI application that processes audio recordings using OpenAI Whisper and GPT models. The response is returned as synthesized speech. It now supports longer conversations by maintaining history for each browser session.

## Prerequisites

- **Python 3.9+**
- An [OpenAI API key](https://platform.openai.com/).

## Installation

Install the required dependencies in a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Launching the Server

Set your OpenAI API key in `voicebot.py` or export it as an environment variable before launching.

Run the FastAPI server with Uvicorn:

```bash
uvicorn voicebot:app --reload
```

The API will be available at `http://127.0.0.1:8000/voicebot/<conversation_id>` where `<conversation_id>` is any identifier you choose (the demo page generates one automatically).

## Using the Voice Bot

Open `index.html` in a web browser. Press **Record** to start capturing audio and **Stop** to finish. Each browser session is assigned a conversation ID so you can have a longer exchange with the bot. After you stop recording, the page sends the audio to the FastAPI server and plays back the generated response while showing the transcript history.

Ensure the browser loads `index.html` from the same origin as the API (you can serve it with a simple HTTP server such as `python3 -m http.server`).

