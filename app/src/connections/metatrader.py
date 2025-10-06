import MetaTrader5 as mt5

class MT5Connection:
    _connected = False

    @classmethod
    def connect(cls):
        if not cls._connected:
            cls._connected = mt5.initialize()
            if cls._connected:
                print("MetaTrader 5 connection established!")
            else:
                print(f"Error connecting to MT5: {mt5.last_error()}")
        return cls._connected

    @classmethod
    def shutdown(cls):
        if cls._connected:
            mt5.shutdown()
            cls._connected = False
            print("MT5 connection closed.")

    @classmethod
    def is_connected(cls):
        return cls._connected

if __name__ == "__main__":
    MT5Connection.connect()
    print("Connected?", MT5Connection.is_connected())
    MT5Connection.shutdown()
