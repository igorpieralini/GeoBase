import csv
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

import MetaTrader5 as mt5
from app.src.connections.metatrader import MT5Connection
from app.src.connections.network import check_internet_speed

ROOT_DIR = Path(__file__).resolve()
while ROOT_DIR != ROOT_DIR.parent:
    if (ROOT_DIR / ".env").exists():
        load_dotenv(ROOT_DIR / ".env")
        break
    ROOT_DIR = ROOT_DIR.parent

N_CANDLES = int(os.getenv("N_CANDLES", 10000))

check_internet_speed()

class MegaTraderCSV:

    @staticmethod
    def generate():
        mega_trader_symbols = os.getenv("MEGA_TRADER_SYMBOLS", "EURUSD,GBPUSD,USDCHF").split(",")

        if not MT5Connection.connect():
            print("❌ Failed to connect to MetaTrader 5. Exiting.")
            exit(1)

        csv_folder = "csv"
        os.makedirs(csv_folder, exist_ok=True)

        for symbol in mega_trader_symbols:
            try:
                rates = mt5.copy_rates_from_pos(symbol.strip(), mt5.TIMEFRAME_M1, 0, N_CANDLES)
                if rates is None or len(rates) == 0:
                    print(f"⚠️ No historical data available for symbol: {symbol}")
                    continue

                csv_file = os.path.join(csv_folder, f"{symbol.strip()}_history.csv")
                with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
                    fieldnames = ["Time", "Open", "High", "Low", "Close", "TickVolume", "Spread", "RealVolume"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()

                    for rate in rates:
                        try:
                            writer.writerow({
                                "Time": datetime.fromtimestamp(rate['time']).strftime("%Y-%m-%d %H:%M:%S"),
                                "Open": rate['open'],
                                "High": rate['high'],
                                "Low": rate['low'],
                                "Close": rate['close'],
                                "TickVolume": rate['tick_volume'],
                                "Spread": rate['spread'],
                                "RealVolume": rate['real_volume']
                            })
                        except Exception as e:
                            print(f"⚠️ Failed to write rate for {symbol}: {e}")

                print(f"✅ Historical CSV exported successfully: {csv_file}")

            except Exception as e:
                print(f"❌ Failed to retrieve historical data for {symbol}: {e}")

        try:
            MT5Connection.shutdown()
        except Exception as e:
            print(f"⚠️ Failed to shutdown MT5 connection properly: {e}")


if __name__ == "__main__":
    try:
        MegaTraderCSV.generate()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        MT5Connection.shutdown()
        exit(1)
