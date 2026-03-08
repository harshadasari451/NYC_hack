from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter()


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message to the avatar and get a response."""
    result = await chat_service.send_message(
        message=request.message,
        conversation_id=request.conversation_id,
    )
    return ChatResponse(**result)


@router.get("/history/{conversation_id}")
async def get_history(conversation_id: str):
    """Get conversation history."""
    history = chat_service.get_history(conversation_id)
    return {"conversation_id": conversation_id, "messages": history}


@router.delete("/history/{conversation_id}")
async def clear_history(conversation_id: str):
    """Clear conversation history."""
    chat_service.clear_conversation(conversation_id)
    return {"status": "cleared", "conversation_id": conversation_id}
