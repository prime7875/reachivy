import assemblyai as aai
import uuid
import os
from openai import OpenAI
import sounddevice as sd
from scipy.io.wavfile import write

aai.settings.api_key = "ASSEMBLY AI API KEY HERE"
client = OpenAI(api_key="OPEN AI API KEY HERE")


def record_audio(duration=6, fs=44100):
    """
    Records audio from mic for `duration` seconds
    """
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    path = f"/tmp/{uuid.uuid4()}.wav"
    write(path, fs, recording)
    return path


def text_to_speech(text, path="output.mp3"):
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    ) as response:
        response.stream_to_file(path)

    return path

def speech_to_text(audio_path):
    return aai.Transcriber().transcribe(audio_path).text