import yaml

from bonus_service.app.core.datetime_utils import is_weekend_or_holiday
from bonus_service.app.domain.models import AppliedRule, BonusCalculationRequest, BonusCalculationResult
from bonus_service.app.domain.rules import BonusRule


class RuleFactory:
    @staticmethod
    def create_rule(rule_def: dict) -> BonusRule:
        name = rule_def["name"]
        rule_type = rule_def["type"]
        cfg = rule_def.get("config", {})
        condition = rule_def.get("condition")

        class BaseRule(BonusRule):
            def _apply_rule(self, request, current_bonus) -> (float, AppliedRule):
                unit = cfg.get("per_amount", 10)
                bonus_per_unit = cfg.get("bonus", 1)
                bonus = int(request.transaction_amount / unit) * bonus_per_unit
                return bonus, AppliedRule(rule=name, bonus=bonus)

        class MultiplierRule(BonusRule):
            def _apply_rule(self, request, current_bonus) -> (float, AppliedRule):
                if condition == "is_weekend_or_holiday" and not is_weekend_or_holiday(request.timestamp):
                    return current_bonus, None
                if condition == "is_vip" and request.customer_status.lower() != "vip":
                    return current_bonus, None
                multiplier = cfg.get("multiplier", 1)
                bonus = current_bonus * multiplier
                return bonus, AppliedRule(rule=name, bonus=bonus - current_bonus)

        if rule_type == "base":
            return BaseRule()
        elif rule_type == "multiplier":
            return MultiplierRule()
        else:
            raise ValueError(f"Unknown rule type: {rule_type}")


class BonusCalculator:
    def __init__(self, rules_path: str):
        self.rules_path = rules_path

    def calculate(self, request: BonusCalculationRequest) -> BonusCalculationResult:
        with open(self.rules_path) as f:
            rule_defs = yaml.safe_load(f)["rules"]

        base_rule_def = next(r for r in rule_defs if r["type"] == "base")
        base_rule = RuleFactory.create_rule(base_rule_def)

        chain_rules = sorted([r for r in rule_defs if r["type"] != "base"], key=lambda x: x["order"])
        current = base_rule
        for rule_def in chain_rules:
            next_rule = RuleFactory.create_rule(rule_def)
            current.set_next(next_rule)
            current = next_rule

        applied = []
        total_bonus = round(base_rule.apply(request, 0, applied), 2)

        for r in applied:
            r.bonus = round(r.bonus, 2)

        return BonusCalculationResult(total_bonus=total_bonus, applied_rules=applied)
