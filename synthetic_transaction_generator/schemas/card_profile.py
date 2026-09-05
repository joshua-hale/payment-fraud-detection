from pydantic import BaseModel, Field

class CardProfile(BaseModel):
    card_id: str
    home_location: str
    avg_amount: float = Field(gt=0)
    merchant_categories: list[str]
    avg_daily_transactions: float
    current_balance: float
