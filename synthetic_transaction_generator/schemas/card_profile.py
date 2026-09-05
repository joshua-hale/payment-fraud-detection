from pydantic import BaseModel, Field

class CardProfile(BaseModel):
    card_id: str
    home_location: tuple[float, float]
    spend_fraction: float = Field(gt=0)
    activity_weight: float 
    current_balance: float
    is_mule: bool = False
