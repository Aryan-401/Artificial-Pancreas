from pydantic import BaseModel
from typing import List


class GlucagonSModel(BaseModel):
    G: float
    I: float
    dG: float


class GlucagenolysisSModel(BaseModel):
    C: List[float]
    t: int


class InsulinIndependent(BaseModel):
    G: float


class Kidney(BaseModel):
    G: float


class Meal(BaseModel):
    t: int


class EGP(BaseModel):
    G6P: float
    dG: float
    G: float
    x3: float
