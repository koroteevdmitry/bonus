from dishka import Provider, Scope, provide

from bonus_service.app.application.bonus_service import BonusCalculator


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def bonus_calculator(self) -> BonusCalculator:
        return BonusCalculator(rules_path="bonus_service/app/adapters/config/rules.yaml")
