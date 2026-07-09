import io
import math
import wave

from app.providers.base import GeneratedSpeech
from app.schemas import TtsRequest


class StubVoiceProvider:
    name = "stub"

    async def generate(self, request: TtsRequest) -> GeneratedSpeech:
        duration_seconds = min(2.5, max(0.7, len(request.text) / 120.0))
        sample_rate = 24_000
        frequency = self._frequency_for_language(request.language)
        frames = int(sample_rate * duration_seconds)
        amplitude = 8000

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            for index in range(frames):
                envelope = min(1.0, index / 1200, (frames - index) / 1200)
                sample = int(
                    amplitude
                    * envelope
                    * math.sin(2 * math.pi * frequency * index / sample_rate)
                )
                wav.writeframesraw(sample.to_bytes(2, byteorder="little", signed=True))

        return GeneratedSpeech(
            audio_bytes=buffer.getvalue(),
            duration_seconds=round(duration_seconds, 3),
            format="wav",
            provider=self.name,
        )

    def _frequency_for_language(self, language: str) -> float:
        return {
            "en": 440.0,
            "yo": 494.0,
            "ha": 523.25,
            "ig": 587.33,
            "pcm": 659.25,
            "pidgin": 659.25,
        }.get(language.lower(), 440.0)
