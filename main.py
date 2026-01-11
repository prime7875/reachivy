from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi import File, UploadFile
from openai import OpenAI
import io,os,asyncio
from dotenv import load_dotenv
load_dotenv()
from prompts import SYSTEM_PROMPT,ORIENTATION_PROMPT,NOTE_PROMPT,REPORT_PROMPT
from starlette.middleware.sessions import SessionMiddleware
from user_flow import voice_to_text, save_user_response
from ai_flow import (
    generate_next_ai_question,
    text_to_speech,
    save_ai_message
)
from note_flow import generate_notes, save_notes
from report import generate_career_report, save_report

app = FastAPI()
client  = OpenAI(api_key=os.getenv("openai_key"))

## initialize session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY","dev-secret"),
    max_age = 1800
)

orientation_lock = asyncio.Lock()

@app.get("/orientation")
async def orientation(request:Request):
    async with orientation_lock:
        print("[LOCK] Orientation request acquired")
        
        ## init the session chat
        request.session.setdefault("chat",[])
        
        ## idempotency guard
        if request.session.get("orientation_done"):
            print("[REPLAY] Orientation already done")

            last_question = request.session["chat"][-1]["content"]

            audio = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",
                input=last_question
            )

            return StreamingResponse(
                io.BytesIO(audio.read()),
                media_type="audio/mpeg"
            )
        # generate orientation message
        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": ORIENTATION_PROMPT}
            ],
        )
        
        question_text = chat.choices[0].message.content
        print("[LOG]GENRATED ORIENTATION QUESTION:", question_text)
        
        ## save to session
        request.session['chat'].append(
            {
                'role':'assistant',
                'content':question_text
            }
        )
        print("[LOG]SAVED ORIENTATION QUESTION TO SESSION")
        print(f"\n\nTRIAL:\n\n{request.session['chat']}")
        ## mark orientation as done
        request.session['orientation_done'] = True
        
        
        # convert text to speech
        audio = client.audio.speech.create(
            model = "gpt-4o-mini-tts",
            voice = "alloy",
            input = question_text
        )
        print("[LOG]GENERATED ORIENTATION AUDIO")
        audio_bytes = io.BytesIO(audio.read())
        
        # return audio only
        
        return StreamingResponse(
            audio_bytes,
            media_type="audio/mpeg"
        )
        

@app.post("/user_response")
async def user_response(
    request:Request,
    audio: UploadFile = File(...)
):
    audio_bytes = await audio.read()
    
    user_text = voice_to_text(audio_bytes)
    print("[USER SAID]: ", user_text)
    save_user_response(request.session,user_text)
    
    return {"status":"success","user_text":user_text}

@app.post("/ai_flow")
async def ai_flow(request:Request):
    chat_history = request.session.get("chat")
    
    if not chat_history:
        return {"error":"No chat history found"}
    
    ## genrate next ai question
    ai_text = generate_next_ai_question(
        chat_history=chat_history,
        system_prompt=SYSTEM_PROMPT
    )
    print("[AI GENERATED]: ", ai_text)
    
    ## svae ai message to session
    save_ai_message(request.sesssion,ai_text)
    print("[AI MESSAGE SAVED TO SESSION]")
    
    ## convert to voice
    audio_bytes = text_to_speech(ai_text)
    
    ## return audio response
    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg"
    )
    
@app.post("/notes")
async def generate_note_api(request:Request):
    chat_history = request.session.get("chat")
    
    if not chat_history:
        return {"error":"No chat history found"}
    
    # generate notes
    notes = generate_notes(
        chat_history=chat_history,
        system_prompt=NOTE_PROMPT
    )
    
    ## save notes to session
    save_notes(request.session,notes)
    print("[NOTES SAVED TO SESSION]")
    
    return {
        "status":"generated",
        "notes":notes
    }
    
@app.post("/generate_report")
async def generate_report(request:Request):
    chat_history = request.session.get("chat")
    
    if not chat_history:
        return {"error":"No chat history found"}
    
    ## generate report
    report = generate_career_report(
        chat_history=chat_history,
        system_prompt=REPORT_PROMPT
    )
    
    ## save report to session
    save_report(request.session,report)
    print("[REPORT SAVED TO SESSION]")
    
    return {
        "status":"success",
        "report":report
    }