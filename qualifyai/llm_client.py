"""LLM Client for OpenAI API calls."""

import os
import yaml
from openai import AsyncOpenAI

# Get absolute path to config (works from any directory)
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_THIS_DIR)
CONFIG_PATH = os.path.join(_PROJECT_ROOT, "cfg", "config.yml")

def load_config():
    """Load configuration from config.yml."""
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def get_llm_client():
    """configured OpenAI async client"""
    config = load_config()
    return AsyncOpenAI(api_key=config["openai_api_key"])

async def call_llm(prompt: str, system_prompt: str = None) -> str:
    """Make an async call to the LLM and return the response text."""
    client = get_llm_client()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.1,
        max_tokens=1000
    )

    return response.choices[0].message.content
