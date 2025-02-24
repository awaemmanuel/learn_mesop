"""Gemini module for handling Gemini API interactions and model selection."""

from typing import Iterable

import google.generativeai as genai

from data_model import ChatMessage, State
import mesop as me

generation_config = {
    "temperature": 1,
    "max_output_tokens": 8192,
    "top_k": 64,
    "top_p": 0.95,
}


def configure_gemini():
    """Configure the Gemini API key."""
    state = me.state(State)
    if state.gemini_api_key:
        genai.configure(api_key=state.gemini_api_key)
    else:
        raise ValueError(
            "Gemini API key is not set. Please set it in the model picker dialog."
        )


def send_prompt(
    prompt: str, history: list[ChatMessage], model: str = "gemini-2.0-flash"
) -> Iterable[str]:
    """Send a prompt to the Gemini API and yield the response."""
    configure_gemini()
    model = genai.GenerativeModel(
        model_name=model,
        generation_config=generation_config,
    )
    chat_session = model.start_chat(
        history=[
            {
                "role": message.role,
                "parts": [message.content],
            }
            for message in history
        ]
    )
    for chunk in chat_session.send_message(prompt, stream=True):
        yield chunk.text if chunk.text else ""
