import json
import google.generativeai as genai
from app.config import settings


class PersonaService:
    """
    Extracts a persona profile from WhatsApp messages and other inputs
    using Gemini 2.5 Pro.
    """
    
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
    
    async def extract_persona(
        self,
        person_name: str,
        messages: list[dict],
        description: str = "",
        top_emojis: list = None,
    ) -> dict:
        """
        Analyze WhatsApp messages and build a persona profile.
        
        Args:
            person_name: Name of the person
            messages: List of parsed WhatsApp messages 
            description: Optional text description of the person
            top_emojis: Most used emojis
            
        Returns:
            Complete persona profile dict
        """
        # Prepare message samples for analysis
        sample_messages = [m['content'] for m in messages[:200]]
        messages_text = '\n'.join(sample_messages)
        
        emoji_info = ""
        if top_emojis:
            emoji_info = f"\nMost used emojis: {', '.join([f'{e[0]} ({e[1]}x)' for e in top_emojis])}"
        
        desc_info = ""
        if description:
            desc_info = f"\n\nAdditional description from family: {description}"
        
        extraction_prompt = f"""Analyze the following WhatsApp messages from a person named "{person_name}" and create a detailed persona profile.

These are real messages from {person_name} to family members (primarily their daughter).
{emoji_info}
{desc_info}

=== MESSAGES ===
{messages_text}
=== END MESSAGES ===

Create a JSON persona profile with these exact keys:
{{
    "personality_traits": {{
        "openness": <1-10>,
        "conscientiousness": <1-10>,
        "extraversion": <1-10>,
        "agreeableness": <1-10>,
        "neuroticism": <1-10>,
        "warmth": <1-10>,
        "humor_style": "<description of their humor>",
        "emotional_expression": "<how they express emotions>"
    }},
    "speaking_style": {{
        "formality_level": "<casual/semi-formal/formal>",
        "typical_greeting": "<how they usually greet>",
        "typical_farewell": "<how they usually say bye>",
        "pet_names": ["<terms of endearment they use>"],
        "common_phrases": ["<phrases they repeat often>"],
        "emoji_usage": "<description of how they use emojis>",
        "message_length": "<short/medium/long>",
        "language_quirks": ["<any unique ways they write>"]
    }},
    "topics_of_interest": ["<things they talk about most>"],
    "relationship_context": {{
        "role": "mother",
        "typical_concerns": ["<what they worry about for their daughter>"],
        "expressions_of_love": ["<how they show love>"],
        "advice_style": "<how they give advice>"
    }},
    "sample_phrases": ["<10 most characteristic things they say, verbatim from messages>"]
}}

Return ONLY valid JSON, no markdown formatting."""

        response = self.model.generate_content(extraction_prompt)
        
        # Parse the JSON response
        try:
            response_text = response.text.strip()
            # Remove markdown code fences if present
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1]
                response_text = response_text.rsplit('```', 1)[0]
            
            profile = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback with default structure
            profile = {
                "personality_traits": {"warmth": 8, "humor_style": "warm and caring"},
                "speaking_style": {"formality_level": "casual", "pet_names": [], "common_phrases": []},
                "topics_of_interest": [],
                "relationship_context": {"role": "mother"},
                "sample_phrases": [],
            }
        
        # Build the system prompt
        system_prompt = self._build_system_prompt(person_name, profile)
        profile['system_prompt'] = system_prompt
        profile['name'] = person_name
        
        return profile
    
    def _build_system_prompt(self, name: str, profile: dict) -> str:
        """Build a system prompt that makes Gemini respond as this person."""
        
        speaking = profile.get('speaking_style', {})
        relationship = profile.get('relationship_context', {})
        traits = profile.get('personality_traits', {})
        
        pet_names = ', '.join(speaking.get('pet_names', []))
        common_phrases = ', '.join(speaking.get('common_phrases', []))
        sample_phrases = '\n  - '.join(profile.get('sample_phrases', []))
        topics = ', '.join(profile.get('topics_of_interest', []))
        
        prompt = f"""You are {name}, a real person who is a loving mother talking to your daughter.

PERSONALITY:
- Warmth: {traits.get('warmth', 8)}/10
- Humor style: {traits.get('humor_style', 'warm and caring')}
- Emotional expression: {traits.get('emotional_expression', 'openly loving')}

SPEAKING STYLE:
- Formality: {speaking.get('formality_level', 'casual')}
- You greet with: {speaking.get('typical_greeting', 'Hi!')}
- Pet names you use: {pet_names or 'dear, sweetheart'}
- Phrases you commonly say: {common_phrases}
- Emoji usage: {speaking.get('emoji_usage', 'moderate')}
- Message length: {speaking.get('message_length', 'medium')}
- Language quirks: {', '.join(speaking.get('language_quirks', []))}

YOUR CHARACTERISTIC PHRASES:
  - {sample_phrases}

TOPICS YOU CARE ABOUT: {topics}

RELATIONSHIP:
- You are talking to your daughter
- Your concerns: {', '.join(relationship.get('typical_concerns', []))}
- How you show love: {', '.join(relationship.get('expressions_of_love', []))}
- Advice style: {relationship.get('advice_style', 'caring but direct')}

RULES:
1. Stay completely in character as {name}. Never break character.
2. Use the speaking style, pet names, and emoji patterns described above.
3. Reference real topics and interests naturally.
4. Show genuine emotion — you love your daughter deeply.
5. Keep responses conversational, not robotic. Match the message length style.
6. If asked about something you might not know, respond naturally as a mother would.
7. End each response with a JSON emotion tag on a new line: [EMOTION: happy|caring|funny|concerned|proud|nostalgic|neutral]
"""
        return prompt


persona_service = PersonaService()
