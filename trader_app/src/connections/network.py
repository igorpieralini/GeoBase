import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from ..terminal.send.sender import sendMessage

try:
    import speedtest
except ImportError:
    speedtest = None
    sendMessage("⚠️ speedtest module not installed. Speed validation will be skipped.")

ROOT_DIR = Path(__file__).resolve()
while ROOT_DIR != ROOT_DIR.parent:
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        try:
            load_dotenv(env_file)
            sendMessage(f"✅ Loaded environment variables from {env_file}")
        except Exception as e:
            sendMessage(f"⚠️ Failed to load .env file: {e}")
        break
    ROOT_DIR = ROOT_DIR.parent
else:
    sendMessage("⚠️ No .env file found — defaults will be used.")

def get_env_float(var_name, default):
    try:
        return float(os.getenv(var_name, str(default)).strip())
    except ValueError:
        sendMessage(f"⚠️ Invalid {var_name} in .env. Using default {default}.")
        return default

MIN_DOWNLOAD = get_env_float("MIN_DOWNLOAD_Mbps", 100)
MIN_UPLOAD = get_env_float("MIN_UPLOAD_Mbps", 70)
MAX_PING = get_env_float("MAX_PING_ms", 20)

def ping_test(host="8.8.8.8") -> bool:
    try:
        param = "-n" if os.name == "nt" else "-c"
        result = subprocess.run(["ping", param, "1", host], capture_output=True)
        return result.returncode == 0
    except Exception as e:
        sendMessage(f"⚠️ Ping test failed due to exception: {e}")
        return False

def check_internet_speed() -> dict:

    download_mbps = upload_mbps = ping_ms = 0
    is_suitable = False

    if speedtest is None:
        sendMessage("⚠️ Speedtest skipped (module not installed).")
    else:
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_mbps = st.download() / 1_000_000
            upload_mbps = st.upload() / 1_000_000
            ping_ms = st.results.ping
        except Exception as e:
            sendMessage(f"⚠️ Could not retrieve speedtest data: {e}")
            sendMessage("⚠️ Falling back to ping test...")

    if download_mbps == 0 and upload_mbps == 0:
        if ping_test():
            sendMessage("✅ Ping test passed. Internet is reachable, but speed not measured.")
            is_suitable = True
        else:
            sendMessage("❌ Ping test failed. Internet is not reachable. Exiting.")
            sys.exit(1)
    else:
        is_suitable = (
            download_mbps >= MIN_DOWNLOAD and
            upload_mbps >= MIN_UPLOAD and
            ping_ms <= MAX_PING
        )

    if not is_suitable:
        sendMessage(
            f"❌ Connection does not meet required standards.\n"
            f"Required: Download ≥ {MIN_DOWNLOAD} Mbps, Upload ≥ {MIN_UPLOAD} Mbps, Ping ≤ {MAX_PING} ms\n"
            f"Measured: Download = {download_mbps:.2f}, Upload = {upload_mbps:.2f}, Ping = {ping_ms} ms\n"
            f"Exiting program."
        )
        sys.exit(1)

    sendMessage(f"📥 Download: {download_mbps:.2f} Mbps (min required: {MIN_DOWNLOAD})")
    sendMessage(f"📤 Upload: {upload_mbps:.2f} Mbps (min required: {MIN_UPLOAD})")
    sendMessage(f"🏓 Ping: {ping_ms} ms (max allowed: {MAX_PING})")
    sendMessage("✅ Connection suitable for large-scale system.")

    return {
        "download_mbps": download_mbps,
        "upload_mbps": upload_mbps,
        "ping_ms": ping_ms,
        "suitable": is_suitable
    }
