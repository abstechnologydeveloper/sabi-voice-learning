from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_KOKORO_VOICE = "af_heart"
DEFAULT_KOKORO_LANG_CODE = "a"
DEFAULT_KOKORO_ONNX_LANG = "en-us"
DEFAULT_KOKORO_ONNX_MODEL_PATH = Path("models/kokoro/kokoro-v1.0.onnx")
DEFAULT_KOKORO_ONNX_VOICES_PATH = Path("models/kokoro/voices-v1.0.bin")
DEFAULT_PROVIDER = "kokoro-onnx"
DEFAULT_UPLOAD_PATH = "/api/v1/public-files-upload"
LOCAL_AUDIO_DIR = Path("storage/audio")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_keys: str = Field(default="", alias="SABI_VOICE_API_KEYS")
    use_stub_provider: bool = Field(default=False, alias="SABI_VOICE_USE_STUB")
    backend_base_url: str = Field(default="", alias="SABI_VOICE_BACKEND_BASE_URL")
    upload_api_key: str = Field(default="", alias="SABI_VOICE_UPLOAD_API_KEY")
    max_text_chars: int = Field(default=4000, alias="SABI_VOICE_MAX_TEXT_CHARS")

    @property
    def allowed_api_keys(self) -> set[str]:
        return {
            item.strip()
            for item in self.api_keys.split(",")
            if item.strip()
        }

    @property
    def provider(self) -> str:
        return "stub" if self.use_stub_provider else DEFAULT_PROVIDER

    @property
    def storage_dir(self) -> Path:
        return LOCAL_AUDIO_DIR

    @property
    def normalized_public_base_url(self) -> str:
        return "http://localhost:8095"

    @property
    def default_format(self) -> str:
        return "wav"

    @property
    def upload_endpoint_url(self) -> str:
        if not self.backend_base_url:
            return ""
        return f"{self.backend_base_url.rstrip('/')}{DEFAULT_UPLOAD_PATH}"

    @property
    def kokoro_onnx_model_path(self) -> Path:
        return DEFAULT_KOKORO_ONNX_MODEL_PATH

    @property
    def kokoro_onnx_voices_path(self) -> Path:
        return DEFAULT_KOKORO_ONNX_VOICES_PATH


@lru_cache
def get_settings() -> Settings:
    return Settings()
