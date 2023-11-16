#!/usr/bin/env -S poetry run python

from openai import OpenAI

OPENAI_API_KEY = "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"
client = OpenAI(api_key="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")

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)