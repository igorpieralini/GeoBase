import yaml
import os
from pathlib import Path

def load_config():
    """Carrega a configuração do arquivo config.yml."""
    config_path = Path(__file__).parent.parent / "config.yml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config if config else {}
