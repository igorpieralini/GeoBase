import os
from datetime import datetime

log_level = "INFO"
log_path = "logs/"

EMOJI_MAP = {
    "INFO": "ℹ️",
    "ERROR": "❌",
    "WARNING": "⚠️",
    "SUCCESS": "✅",
    "DEBUG": "🔍"
}

COLOR_MAP = {
    "INFO": "\033[94m",
    "ERROR": "\033[91m",
    "WARNING": "\033[93m",
    "SUCCESS": "\033[92m",
    "DEBUG": "\033[36m"
}
RESET_COLOR = "\033[0m"

def configure_logger(level: str = "INFO", path: str = "logs/"):
    global log_level, log_path
    log_level = level
    log_path = path

def log_message(message: str, level: str = "INFO"):
    if not os.path.exists(log_path):
        os.makedirs(log_path, exist_ok=True)
    
    emoji = EMOJI_MAP.get(level, "📝")
    color = COLOR_MAP.get(level, "")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    console_msg = f"{color}{emoji} [{timestamp}] {level}: {message}{RESET_COLOR}"
    file_msg = f"[{timestamp}] {level}: {message}"
    
    print(console_msg)
    
    log_file = os.path.join(log_path, f"app_{datetime.now().strftime('%Y%m%d')}.log")
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(file_msg + "\n")
    except Exception as e:
        print(f"❌ Erro ao escrever log: {e}")
