import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

HENKAKU_POAP_LINK_BOT_TOKEN = os.environ.get("HENKAKU_POAP_LINK_BOT_TOKEN")
