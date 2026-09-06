import numpy as np
from synthetic_transaction_generator.schemas.transaction_type import TransactionType
from synthetic_transaction_generator.schemas.card_profile import CardProfile

def pick_recipient(
        transaction_type: TransactionType,
        sender_card_id: str,
        cards: dict[str, CardProfile],
        merchants: list[str]
) -> str:
    """
    Pick a random recipient depending on transaction type
    (merchant or another valid card_id)
    """

    # PAYMENT - recipient is a merchant
    if transaction_type == TransactionType.PAYMENT:
        return str(np.random.choice(merchants))
    
    # TRANSFER / CASH_OUT - recipient is another real card
    card_ids = list(cards.keys())
    recipient = str(np.random.choice(card_ids))
    while recipient == sender_card_id:
        recipient = str(np.random.choice(card_ids))
    return recipient