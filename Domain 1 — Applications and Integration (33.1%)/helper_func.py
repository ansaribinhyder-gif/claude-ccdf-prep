import os
import sys

import anthropic
from fastapi import FastAPI
from pydantic import BaseModel

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "1024"))
TEMPERATURE = float(os.getenv("CLAUDE_TEMPERATURE", "0.2"))

def get_client(**kwargs) -> anthropic.Anthropic:
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("Set your key first: export ANTHROPIC_API_KEY='sk-ant-..' (never hardcode it)")
    return anthropic.Anthropic(**kwargs)

def banner(title) -> None:
    print(f"\n{'=' * 8} {title} {'=' * 8}")

client = get_client()
app = FastAPI()

class ExtractRequest(BaseModel):
    text: str

@app.post("/extract")
def extract(text: ExtractRequest):
    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        # temperature=TEMPERATURE,
        messages=[{"role": "user", "content": text}],
    )
    return {"result": resp.content[0].text}