from openai import OpenAI

client = OpenAI(api_key="openai_key")

def generate_next_ai_question(chat_history:list,system_prompt:str) -> str:
    """
    Generate the next question using system prompt
    """
    messages = [
        {'role': 'system', 'content': system_prompt+"\nThis the chat history till now:\n"+chat_history}
    ]
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return completion.choices[0].message.content

def text_to_speech(text:str) -> bytes:
    """
    Convert text to speech using OpenAI TTS model
    """
    audio = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    return audio.read()

def save_ai_message(session:dict,message:str):
    session.setdefault("chat",[])
    session['chat'].append(
        {
            'role':'assistant',
            'content':message
        }
    )