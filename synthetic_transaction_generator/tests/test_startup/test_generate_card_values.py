import numpy as np
import pytest

from synthetic_transaction_generator.transaction_generator.startup.generate_card_values import (
    generate_card_values,
)


def test_returns_correct_count():
    cards = generate_card_values(100)
    assert len(cards) == 100


def test_card_ids_are_unique_and_well_formed():
    cards = generate_card_values(100)
    assert len(set(cards.keys())) == 100
    assert all(cid.startswith("card_") for cid in cards)
    assert list(cards.keys())[0] == "card_000000"
    assert list(cards.keys())[-1] == "card_000099"


def test_card_id_field_matches_dict_key():
    cards = generate_card_values(50)
    for card_id, card in cards.items():
        assert card.card_id == card_id


def test_field_ranges_are_valid():
    cards = generate_card_values(2000)
    for card in cards.values():
        lat, lon = card.home_location
        assert -90 <= lat <= 90
        assert -180 <= lon <= 180
        assert 0 < card.spend_fraction <= 0.5
        assert card.activity_weight > 0
        assert 500 <= card.current_balance <= 100_000
        assert card.is_mule is False


def test_zero_cards_returns_empty_dict():
    cards = generate_card_values(0)
    assert cards == {}


def test_seeding_produces_identical_cards():
    np.random.seed(42)
    cards_a = generate_card_values(50)

    np.random.seed(42)
    cards_b = generate_card_values(50)

    assert cards_a.keys() == cards_b.keys()
    for card_id in cards_a:
        assert cards_a[card_id].model_dump() == cards_b[card_id].model_dump()


def test_different_seeds_produce_different_cards():
    np.random.seed(1)
    cards_a = generate_card_values(50)

    np.random.seed(2)
    cards_b = generate_card_values(50)

    # not every field needs to differ, but at least one card should
    assert any(
        cards_a[cid].model_dump() != cards_b[cid].model_dump() for cid in cards_a
    )
