from fastapi import FastAPI

from app.api.routes import build_router
from app.core.config import get_settings
from app.providers.factory import build_voice_provider
from app.storage.factory import build_audio_storage


def create_app() -> FastAPI:
    settings = get_settings()
    provider = build_voice_provider(settings)
    storage = build_audio_storage(settings)

    app = FastAPI(
        title="Sabi Voice Service",
        version="0.1.0",
        description="Open-source voice generation backend for Sabi Voice Learning.",
    )

    app.include_router(
        build_router(
            settings=settings,
            provider=provider,
            storage=storage,
        )
    )
    return app


app = create_app()
