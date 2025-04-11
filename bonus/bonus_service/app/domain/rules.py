from abc import ABC, abstractmethod

from bonus_service.app.domain.models import AppliedRule, BonusCalculationRequest


class BonusRule(ABC):
    def __init__(self):
        self._next = None

    def set_next(self, next_rule: "BonusRule") -> "BonusRule":
        self._next = next_rule
        return next_rule

    def apply(self, request: BonusCalculationRequest, current_bonus: float, result: list) -> float:
        new_bonus, rule_applied = self._apply_rule(request, current_bonus)
        if rule_applied:
            result.append(rule_applied)
        if self._next:
            return self._next.apply(request, new_bonus, result)
        return new_bonus

    @abstractmethod
    def _apply_rule(self, request: BonusCalculationRequest, current_bonus: float) -> tuple[float, AppliedRule | None]:
        pass
