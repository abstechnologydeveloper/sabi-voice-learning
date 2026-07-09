from app.core.config import Settings
from app.providers.base import VoiceProvider
from app.providers.kokoro_onnx import KokoroOnnxVoiceProvider
from app.providers.stub import StubVoiceProvider


def build_voice_provider(settings: Settings) -> VoiceProvider:
    if settings.provider == "stub":
        return StubVoiceProvider()

    if settings.provider == "kokoro-onnx":
        return KokoroOnnxVoiceProvider(settings)

    raise RuntimeError(f"Provider '{settings.provider}' is not supported.")
