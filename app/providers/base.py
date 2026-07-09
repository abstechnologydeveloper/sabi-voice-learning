from dataclasses import dataclass
from typing import Protocol

from app.schemas import TtsRequest


@dataclass(frozen=True)
class GeneratedSpeech:
    audio_bytes: bytes
    duration_seconds: float
    format: str
    provider: str


class VoiceProvider(Protocol):
    name: str

    async def generate(self, request: TtsRequest) -> GeneratedSpeech:
        ...
