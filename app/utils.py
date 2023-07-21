from langchain.callbacks import get_openai_callback
from pydantic import  BaseSettings
from functools import lru_cache


def count_tokens(chain, query):
    """
    Calculate cost assosiated
    """
    with get_openai_callback() as cb:
        result = chain({"question" :query})
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")

    return result, cb


class Settings(BaseSettings):
    """
    Settings class for this application.
    Utilizes the BaseSettings from pydantic for environment variables.
    """

    openai_api_key: str
    host: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """Function to get and cache settings.
    The settings are cached to avoid repeated disk I/O.
    """
    return Settings()