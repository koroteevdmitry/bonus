from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI

from bonus_service.app.application.bonus_service import BonusCalculator
from bonus_service.app.containers import Container
from bonus_service.app.domain.models import BonusCalculationRequest, BonusCalculationResult

container = Container()
container.config.rules_path.from_value("bonus_service/app/adapters/config/rules.yaml")
container.wire(modules=[__name__])

app = FastAPI()
app.container = container


@app.post("/calculate-bonus", response_model=BonusCalculationResult)
@inject
def calculate_bonus(
    request: BonusCalculationRequest,
    calculator: Annotated[BonusCalculator, Provide[Container.bonus_calculator]],
) -> BonusCalculationResult:
    return calculator.calculate(request)
