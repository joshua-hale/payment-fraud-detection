from synthetic_transaction_generator.transaction_generator.startup.generate_recipient_ids import (
    generate_recipient_ids,
)


def test_returns_correct_count():
    recipients = generate_recipient_ids(500)
    assert len(recipients) == 500


def test_ids_are_unique():
    recipients = generate_recipient_ids(500)
    assert len(set(recipients)) == 500


def test_ids_are_well_formed():
    recipients = generate_recipient_ids(10)
    assert recipients[0] == "recipient_0000000"
    assert recipients[-1] == "recipient_0000009"
    assert all(r.startswith("recipient_") for r in recipients)


def test_zero_recipients_returns_empty_list():
    recipients = generate_recipient_ids(0)
    assert recipients == []


def test_large_count_still_zero_padded_correctly():
    recipients = generate_recipient_ids(1_000_001)
    # confirms 7-digit padding doesn't silently truncate at 1,000,000+
    assert recipients[1_000_000] == "recipient_1000000"