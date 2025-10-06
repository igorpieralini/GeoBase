import csv
import os
from datetime import datetime

from app.src.connections.metatrader import MT5Connection
from app.src.connections.network import check_internet_speed

import MetaTrader5 as mt5

class MegaTraderCSV:

    check_internet_speed()

    @staticmethod
    def generate():
        mega_trader_symbols = [
            "EURUSD", "GBPUSD", "USDCHF"
        ]

        if not MT5Connection.connect():
            exit(1)

        csv_folder = "csv"
        os.makedirs(csv_folder, exist_ok=True)

        n_candles = 1000

        for symbol in mega_trader_symbols:
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, n_candles)
            if rates is None or len(rates) == 0:
                print(f"⚠️ No historical data for: {symbol}")
                continue

            csv_file = os.path.join(csv_folder, f"{symbol}_history.csv")
            with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
                fieldnames = ["Time", "Open", "High", "Low", "Close", "TickVolume", "Spread", "RealVolume"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for rate in rates:
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

            print(f"✅ Historical CSV exported successfully: {csv_file}")

        MT5Connection.shutdown()


if __name__ == "__main__":
    MegaTraderCSV.generate()
