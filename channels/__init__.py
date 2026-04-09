from channels.a1_investors import CHANNEL as A1_INVESTORS
from channels.a1_markets import CHANNEL as A1_MARKETS

CHANNELS = {
    "a1_investors": A1_INVESTORS,
    "a1_markets": A1_MARKETS,
}


def get_channel(slug):
    return CHANNELS.get(slug)


def list_channels():
    return [{"slug": k, "name": v["name"], "description": v["description"]} for k, v in CHANNELS.items()]
