from synthetic_transaction_generator.transaction_generator.dispatcher.pick_recipient import pick_recipient
from synthetic_transaction_generator.schemas.card_profile import CardProfile
from synthetic_transaction_generator.schemas.transaction_type import TransactionType
import pytest

def make_card_profile(card_id: str) -> CardProfile:
    return CardProfile(
        card_id=card_id,
        home_location=(0.0, 0.0),
        spend_fraction=0.05,
        activity_weight=1.0,
        current_balance=1000.0,
        is_mule=False,
    )

@pytest.fixture
def sample_cards() -> dict[str, CardProfile]:
    cards = {}
    for id in ["card_000000", "card_000001", "card_000002"]:
        cards[id] = make_card_profile(id)

    return cards

@pytest.fixture
def sample_merchants() -> list[str]:
    return ["merchant_0000000", "merchant_0000001"]

def test_payment_returns_a_merchant(sample_cards, sample_merchants):
    for i in range(50):
        recipient = pick_recipient(TransactionType.PAYMENT, "card_000000", sample_cards, sample_merchants)
        assert recipient in sample_merchants

def test_transfer_returns_a_card(sample_cards, sample_merchants):
    for _ in range(50):
        recipient = pick_recipient(TransactionType.TRANSFER, "card_000000", sample_cards, sample_merchants)
        assert recipient in sample_cards


def test_transfer_never_returns_the_sender(sample_cards, sample_merchants):
    for _ in range(200):
        recipient = pick_recipient(TransactionType.TRANSFER, "card_000000", sample_cards, sample_merchants)
        assert recipient != "card_000000"


def test_cash_out_never_returns_the_sender(sample_cards, sample_merchants):
    for _ in range(200):
        recipient = pick_recipient(TransactionType.CASH_OUT, "card_000000", sample_cards, sample_merchants)
        assert recipient != "card_000000"


def test_transfer_with_only_two_cards_still_terminates(sample_merchants):
    # regression guard: with exactly 2 cards, the self-exclusion while-loop
    # must still be able to pick the other card and terminate
    two_cards = {cid: make_card_profile(cid) for cid in ["card_000000", "card_000001"]}
    recipient = pick_recipient(TransactionType.TRANSFER, "card_000000", two_cards, sample_merchants)
    assert recipient == "card_000001"
