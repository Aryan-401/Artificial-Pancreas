from blocks.static.constants import Constants
from blocks.static.type_check import KidneyModel

c = Constants()


def kidney(data: KidneyModel) -> float:
    Ke1 = 0.003
    Ke2 = 162

    if G >= Ke2:
        y = Ke1 * (data.G - Ke2)
    else:
        y = 0

    return y
