# Python Project Standards

This document outlines the standard project structure, configuration management, and client abstractions for Python projects in this homelab environment, derived from the successful `vod_hub` and `abg` implementations.

## 1. Project Structure

A standard project should follow this source-layout:
```text
project_root/
├── pyproject.toml
├── .env
├── src/
│   └── <package_name>/
│       ├── __init__.py
│       ├── main.py
│       ├── configs/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── redis.py (optional)
│       │   └── ...
│       ├── clients/
│       │   ├── __init__.py
│       │   ├── logger.py
│       │   ├── fetch.py
│       │   ├── llm.py
│       │   └── ...
│       ├── models/
│       │   ├── __init__.py
│       │   └── ...
│       └── tools/
│           ├── __init__.py
│           └── ...
└── tests/
    └── ...
```

## 2. Configuration Management

Use `pydantic-settings` to manage configurations in a modular way.

### Base Configuration (`configs/base.py`)
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"

class BaseAppConfig(BaseSettings):
    SERVER_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    SERVER_MODE: str = "production"
    LOG_LEVEL: str = "INFO"
    TZ: str = "Asia/Hong_Kong"
    
    model_config = SettingsConfigDict(
        env_prefix=os.getenv("ENV_PREFIX", ""),
        env_file=os.getenv("ENV_FILE", str(DEFAULT_ENV_FILE)),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
```

## 3. Client Abstractions

### LoggerClient (`clients/logger.py`)
Provides premium logging with `DONE` level and emoji formatting. Use `LoggerClient().get()` to retrieve the logger instance.

### FetchClient (`clients/fetch.py`)
A robust `httpx`-based async client with:
- URL building with template support.
- Automatic retries with exponential backoff.
- HTML processing for LLM-friendly text extraction (via BeautifulSoup).
- Standardized error handling.

### LLMClient (`clients/llm.py`)
A `LangChain`-based OpenAI-compatible client for text and image generation.
- Supports system, assistant, and user prompts.
- Handles rate limits and basic error propagation.

## 4. `__init__.py` Patterns

To ensure clean namespaces and avoid circular imports, follow these patterns:

### Client/Config Exports (`clients/__init__.py`)
Export **classes** (not instances) from the submodules using relative imports and `__all__`.

```python
from .logger import LoggerClient
from .fetch import FetchClient
from .llm import LLMClient

__all__ = [
    "LoggerClient",
    "FetchClient",
    "LLMClient",
]
```

### Configuration Instance (`configs/__init__.py`)
Expose a single `settings` instance and the `Settings` class.

```python
from .llm import LLMSettings

class Settings(LLMSettings):
    pass

settings = Settings()

__all__ = ["settings", "Settings"]
```

## 5. Implementation Guidelines
- **Always** use modular configs instead of a single `config.py`.
- **Always** use `LoggerClient` for consistent, aesthetic logs.
- **Always** use `FetchClient` or derived classes for HTTP interactions.
- **Always** use `LLMClient` for interactions with Large Language Models.
- **Always** include a `tools/` directory for stand-alone utilities.
- **Always** explicitly export public classes and instances using `__all__` inside the `__init__.py` files of your submodules (`configs`, `clients`, `models`, `tools`).
- **Always** use standard relative `.module` imports within a package's internal `__init__.py` file to cleanly expose exports.
- **Always** instantiate clients (like `LoggerClient`, `FetchClient`) **within the module that uses them** (e.g., `main.py`, `worker.py`) using `LoggerClient(__name__).get()`, rather than exporting instances from `clients/__init__.py`.
- **Always** use absolute package imports externally across the application namespace, referencing those exposed functions directly (e.g., `from mac_tts.configs import settings` instead of relative internals like `from .configs import settings`).
