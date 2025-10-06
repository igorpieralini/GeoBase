import os
import speedtest
from pathlib import Path
from dotenv import load_dotenv

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

    if download_mbps < MIN_DOWNLOAD:
        print(f"⚠️ Warning: Download speed below {MIN_DOWNLOAD} Mbps")
    if upload_mbps < MIN_UPLOAD:
        print(f"⚠️ Warning: Upload speed below {MIN_UPLOAD} Mbps")
    if ping_ms > MAX_PING:
        print(f"⚠️ Warning: Ping higher than {MAX_PING} ms")

    is_suitable = download_mbps >= MIN_DOWNLOAD and upload_mbps >= MIN_UPLOAD and ping_ms <= MAX_PING
    status_emoji = "✅" if is_suitable else "❌"
    print(f"{status_emoji} Connection suitable for large-scale system: {is_suitable}")

    return {
        "download_mbps": download_mbps,
        "upload_mbps": upload_mbps,
        "ping_ms": ping_ms,
        "suitable": is_suitable
    }

if __name__ == "__main__":
    result = check_internet_speed()
