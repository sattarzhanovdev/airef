# food/services/openai_client.py
import os
from openai import OpenAI

def get_openai_client():
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN environment variable is not set")

    return OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=token,
    )
