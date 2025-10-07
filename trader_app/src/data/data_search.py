import os
import csv
from datetime import datetime
import MetaTrader5 as mt5
import numpy as np

from ..connections.network import check_internet_speed
from ..terminal.send.sender import sendMessage
from ..connections.metatrader import MT5Connection


class MegaTraderCSV:
    @staticmethod
    def generate(symbols=None, count=10000):
        try:
            check_internet_speed()
        except Exception as e:
            sendMessage(f"⚠️ Falha ao verificar internet: {e}")

        if symbols is None:
            symbols = os.getenv("MEGA_TRADER_SYMBOLS", "EURUSD,GBPUSD,USDCHF").split(",")

        if not MT5Connection.connect():
            sendMessage("❌ Failed to connect to MetaTrader 5. Exiting.")
            return

        os.makedirs("csv", exist_ok=True)

        for symbol in symbols:
            symbol = symbol.strip()
            sendMessage(f"⏳ Retrieving data for {symbol}...")

            try:
                rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, count)

                if rates is None or len(rates) == 0 or (isinstance(rates, np.ndarray) and rates.size == 0):
                    sendMessage(f"⚠️ No historical data found for {symbol}")
                    continue

                csv_file = os.path.join("csv", f"{symbol}_history.csv")
                with open(csv_file, "w", newline="", encoding="utf-8") as f:
                    fieldnames = ["Time", "Open", "High", "Low", "Close", "TickVolume", "Spread", "RealVolume"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()

                    for r in rates:
                        writer.writerow({
                            "Time": datetime.fromtimestamp(r['time']).strftime("%Y-%m-%d %H:%M:%S"),
                            "Open": r['open'],
                            "High": r['high'],
                            "Low": r['low'],
                            "Close": r['close'],
                            "TickVolume": r['tick_volume'],
                            "Spread": r['spread'],
                            "RealVolume": r['real_volume']
                        })

                sendMessage(f"✅ CSV exported successfully: {csv_file}")

            except Exception as e:
                sendMessage(f"❌ Error retrieving data for {symbol}: {e}")

        try:
            MT5Connection.shutdown()
            sendMessage("✅ MetaTrader 5 connection closed successfully.")
        except Exception as e:
            sendMessage(f"⚠️ Failed to properly shutdown MT5 connection: {e}")
