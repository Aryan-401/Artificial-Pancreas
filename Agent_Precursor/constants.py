from pydantic import BaseModel, root_validator
from typing import List


class Constant:
    NUM_MEALS = 8
    I = 18.7813
    X = 0.0067
    G = 120.0
    h = 1
    u = 48.2328
    MAX_TIME = 1440

    MAX_G = 120
    MIN_G = 70

    p1 = 0.0337
    p2 = 0.0209
    p3 = 7.5 * pow(10, -6)
    tau = 0.083333
    n = 0.214
    Gb = 144.0

    # u = 48.2328

    Ag = 0.8
    tmax_I = 33.0
    tmax_G = 24.0
    Vg = 13.79

class ListMaxSize(BaseModel):
    inputs: List[float]
    max_size: int

    @root_validator(pre=True)  # Execute this validator before other validations
    def check_inputs_size(cls, values):
        inputs = values.get("inputs")
        max_size = values.get("max_size")
        if inputs and len(inputs) > max_size:
            raise ValueError("inputs list size exceeds max_size")
        if inputs and len(inputs) < max_size:
            inputs.extend([0] * (max_size - len(inputs)))

        return values
