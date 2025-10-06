import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Tenta importar speedtest
try:
    import speedtest
except ImportError:
    speedtest = None
    print("⚠️ speedtest module not installed. Speed validation will be skipped.")

# Carrega .env
ROOT_DIR = Path(__file__).resolve()
while ROOT_DIR != ROOT_DIR.parent:
    if (ROOT_DIR / ".env").exists():
        ENV_PATH = ROOT_DIR / ".env"
        try:
            load_dotenv(ENV_PATH)
            print(f"✅ Loaded environment variables from {ENV_PATH}")
        except Exception as e:
            print(f"⚠️ Failed to load .env file: {e}")
        break
    ROOT_DIR = ROOT_DIR.parent
else:
    print("⚠️ No .env file found — defaults will be used.\n")

# Leitura segura das variáveis de configuração
try:
    MIN_DOWNLOAD = float(os.getenv("MIN_DOWNLOAD_Mbps", "100").strip())
except ValueError:
    print("⚠️ Invalid MIN_DOWNLOAD_Mbps in .env. Using default 100 Mbps.")
    MIN_DOWNLOAD = 100.0

try:
    MIN_UPLOAD = float(os.getenv("MIN_UPLOAD_Mbps", "70").strip())
except ValueError:
    print("⚠️ Invalid MIN_UPLOAD_Mbps in .env. Using default 70 Mbps.")
    MIN_UPLOAD = 70.0

try:
    MAX_PING = float(os.getenv("MAX_PING_ms", "20").strip())
except ValueError:
    print("⚠️ Invalid MAX_PING_ms in .env. Using default 20 ms.")
    MAX_PING = 20.0

def ping_test(host="8.8.8.8"):
    """Fallback ping test to verify internet connectivity"""
    try:
        param = "-n" if os.name == "nt" else "-c"
        result = subprocess.run(["ping", param, "1", host], capture_output=True)
        return result.returncode == 0
    except Exception as e:
        print(f"⚠️ Ping test failed due to exception: {e}")
        return False

def check_internet_speed():
    download_mbps = upload_mbps = ping_ms = 0
    is_suitable = False

    if speedtest is None:
        print("⚠️ Speedtest skipped (module not installed).")
    else:
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_mbps = st.download() / 1_000_000
            upload_mbps = st.upload() / 1_000_000
            ping_ms = st.results.ping
        except Exception as e:
            print(f"⚠️ Could not retrieve speedtest data: {e}")
            print("⚠️ Trying ping fallback...")

    # Fallback se speedtest falhar
    if download_mbps == 0 and upload_mbps == 0:
        if ping_test():
            print("✅ Ping test passed. Internet is reachable, but speed not measured.")
            is_suitable = True
        else:
            print("❌ Ping test failed. Internet is not reachable. Exiting.")
            sys.exit(1)
    else:
        is_suitable = download_mbps >= MIN_DOWNLOAD and upload_mbps >= MIN_UPLOAD and ping_ms <= MAX_PING

    # Validação final
    if not is_suitable:
        print(f"❌ Connection does not meet the required standards.\n"
              f"Required: Download ≥ {MIN_DOWNLOAD} Mbps, Upload ≥ {MIN_UPLOAD} Mbps, Ping ≤ {MAX_PING} ms\n"
              f"Measured: Download = {download_mbps:.2f}, Upload = {upload_mbps:.2f}, Ping = {ping_ms} ms\n"
              f"Exiting program.")
        sys.exit(1)

    print(f"📥 Download: {download_mbps:.2f} Mbps (min required: {MIN_DOWNLOAD})")
    print(f"📤 Upload: {upload_mbps:.2f} Mbps (min required: {MIN_UPLOAD})")
    print(f"🏓 Ping: {ping_ms} ms (max allowed: {MAX_PING})")
    print("✅ Connection suitable for large-scale system.")

    return {
        "download_mbps": download_mbps,
        "upload_mbps": upload_mbps,
        "ping_ms": ping_ms,
        "suitable": is_suitable
    }

if __name__ == "__main__":
    try:
        result = check_internet_speed()
    except Exception as e:
        print(f"❌ Unexpected error during internet check: {e}")
        sys.exit(1)
