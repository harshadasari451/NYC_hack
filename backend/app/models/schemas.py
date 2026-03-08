from pydantic import BaseModel
from typing import Optional


class PersonaProfile(BaseModel):
    """The extracted persona profile from all input data."""
    name: str
    personality_traits: dict  # Big Five + custom traits
    speaking_style: dict  # vocabulary, slang, emoji patterns
    topics_of_interest: list[str]
    relationship_context: dict  # how she talks to daughter
    sample_phrases: list[str]  # characteristic things she says
    system_prompt: str  # constructed prompt for Gemini
    description: Optional[str] = None


class WhatsAppMessage(BaseModel):
    """A single parsed WhatsApp message."""
    timestamp: str
    sender: str
    content: str
    is_media: bool = False


class ChatMessage(BaseModel):
    """A message in the conversation with the avatar."""
    role: str  # "user" or "avatar"
    content: str
    emotion: Optional[str] = None  # happy, caring, funny, concerned, neutral
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    """Request to send a message to the avatar."""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response from the avatar."""
    message: str
    emotion: str
    conversation_id: str


class PersonaInput(BaseModel):
    """Manual inputs for persona creation."""
    person_name: str
    description: Optional[str] = None
