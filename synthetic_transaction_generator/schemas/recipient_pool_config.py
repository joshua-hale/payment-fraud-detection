from pydantic import BaseModel

class RecipientPoolConfig(BaseModel):
    n_recipients: int = 1_000_000


