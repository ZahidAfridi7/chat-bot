from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.services.voice import voice_processor
from app.schemas.voice import VoiceResponse
from app.db.models.user import User
from app.services.auth import get_current_user
from typing import Annotated
from app.services import ai_services

router = APIRouter()

@router.post("/process", response_model=VoiceResponse)
async def process_voice_input(
    current_user: Annotated[User, Depends(get_current_user)],
    audio_file: UploadFile = File(...)
):
    """Endpoint for processing voice messages"""
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(400, "Only audio files are accepted")
    
    audio_bytes = await audio_file.read()
    text, analysis = await voice_processor.process_audio(
        user=current_user,
        audio_bytes=audio_bytes,
        content_type=audio_file.content_type.split("/")[1]
    )
    
    # Generate response (connect to your AI service)
    ai_response = await ai_services.generate_voice_response(
        user=current_user,
        voice_analysis=analysis
    )
    
    return VoiceResponse(
        text_response=ai_response,
        emotion_adapted=True,
        voice_analysis=analysis
    )