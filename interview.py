from llm import generate_question
from speech import text_to_speech, speech_to_text
from state import add_turn

def ai_ask(state):
    question = generate_question(state["conversation"])
    add_turn(state, "assistant", question)
    audio = text_to_speech(question)
    return question, audio

def user_answer(audio_path):
    return speech_to_text(audio_path)

def start_interview(state):
    intro = (
    "Hi! I’m your AI career guide. "
    "We’ll have a short, relaxed voice conversation to explore what you enjoy and what might suit you in the future. "
    "There are no right or wrong answers—just be yourself. To start, what’s your name?"
    )
    add_turn(state, "assistant", intro)
    audio = text_to_speech(intro)
    state["started"] = True
    state["waiting_for_user"] = True
    return intro, audio