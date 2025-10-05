import speedtest


def check_internet_speed():
    st = speedtest.Speedtest()
    st.get_best_server()

    download_mbps = st.download() / 1_000_000
    upload_mbps = st.upload() / 1_000_000
    ping_ms = st.results.ping

    print(f"📥 Download: {download_mbps:.2f} Mbps")
    print(f"📤 Upload: {upload_mbps:.2f} Mbps")
    print(f"🏓 Ping: {ping_ms} ms")

    if download_mbps < 100:
        print("⚠️ Warning: Download speed below 100 Mbps")
    if upload_mbps < 70:
        print("⚠️ Warning: Upload speed below 70 Mbps")
    if ping_ms > 20:
        print("⚠️ Warning: Ping higher than 20 ms")

    is_suitable = download_mbps >= 100 and upload_mbps >= 70 and ping_ms <= 20
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
