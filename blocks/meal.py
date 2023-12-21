from static.constants import Constants
from static.type_check import Meal

c = Constants()


def meal(data: Meal) -> float:
    d1 = 12.42
    Dg1 = (1000 * d1) / 180
    d2 = 1.83
    Dg2 = (1000 * d2) / 180
    d3 = 3.45
    Dg3 = (1000 * d3) / 180
    # d4 = 3.85
    # Dg4=(1000*d4)/180
    # d5 = 3.45
    # Dg5=(1000*d5)/180

    if data.t < 210:
        y = 0
    elif 210 <= data.t < 220:
        y = Dg1
    # elif 390 <= t <= 410:
    elif 450 <= data.t <= 470:
        y = Dg2
    # elif 600 <= t <= 610:
    elif 690 <= data.t <= 700:
        y = Dg3
    # elif 765 <= t <= 785:
    #     y = Dg4
    # elif 900 <= t <= 910:
    #     y = Dg5
    else:
        y = 0

    return y
