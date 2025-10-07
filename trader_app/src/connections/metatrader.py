import MetaTrader5 as mt5
from ..terminal.send.sender import sendMessage

class MT5Connection:

    _connected = False

    @classmethod
    def connect(cls) -> bool:
        if cls._connected:
            return True

        try:
            cls._connected = mt5.initialize()
            if cls._connected:
                sendMessage("✅ MetaTrader 5 connection established!")
            else:
                error_code = mt5.last_error()
                sendMessage(f"❌ Error connecting to MT5: {error_code}")
        except Exception as e:
            sendMessage(f"❌ Exception during MT5 connection: {e}")
            cls._connected = False

        return cls._connected

    @classmethod
    def shutdown(cls):
        if cls._connected:
            try:
                mt5.shutdown()
                cls._connected = False
                sendMessage("🛑 MT5 connection closed.")
            except Exception as e:
                sendMessage(f"⚠️ Failed to properly shutdown MT5: {e}")

    @classmethod
    def is_connected(cls) -> bool:
        return cls._connected
