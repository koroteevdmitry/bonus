from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class CustomerStatusEnum(str, Enum):
    vip = "vip"
    regular = "regular"
    unknown = "unknown"


class BonusCalculationRequest(BaseModel):
    transaction_amount: float
    timestamp: datetime
    customer_status: CustomerStatusEnum


class AppliedRule(BaseModel):
    rule: str
    bonus: float


class BonusCalculationResult(BaseModel):
    total_bonus: float
    applied_rules: list[AppliedRule]
