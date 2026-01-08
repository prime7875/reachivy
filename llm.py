from openai import OpenAI
import json
import os
from prompts import SYSTEM_PROMPT

client = OpenAI(api_key="OPEN AI API KEY HERE")


def generate_question(conversation):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation
        ],
        temperature=0.5
    )
    return response.choices[0].message.content