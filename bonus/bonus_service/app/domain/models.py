from datetime import datetime

from pydantic import BaseModel


class BonusCalculationRequest(BaseModel):
    transaction_amount: float
    timestamp: datetime
    customer_status: str


class AppliedRule(BaseModel):
    rule: str
    bonus: float


class BonusCalculationResult(BaseModel):
    total_bonus: float
    applied_rules: list[AppliedRule]
