from dishka import FromDishka, make_async_container
from dishka.integrations.fastapi import inject, setup_dishka
from fastapi import FastAPI

from bonus_service.app.application.bonus_service import BonusCalculator
from bonus_service.app.domain.models import BonusCalculationRequest, BonusCalculationResult
from bonus_service.app.providers import AppProvider

container = make_async_container(AppProvider())

app = FastAPI()
setup_dishka(container, app)


@app.post("/calculate-bonus", response_model=BonusCalculationResult)
@inject
def calculate_bonus(
    calculator: FromDishka[BonusCalculator],
    request: BonusCalculationRequest,
) -> BonusCalculationResult:
    return calculator.calculate(request)
