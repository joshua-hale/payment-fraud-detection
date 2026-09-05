def generate_recipient_ids(n_recipients: int) -> list[str]:
    """Generate the specified number of recipient ids"""

    recipients = []

    for n in range(n_recipients):
        recipients.append(f"recipient_{n:07d}")

    return recipients