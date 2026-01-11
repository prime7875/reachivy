from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
import assemblyai as aai


aai.settings.api_key = os.getenv("ass_api")

async def voice_to_text(audio_bytes: bytes) -> str:
    """
    convert users voice to text
    """
    transcriber = aai.Transcriber()
    
    transcript = transcriber.transcribe(audio_bytes)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(transcript.error)
    
    return transcript.text

def save_user_response(session:dict,text:str):
    """
    Save user response to session
    """
    session.setdefault("chat",[])
    
    session["chat"].append(
        {"role":"user","content":text}
    )
    