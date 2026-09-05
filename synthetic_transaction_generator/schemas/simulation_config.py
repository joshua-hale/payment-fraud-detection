from pydantic import BaseModel, Field
from recipient_pool_config import RecipientPoolConfig

class SimulationConfig(BaseModel):
    n_cards: int = 200_000
    fraud_rate: float = Field(default=0.025, ge=0, lt=1)
    n_mule_accounts: int = 500
    rate_multiplier: float = Field(default=1.0, gt=0)
    random_seed: int = 42
    recipient_pools: RecipientPoolConfig = Field(default_factory=RecipientPoolConfig)