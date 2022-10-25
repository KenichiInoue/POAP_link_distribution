import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

HENKAKU_BOT_TOKEN = os.environ.get("HENKAKU_TOKEN")
HENKAKU_POAP_LINK_TOKEN = os.environ.get("HENKAKU_POAP_LINK_TOKEN")
BCSCHOOL_TOKEN = os.environ.get("BCSCHOOL_TOKEN")
CH_ID = os.environ.get("CHANNEL_ID")
