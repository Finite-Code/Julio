#from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import random  # For generating responses without OpenAI
import speech_recognition as sr  # For wake word detection

# Initialize FastAPI app
app = FastAPI()

# Define request model
class JulioRequest(BaseModel):
    command: str  # Command to execute (e.g., "open YouTube")

# Simple local AI responses (since OpenAI is not used)
def local_ai_response(command):
    responses = {
        "who are you": "I am Julio, your AI assistant!",
        "tell me a joke": random.choice([
            "Why don’t skeletons fight each other? Because they don’t have the guts!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don’t some couples go to the gym? Because some relationships don’t work out!"
        ]),
    }
    return responses.get(command, f"I don't understand '{command}' yet.")

@app.post("/julio")
async def julio_action(request: JulioRequest):
    """Handles user requests and executes actions."""
    command = request.command.lower()
    return {"response": local_ai_response(command)}

# Wake-word detection (runs locally)
def wake_word_listener():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    wake_word = "julio"
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for wake word...")
        
        while True:
            try:
                audio = recognizer.listen(source)
                transcript = recognizer.recognize_google(audio).lower()
                if wake_word in transcript:
                    print("Wake word detected! Julio is ready.")
                    return
            except sr.UnknownValueError:
                continue  # Ignore unrecognized speech
            except sr.RequestError:
                print("Speech recognition service error.")
                break

# Run the server locally for testing
if __name__ == "__main__":
    import uvicorn
    from threading import Thread
    
    # Start wake word detection in a separate thread
    wake_thread = Thread(target=wake_word_listener, daemon=True)
    wake_thread.start()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
