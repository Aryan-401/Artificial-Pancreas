from static.constants import Constants
from static.type_check import Kidney

c = Constants()


def kidney(data: Kidney) -> float:
    Ke1 = 0.003
    Ke2 = 162

    if G >= Ke2:
        y = Ke1 * (data.G - Ke2)
    else:
        y = 0

    return y
