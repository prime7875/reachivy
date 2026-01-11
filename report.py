from openai import OpenAI

client = OpenAI(api_key='openai_key')

def generate_career_report(chat_history:list,system_prompt:str) -> str:
    """
    Generate career report based on chat discussion.
    """
    messages = [
        {'role':'system','content':system_prompt},
        *chat_history
    ]
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    
    return completion.choices[0].message.content

def save_report(session:dict,report:str):
    """
    Save generated report to session.
    """
    session['final_report'] = report