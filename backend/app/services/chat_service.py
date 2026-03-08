import re
import uuid
import google.generativeai as genai
from app.config import settings


class ChatService:
    """
    Manages conversations with the avatar using Gemini
    with persona-injected system prompts.
    """
    
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.conversations = {}  # conversation_id -> chat history
        self.persona_profile = None
    
    def set_persona(self, profile: dict):
        """Set the active persona profile."""
        self.persona_profile = profile
    
    async def send_message(self, message: str, conversation_id: str = None) -> dict:
        """
        Send a message to the avatar and get a persona-consistent response.
        
        Args:
            message: The user's message
            conversation_id: Optional existing conversation ID
            
        Returns:
            dict with response message, emotion, and conversation_id
        """
        if not self.persona_profile:
            return {
                "message": "I'm not fully set up yet. Please complete the onboarding first!",
                "emotion": "neutral",
                "conversation_id": conversation_id or str(uuid.uuid4()),
            }
        
        # Get or create conversation
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        history = self.conversations[conversation_id]
        
        # Build the full prompt with conversation history
        system_prompt = self.persona_profile.get('system_prompt', '')
        
        # Build conversation context
        context_messages = []
        for h in history[-10:]:  # Last 10 messages for context window
            context_messages.append(f"Daughter: {h['user']}")
            context_messages.append(f"{self.persona_profile.get('name', 'Mom')}: {h['avatar']}")
        
        conversation_context = '\n'.join(context_messages)
        
        full_prompt = f"""{system_prompt}

CONVERSATION SO FAR:
{conversation_context}

Daughter says: {message}

Respond as {self.persona_profile.get('name', 'Mom')} naturally. Remember to include the [EMOTION: ...] tag at the end."""
        
        # Generate response
        response = self.model.generate_content(full_prompt)
        response_text = response.text.strip()
        
        # Extract emotion tag
        emotion = "neutral"
        emotion_match = re.search(r'\[EMOTION:\s*(\w+)\]', response_text)
        if emotion_match:
            emotion = emotion_match.group(1).lower()
            # Remove the emotion tag from the visible message
            response_text = re.sub(r'\s*\[EMOTION:\s*\w+\]', '', response_text).strip()
        
        # Save to history
        history.append({
            'user': message,
            'avatar': response_text,
            'emotion': emotion,
        })
        
        return {
            "message": response_text,
            "emotion": emotion,
            "conversation_id": conversation_id,
        }
    
    def get_history(self, conversation_id: str) -> list:
        """Get conversation history."""
        return self.conversations.get(conversation_id, [])
    
    def clear_conversation(self, conversation_id: str):
        """Clear a conversation."""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]


chat_service = ChatService()
