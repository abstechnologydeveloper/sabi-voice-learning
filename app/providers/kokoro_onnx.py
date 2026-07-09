import asyncio
import io

import soundfile as sf

from app.core.config import DEFAULT_KOKORO_ONNX_LANG, DEFAULT_KOKORO_VOICE, Settings
from app.providers.base import GeneratedSpeech
from app.schemas import TtsRequest

KOKORO_ONNX_LANGUAGE_CODES = {
    "en": "en-us",
    "en-us": "en-us",
    "american-english": "en-us",
    "en-gb": "en-gb",
    "british-english": "en-gb",
    "es": "es",
    "fr": "fr",
    "hi": "hi",
    "it": "it",
    "ja": "ja",
    "pt-br": "pt-br",
    "zh": "zh",
    "zh-cn": "zh",
}


class KokoroOnnxVoiceProvider:
    name = "kokoro-onnx"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._engine = None

    async def generate(self, request: TtsRequest) -> GeneratedSpeech:
        return await asyncio.to_thread(self._generate_sync, request)

    def _generate_sync(self, request: TtsRequest) -> GeneratedSpeech:
        engine = self._get_engine()
        voice = self._voice_for(request)
        language = self._language_for(request)

        audio, sample_rate = engine.create(
            request.text,
            voice=voice,
            speed=request.speed,
            lang=language,
        )

        buffer = io.BytesIO()
        sf.write(buffer, audio, sample_rate, format="WAV")

        return GeneratedSpeech(
            audio_bytes=buffer.getvalue(),
            duration_seconds=round(float(len(audio) / sample_rate), 3),
            format="wav",
            provider=self.name,
        )

    def _get_engine(self):
        if self._engine is not None:
            return self._engine

        model_path = self.settings.kokoro_onnx_model_path
        voices_path = self.settings.kokoro_onnx_voices_path
        if not model_path.exists():
            raise RuntimeError(f"Kokoro ONNX model file not found: {model_path}")
        if not voices_path.exists():
            raise RuntimeError(f"Kokoro ONNX voices file not found: {voices_path}")

        try:
            from kokoro_onnx import Kokoro
        except ImportError as exc:
            raise RuntimeError(
                "Kokoro ONNX dependencies are not installed. "
                "Run: pip install -r requirements.txt"
            ) from exc

        self._engine = Kokoro(str(model_path), str(voices_path))
        return self._engine

    def _language_for(self, request: TtsRequest) -> str:
        override = request.metadata.get("kokoroOnnxLang")
        if isinstance(override, str) and override.strip():
            return override.strip()

        return KOKORO_ONNX_LANGUAGE_CODES.get(
            request.language.lower(),
            DEFAULT_KOKORO_ONNX_LANG,
        )

    def _voice_for(self, request: TtsRequest) -> str:
        override = request.metadata.get("kokoroOnnxVoice")
        if isinstance(override, str) and override.strip():
            return override.strip()

        if request.voice_id.startswith(("af_", "am_", "bf_", "bm_")):
            return request.voice_id

        return DEFAULT_KOKORO_VOICE
