from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

AudioFormat = Literal["wav", "mp3"]
SpeechStatus = Literal["ready", "failed"]


class TtsRequest(BaseModel):
    text: str = Field(min_length=1)
    language: str = Field(default="en", min_length=2, max_length=16)
    voice_id: str = Field(default="sabi_female_en_01", alias="voiceId")
    format: AudioFormat = "wav"
    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("text")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        cleaned = " ".join(value.split())
        if not cleaned:
            raise ValueError("text cannot be empty")
        return cleaned

    @field_validator("language")
    @classmethod
    def normalize_language(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("voice_id")
    @classmethod
    def normalize_voice_id(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("voiceId cannot be empty")
        return cleaned


class TtsResponse(BaseModel):
    audio_url: str = Field(alias="audioUrl")
    duration_seconds: float = Field(alias="durationSeconds")
    format: AudioFormat
    voice_id: str = Field(alias="voiceId")
    provider: str
    status: SpeechStatus = "ready"


class HealthResponse(BaseModel):
    ok: bool
    service: str
    provider: str
    storage: str
