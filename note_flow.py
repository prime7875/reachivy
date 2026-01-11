from openai import OpenAI

client = OpenAI(api_key="openai_key")

def generate_notes(chat_history:list,system_prompt:str) -> str:
    """
    Generate concise notes from the conversation
    """
    messages = [
        {"role":"system","content": system_prompt},
        *chat_history
    ]
    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages
    )
    return completion.choices[0].message.content

def save_notes(session:dict,notes:str):
    session['notes'] = notes

