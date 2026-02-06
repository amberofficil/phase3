
"""
API endpoint for the AI Todo Assistant that processes natural language commands.
"""
from fastapi import APIRouter, HTTPException
from ..models.api_models import NaturalLanguageCommand, CommandResponse
from ..services.natural_language_processor import NaturalLanguageProcessor

router = APIRouter()

@router.post("/ai/todo/process", response_model=CommandResponse)
async def process_natural_language_command(command: NaturalLanguageCommand):
    try:
        # 🔍 DEBUG
        print("➡️ Received command:", command.dict())

        processor = NaturalLanguageProcessor()

        # ✅ FIX: await is REQUIRED
        result = await processor.process_command(
            user_input=command.user_input,
            user_id=command.user_id,
            conversation_context=command.conversation_context
        )

        print("✅ AI Result:", result)

        return CommandResponse(**result)

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Todo Assistant API"}
