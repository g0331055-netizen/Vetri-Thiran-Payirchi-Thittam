from os import environ
from pathlib import Path


def _load_env_file() -> None:
    env_file = Path(__file__).with_name(".env")
    if not env_file.exists():
        return

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file()


class Settings:
    APP_NAME = environ.get("APP_NAME", "EduGenie")
    GEMINI_MODEL = environ.get("GEMINI_MODEL", "gemini-pro")
    HOST = environ.get("HOST", "127.0.0.1")
    PORT = int(environ.get("PORT", "8000"))


settings = Settings()