from static.constants import Constants
from static.type_check import InsulinIndependent
c = Constants()


def insulin_independent(data: InsulinIndependent) -> float:
    F01 = 18 * ((0.00097 * 70) / (0.12 * 70))

    if data.G >= 81:
        y = F01
    else:
        y = F01 * (data.G / 81)

    return y
