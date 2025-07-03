from os import getenv

from dotenv import load_dotenv

load_dotenv()

# broker
USER_SERVER = getenv("USER_SERVER")
NEW_USER_TOPIC = getenv("NEW_USER_TOPIC")
