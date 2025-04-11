from dependency_injector import containers, providers

from bonus_service.app.application.bonus_service import BonusCalculator


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    bonus_calculator = providers.Singleton(BonusCalculator, rules_path=config.rules_path)
