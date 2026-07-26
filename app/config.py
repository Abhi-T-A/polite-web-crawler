from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME")

    BASE_URL = os.getenv("BASE_URL")

    USER_AGENT = os.getenv("USER_AGENT")

    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))

    REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", 2))

    OUTPUT_JSON = os.getenv("OUTPUT_JSON")

    OUTPUT_CSV = os.getenv("OUTPUT_CSV")

    DATABASE_PATH = os.getenv("DATABASE_PATH")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()