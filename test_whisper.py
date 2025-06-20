import whisper
model = whisper.load_model("small")
print("✅ whisper loaded, model size:", model.device)