from enum import Enum

class FraudType(str, Enum):
    ACCOUNT_DRAIN = "account_drain"
    VELOCITY_ABUSE = "velocity_abuse"
    GEO_IMPOSSIBLE = "geo_impossible"
    CARD_TESTING = "card_testing"
    MULE_COLLECTION = "mule_collection"
    NONE = "none"
