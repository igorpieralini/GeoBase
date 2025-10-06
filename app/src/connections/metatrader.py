import MetaTrader5 as mt5
import sys

class MT5Connection:
    _connected = False

    @classmethod
    def connect(cls):
        """Establish a connection to MetaTrader 5."""
        if cls._connected:
            return True
        try:
            cls._connected = mt5.initialize()
            if cls._connected:
                print("✅ MetaTrader 5 connection established!")
            else:
                error_code = mt5.last_error()
                print(f"❌ Error connecting to MT5: {error_code}")
        except Exception as e:
            print(f"❌ Exception during MT5 connection: {e}")
            cls._connected = False
        return cls._connected

    @classmethod
    def shutdown(cls):
        """Shutdown MT5 connection if active."""
        if cls._connected:
            try:
                mt5.shutdown()
                cls._connected = False
                print("🛑 MT5 connection closed.")
            except Exception as e:
                print(f"⚠️ Failed to properly shutdown MT5: {e}")

    @classmethod
    def is_connected(cls):
        """Check connection status."""
        return cls._connected


if __name__ == "__main__":
    try:
        if not MT5Connection.connect():
            print("❌ Unable to connect to MT5. Exiting.")
            sys.exit(1)
        print("Connected?", MT5Connection.is_connected())
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        MT5Connection.shutdown()
