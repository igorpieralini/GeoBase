import asyncio
from fastapi import FastAPI
from app.core.logger import logger
from app.services.stock_service import StockService
from app.services.news_service import NewsService

stock_service = StockService()
news_service = NewsService()

async def fetch_data_periodically():
    while True:
        try:
            await asyncio.to_thread(stock_service.fetch_and_save)
            await asyncio.to_thread(news_service.fetch_and_save, stock_service.symbols)
            logger.info("Stock data and news collected and saved successfully.")
        except Exception as e:
            logger.error(f"Error during data collection: {e}")
        await asyncio.sleep(60)

def create_app() -> FastAPI:
    app = FastAPI(title="Finance AI API", version="0.0.0_Development")

    @app.on_event("startup")
    async def startup_event():
        asyncio.create_task(fetch_data_periodically())
        logger.info("Periodic data collection task started.")

    logger.info("API initialized.")
    return app

app = create_app()
