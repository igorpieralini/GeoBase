import sys
from pathlib import Path
import time

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.main import create_api

if __name__ == "__main__":
    start_time = time.time()
    print("\n" + "="*60)
    print("🎯 TraderIA API - Iniciando...")
    print("="*60 + "\n")
    
    create_api()
    
    total_time = time.time() - start_time
    print("\n" + "="*60)
    print(f"⏱️  Tempo total de execução: {total_time:.2f}s")
    print("="*60 + "\n")
