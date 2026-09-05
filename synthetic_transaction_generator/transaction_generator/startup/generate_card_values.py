from synthetic_transaction_generator.schemas.card_profile import CardProfile
import random
import numpy as np

def generate_card_values(n_cards: int) -> dict[str, CardProfile]:
    """Generate the specified number of card profiles keyed by card_id"""
    
    cards = {}

    for n in range(n_cards):
        card_id = f"card_{n:06d}"
        cards[card_id] = CardProfile(
            card_id=card_id,
            home_location=(np.random.uniform(-90,90), np.random.uniform(-180,180)),
            spend_fraction = float(np.random.beta(a=1, b=19)),
            activity_weight = float(np.random.pareto(a=2.0) + 1.0),
            current_balance=(np.random.uniform(500,100000)),
            is_mule=False
        )

    return cards
    
        
