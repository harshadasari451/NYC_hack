from fastapi import APIRouter, HTTPException
from app.models.schemas import PersonaInput
from app.services.whatsapp_parser import WhatsAppParser
from app.services.persona_service import persona_service
from app.services.chat_service import chat_service
from app.config import settings

router = APIRouter()

# In-memory persona storage (will be replaced with Firestore)
current_persona = {}


@router.post("/create")
async def create_persona(input_data: PersonaInput):
    """
    Create a persona profile from uploaded WhatsApp data + description.
    
    Assumes WhatsApp file has already been uploaded via /api/upload/whatsapp.
    """
    global current_persona
    
    # Find uploaded WhatsApp file
    whatsapp_dir = settings.UPLOAD_DIR / "whatsapp"
    txt_files = list(whatsapp_dir.glob("*.txt"))
    
    if not txt_files:
        raise HTTPException(status_code=400, detail="No WhatsApp export file found. Upload one first.")
    
    # Parse the most recent WhatsApp file
    latest_file = max(txt_files, key=lambda f: f.stat().st_mtime)
    with open(latest_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = WhatsAppParser(input_data.person_name)
    parsed = parser.parse(content)
    
    if parsed['target_messages'] == 0:
        raise HTTPException(
            status_code=400,
            detail=f"No messages found from '{input_data.person_name}'. "
                   f"Available senders: {', '.join(parsed['all_senders'])}"
        )
    
    # Extract persona using Gemini
    profile = await persona_service.extract_persona(
        person_name=input_data.person_name,
        messages=parsed['messages'],
        description=input_data.description or "",
        top_emojis=parsed['top_emojis'],
    )
    
    current_persona = profile
    
    # Set persona on chat service
    chat_service.set_persona(profile)
    
    return {
        "status": "success",
        "persona": {
            "name": profile.get('name'),
            "personality_traits": profile.get('personality_traits'),
            "speaking_style": profile.get('speaking_style'),
            "topics_of_interest": profile.get('topics_of_interest'),
            "sample_phrases": profile.get('sample_phrases'),
        },
        "stats": {
            "total_messages_parsed": parsed['total_messages'],
            "target_person_messages": parsed['target_messages'],
            "top_emojis": parsed['top_emojis'],
        },
    }


@router.get("/current")
async def get_current_persona():
    """Get the current active persona profile."""
    if not current_persona:
        raise HTTPException(status_code=404, detail="No persona created yet")
    
    return {
        "name": current_persona.get('name'),
        "personality_traits": current_persona.get('personality_traits'),
        "speaking_style": current_persona.get('speaking_style'),
        "topics_of_interest": current_persona.get('topics_of_interest'),
        "sample_phrases": current_persona.get('sample_phrases'),
    }
