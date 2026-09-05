from pydantic import BaseModel, Field

class SimulationConfig(BaseModel):
    n_cards: int = 200_000
    n_recipients: int = 1_000_000
    fraud_rate: float = Field(default=0.025, ge=0, lt=1)
    n_mule_accounts: int = 500
    rate_multiplier: float = Field(default=1.0, gt=0)
    random_seed: int = 42
