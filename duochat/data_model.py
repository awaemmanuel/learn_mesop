""" Data Model for DuoChat """
from dataclasses import dataclass, field
from typing import Literal
from enum import Enum

import mesop as me 

Role = Literal["user", "model"]

@dataclass(kw_only=True)
class ChatMessage:
    """Class to represent a chat message."""
    role: Role = "user"
    content: str = ""
    in_progress: bool = False

class Models(Enum):
    """Enum to represent the models used in the chat."""
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_1_5_PRO = "gemini-1.5-pro"

@dataclass
class Conversation:
    """Class to represent a conversation."""
    model: str = ""
    messages: list[ChatMessage] = field(default_factory=list)

@me.stateclass
class State:
    """State class to handle model picking and conversation."""
    is_model_picker_dialog_open: bool = False
    input: str = ""
    conversations: list[Conversation] = field(default_factory=list)
    models: list[str] = field(default_factory=list)
    gemini_api_key: str = ""
    claude_api_key: str = ""

@me.stateclass
class ModelDialogState:
    """State class to handle model picker dialog."""
    selected_models: list[str] = field(default_factory=list)