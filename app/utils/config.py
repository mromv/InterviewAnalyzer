"""
Конфигурации
"""
from typing import Optional
from pydantic_settings import BaseSettings


class LLMConfig(BaseSettings):
    api_key: str
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    temperature: float = 0.3
    max_tokens: int = 8192


class Settings(BaseSettings):
    """Настройки приложения"""

    # API-агенты
    llm_base: LLMConfig
    llm_company_analyzer: Optional[LLMConfig] = None
    llm_hypotheses_generator: Optional[LLMConfig] = None
    llm_industry_analyzer: Optional[LLMConfig] = None
    llm_final_analyzer: Optional[LLMConfig] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = '__'

settings = Settings()
