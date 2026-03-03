import logging
from typing import Optional


# --- 1. 自訂 DONE 等級與方法 ---
DONE = 25
logging.addLevelName(DONE, "DONE")
logging.DONE = DONE


def _done(self: logging.Logger, message: str, *args, **kwargs) -> None:
    if self.isEnabledFor(DONE):
        self._log(DONE, message, args, **kwargs)


# 掛到 Logger 類別，之後任何 logger 都可以 logger.done(...)
logging.Logger.done = _done


# --- 2. Emoji Formatter ---
class EmojiFormatter(logging.Formatter):
    """
    Emoji Formatter
    """
    EMOJIS = {
        logging.ERROR: "❌",
        logging.WARNING: "⚠️",
        logging.INFO: "   ",
        DONE: "✅",
    }

    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        prefix = self.EMOJIS.get(record.levelno, "")
        return f"{prefix} {base}" if prefix else base


# --- 3. LoggerClient 包裝 ---
class LoggerClient:
    """
    Standard logger wrapper with emoji formatting and file logging.
    """

    def __init__(
        self,
        name: str = "app",
        level: int = logging.INFO,
        fmt: str = "%(asctime)s - %(levelname)s\n%(message)s",
    ) -> None:
        self._name = name
        self._level = level
        self._fmt = fmt
        self._logger = self._setup()

    def _setup(
        self,
        name: Optional[str] = None,
        level: Optional[int] = None,
    ) -> logging.Logger:
        name = name or self._name
        level = level or self._level

        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:
            # Console Handler
            handler = logging.StreamHandler()
            handler.setFormatter(EmojiFormatter(self._fmt))
            logger.addHandler(handler)
            
            # File Handler
            from pathlib import Path
            # Resolve project root (presumes src/<pkg>/clients/logger.py)
            project_root = Path(__file__).resolve().parent.parent.parent.parent
            log_dir = project_root / "log"
            log_dir.mkdir(exist_ok=True, parents=True)
                
            file_handler = logging.FileHandler(log_dir / f"{self._name}.log")
            file_handler.setFormatter(logging.Formatter(self._fmt))
            logger.addHandler(file_handler)

        return logger

    def get(self) -> logging.Logger:
        return self._logger
