from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.core.config import Settings
from app.core.security import require_api_key
from app.providers.base import VoiceProvider
from app.schemas import HealthResponse, TtsRequest, TtsResponse
from app.storage.base import AudioStorage


def build_router(
    *,
    settings: Settings,
    provider: VoiceProvider,
    storage: AudioStorage,
) -> APIRouter:
    router = APIRouter()

    @router.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(
            ok=True,
            service="sabi-voice-service",
            provider=provider.name,
            storage=storage.name,
        )

    @router.post(
        "/v1/tts",
        response_model=TtsResponse,
        dependencies=[Depends(require_api_key)],
    )
    async def generate_tts(request: TtsRequest) -> TtsResponse:
        if len(request.text) > settings.max_text_chars:
            raise HTTPException(
                status_code=413,
                detail=f"text is too long. Max {settings.max_text_chars} characters.",
            )

        generated = await provider.generate(request)
        suffix = generated.format or request.format or settings.default_format
        content_type = "audio/mpeg" if suffix == "mp3" else "audio/wav"
        audio_url = await storage.save(
            generated.audio_bytes,
            suffix,
            content_type=content_type,
            metadata=request.metadata,
        )

        return TtsResponse(
            audioUrl=audio_url,
            durationSeconds=generated.duration_seconds,
            format="wav" if suffix == "wav" else "mp3",
            voiceId=request.voice_id,
            provider=generated.provider,
            status="ready",
        )

    @router.get("/audio/{file_name}")
    async def get_audio(file_name: str):
        path = storage.resolve_audio_path(file_name)
        if path is None:
            raise HTTPException(status_code=404, detail="Local audio storage is disabled.")
        if not path.exists() or not path.is_file():
            raise HTTPException(status_code=404, detail="Audio file not found.")

        media_type = "audio/mpeg" if path.suffix.lower() == ".mp3" else "audio/wav"
        return FileResponse(path, media_type=media_type, filename=path.name)

    return router
