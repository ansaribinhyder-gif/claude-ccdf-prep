import os
import sys

import anthropic

MODEL = os.getenv("CLAUDE_MODEL")

def get_client(**kwargs) -> anthropic.Anthropic:
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("Set your key first: export ANTHROPIC_API_KEY = 'sk-ant-..' (never hardcode it)")
    return anthropic.Anthropic(**kwargs)

def banner(title) -> None:
    print(f"\n{'=' *8} {title} {'=' *8}")