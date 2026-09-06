import uuid
from pydantic import BaseModel, Field
from fraud_type import FraudType

class TransactionEvent(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float
    card_id: str
    merchant_id: str
    transaction_type: str
    amount: float = Field(gt=0)
    balance_before: float = Field(ge=0)
    balance_after: float = Field(ge=0)
    dest_balance_before: float = Field(ge=0)
    dest_balance_after: float = Field(ge=0)
    location: tuple[float, float]
    merchant_category: int
    is_fraud: bool
    fraud_pattern: FraudType = FraudType.NONE

    model_config = {'use_enum_values': True}

