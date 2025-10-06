import os
import speedtest
from pathlib import Path
from dotenv import load_dotenv
import sys

ROOT_DIR = Path(__file__).resolve()
while ROOT_DIR != ROOT_DIR.parent:
    if (ROOT_DIR / ".env").exists():
        ENV_PATH = ROOT_DIR / ".env"
        load_dotenv(ENV_PATH)
        break
    ROOT_DIR = ROOT_DIR.parent
else:
    print("⚠️ No .env file found — defaults will be used.\n")

MIN_DOWNLOAD = float(os.getenv("MIN_DOWNLOAD_Mbps", 100))
MIN_UPLOAD = float(os.getenv("MIN_UPLOAD_Mbps", 70))
MAX_PING = float(os.getenv("MAX_PING_ms", 20))

def check_internet_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        download_mbps = st.download() / 1_000_000
        upload_mbps = st.upload() / 1_000_000
        ping_ms = st.results.ping

    except Exception as e:
        print(f"❌ Failed to retrieve speedtest data: {e}")
        download_mbps = 0
        upload_mbps = 0
        ping_ms = 0

    print(f"📥 Download: {download_mbps:.2f} Mbps (min required: {MIN_DOWNLOAD})")
    print(f"📤 Upload: {upload_mbps:.2f} Mbps (min required: {MIN_UPLOAD})")
    print(f"🏓 Ping: {ping_ms} ms (max allowed: {MAX_PING})")

    is_suitable = download_mbps >= MIN_DOWNLOAD and upload_mbps >= MIN_UPLOAD and ping_ms <= MAX_PING

    if not is_suitable:
        print(f"❌ Connection does not meet the required standards. Exiting program.")
        sys.exit(1)  # encerra o programa

    print(f"✅ Connection suitable for large-scale system.")

    return {
        "download_mbps": download_mbps,
        "upload_mbps": upload_mbps,
        "ping_ms": ping_ms,
        "suitable": is_suitable
    }

if __name__ == "__main__":
    result = check_internet_speed()
