import yaml
from pydantic import BaseModel
from types import SimpleNamespace

class DatabaseSettings(BaseModel):
    host: str
    user: str
    password: str
    name: str

class DataSourcesSettings(BaseModel):
    provider: str
    interval: str
    history_limit: int
    news_api_key: str
    symbols: list[str]

class ModelSettings(BaseModel):
    type: str
    window_size: int
    epochs: int
    batch_size: int

class RecommendationSettings(BaseModel):
    buy_threshold: float
    sell_threshold: float

class LoggingSettings(BaseModel):
    level: str
    save_to_mysql: bool
    save_to_file: bool
    file_path: str

class APISettings(BaseModel):
    port: int
    enable_auth: bool

class AppSettings(BaseModel):
    version: str
    time_development: str
    Authors: list[str]

class Settings(BaseModel):
    database: DatabaseSettings
    data_sources: DataSourcesSettings
    model: ModelSettings
    recommendation: RecommendationSettings
    logging: LoggingSettings
    api: APISettings
    app: AppSettings

with open("config.yml", "r") as f:
    config_dict = yaml.safe_load(f)

settings = Settings(**config_dict)
