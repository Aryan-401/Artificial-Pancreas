from pydantic import BaseModel
from typing import List


class GlucagonSModel(BaseModel):
    G: float
    I: float
    dG: float


class GlucagenolysisSModel(BaseModel):
    C: List[float]
    t: int


class InsulinIndependentModel(BaseModel):
    G: float


class KidneyModel(BaseModel):
    G: float


class MealModel(BaseModel):
    t: int


class EGPModel(BaseModel):
    G6P: float
    dG: float
    G: float
    x3: float
