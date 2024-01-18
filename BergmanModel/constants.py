from pydantic import BaseModel, validator
from typing import List


class Constant:
    NUM_MEALS = 8
    I = 18.7813
    X = 0.0067
    G = 120.0
    t = 0.0
    h = 1.0

    p1 = 0.0337
    p2 = 0.0209
    p3 = 7.5 * pow(10, -6)
    tau = 0.083333
    n = 0.214
    Gb = 144.0

    u = 48.2328

    Ag = 0.8
    tmax_I = 33.0
    tmax_G = 24.0
    Vg = 13.79

    MAX_TIME = 1440

class ListMaxSize(BaseModel):
    inputs: List[float]
    max_size: int

    @validator('inputs')
    def check_max_size(cls, v, values, **kwargs):
        max_size = values.get('max_size')
        if max_size is not None and len(v) > max_size:
            raise ValueError(f'List size must be less than or equal to {max_size}\nGot {len(v)}')
        return v


