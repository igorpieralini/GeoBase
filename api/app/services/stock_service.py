import os
from datetime import datetime
import time
import yfinance as yf
import pandas as pd
from app.config import settings
from app.core.logger import logger

class StockService:
    def __init__(self):
        self.interval = settings.data_sources.interval
        self.base_path = "data/assets"
        self.symbols = settings.data_sources.symbols
        self.retry_attempts = 3
        self.retry_delay = 3
        self.request_delay = 1

    def fetch_stock(self, symbol: str) -> pd.DataFrame:
        for attempt in range(1, self.retry_attempts + 1):
            try:
                ticker_full = symbol + ".SA"
                ticker = yf.Ticker(ticker_full)

                data = yf.download(
                    tickers=ticker_full,
                    period="max",  # traz todo o histórico disponível
                    interval=self.interval,
                    auto_adjust=True,
                    progress=False,
                    threads=False
                )

                if data.empty:
                    logger.warning(f"No data found for {symbol}. Symbol may be inactive or delisted.")
                    return pd.DataFrame()

                info = ticker.info
                company_info = {
                    "symbol": symbol,
                    "name": info.get("longName", ""),
                    "sector": info.get("sector", ""),
                    "industry": info.get("industry", ""),
                    "marketCap": info.get("marketCap", ""),
                    "PE_ratio": info.get("trailingPE", ""),
                    "PB_ratio": info.get("priceToBook", ""),
                    "EPS": info.get("trailingEps", ""),
                    "dividendYield": info.get("dividendYield", ""),
                    "debtToEquity": info.get("debtToEquity", "")
                }

                df = data.reset_index()
                for i, (key, value) in enumerate(company_info.items()):
                    df.insert(i, key, value)

                time.sleep(self.request_delay)
                return df

            except Exception as e:
                logger.error(f"Failed to fetch {symbol}, attempt {attempt}/{self.retry_attempts}: {e}")
                if attempt < self.retry_attempts:
                    time.sleep(self.retry_delay)
                else:
                    return pd.DataFrame()

    def save_stock(self, symbol: str, df: pd.DataFrame):
        if df.empty:
            logger.warning(f"No data to save for {symbol}.")
            return

        base_path = os.path.join(self.base_path, symbol)
        os.makedirs(base_path, exist_ok=True)

        # Salva preços e dados principais
        price_path = os.path.join(base_path, "price.csv")
        df.to_csv(price_path, index=False)
        logger.info(f"Saved price data for {symbol} to {price_path}")

        ticker = yf.Ticker(symbol + ".SA")

        # Salva dividendos
        dividends = ticker.dividends
        if not dividends.empty:
            div_path = os.path.join(base_path, "dividends.csv")
            dividends.to_csv(div_path, index=True)
            logger.info(f"Saved dividends for {symbol} to {div_path}")

        # Salva splits
        splits = ticker.splits
        if not splits.empty:
            splits_path = os.path.join(base_path, "splits.csv")
            splits.to_csv(splits_path, index=True)
            logger.info(f"Saved splits for {symbol} to {splits_path}")

    def fetch_and_save(self):
        for symbol in self.symbols:
            df = self.fetch_stock(symbol)
            self.save_stock(symbol, df)
