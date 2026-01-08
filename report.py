from openai import OpenAI
from prompts import REPORT_PROMPT
import os

client = OpenAI(api_key="OPEN AI API KEY HERE")

def generate_report(transcript):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": REPORT_PROMPT},
            {"role": "user", "content": "\n".join(transcript)}
        ]
    )
    return response.choices[0].message.content
