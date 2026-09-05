import pytest

from synthetic_transaction_generator.schemas.simulation_config import SimulationConfig
from synthetic_transaction_generator.transaction_generator.startup.initialise import (
    initialise,
)


def make_config(**overrides) -> SimulationConfig:
    defaults = dict(n_cards=1000, n_recipients=200, n_mule_accounts=50, random_seed=42)
    defaults.update(overrides)
    return SimulationConfig(**defaults)


def test_returns_correct_card_and_recipient_counts():
    config = make_config()
    cards, recipients = initialise(config)
    assert len(cards) == config.n_cards
    assert len(recipients) == config.n_recipients


def test_correct_number_of_mules_assigned():
    config = make_config(n_cards=1000, n_mule_accounts=50)
    cards, _ = initialise(config)
    mule_count = sum(1 for c in cards.values() if c.is_mule)
    assert mule_count == 50


def test_mule_ids_are_distinct():
    config = make_config(n_cards=1000, n_mule_accounts=50)
    cards, _ = initialise(config)
    mule_ids = [cid for cid, c in cards.items() if c.is_mule]
    assert len(mule_ids) == len(set(mule_ids))


def test_zero_mule_accounts_flags_nobody():
    config = make_config(n_mule_accounts=0)
    cards, _ = initialise(config)
    assert all(not c.is_mule for c in cards.values())


def test_all_cards_can_be_mules():
    config = make_config(n_cards=20, n_mule_accounts=20)
    cards, _ = initialise(config)
    assert all(c.is_mule for c in cards.values())


def test_seeding_produces_identical_mule_selection():
    config = make_config(n_cards=500, n_mule_accounts=25, random_seed=7)

    cards_a, _ = initialise(config)
    cards_b, _ = initialise(config)

    mules_a = {cid for cid, c in cards_a.items() if c.is_mule}
    mules_b = {cid for cid, c in cards_b.items() if c.is_mule}
    assert mules_a == mules_b


def test_seeding_produces_identical_profiles_end_to_end():
    config = make_config(random_seed=99)

    cards_a, recipients_a = initialise(config)
    cards_b, recipients_b = initialise(config)

    assert recipients_a == recipients_b
    for card_id in cards_a:
        assert cards_a[card_id].model_dump() == cards_b[card_id].model_dump()