from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
VALHEIM_LOG_PATH = os.getenv('VALHEIM_LOG_PATH')
SCOREBOARD_FILE = os.getenv('SCOREBOARD_FILE')
