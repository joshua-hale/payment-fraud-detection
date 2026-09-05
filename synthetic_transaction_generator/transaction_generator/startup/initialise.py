from synthetic_transaction_generator.schemas.simulation_config import SimulationConfig
from synthetic_transaction_generator.schemas.card_profile import CardProfile
from synthetic_transaction_generator.schemas.simulation_config import SimulationConfig
from synthetic_transaction_generator.transaction_generator.startup.generate_card_values import generate_card_values
from synthetic_transaction_generator.transaction_generator.startup.generate_recipient_ids import generate_recipient_ids
import random
import numpy as np

def initialise(config: SimulationConfig) -> tuple[dict[str, CardProfile], list[str]]:
    """Initialise card profiles and merchant id's"""

    random.seed(config.random_seed)
    np.random.seed(config.random_seed)

    cards = generate_card_values(config.n_cards)

    mule_ids = random.sample(list(cards.keys()), config.n_mule_accounts)
    for id in mule_ids:
        cards[id].is_mule = True

    recipients = generate_recipient_ids(config.n_recipients)

    return cards, recipients