from blocks.static.constants import Constants
from blocks.static.type_check import EGPModel

c = Constants()


def EGP(data: EGPModel) -> float:
    # Parameter values
    Gb = c.Gb  # mg/dL
    # Ggnb = 0.495 ;        %mg/dL/min
    Gggb = 0.7425  # mg/dL/min
    Sc = 306  # mg/dl/mim per mg/dl
    Cth = 80 * 10 ** (-7)  # mg/dL
    K6GP = c.K6GP  # /min
    tD = 59.90  # min
    tau = 23.24  # min
    kp2 = c.KP2  # mg/dL

    # if G <= Gb
    # E = 1/2 * (1 - np.tanh((t - tD) / tau))
    # Ggg = Gggb + (Sc * np.maximum(0, (C - Cth)) * E)

    if data.dG >= 0:
        y = K6GP * data.G6P - kp2 * (data.G - Gb) - data.x3 * data.dG
        # y = K6GP * G6P
        # y = Gggb + Ggg - x3 * dG - kp2 * (G - Gb) - x3 * (G - Gb)
        # y = Gggb + x3 * Ggg - x3 * dG - kp2 * (G - Gb)
    else:
        y = K6GP * data.G6P - kp2 * (data.G - Gb)
        # y = Gggb + Ggg - kp2 * (G - Gb) - x3 * (G - Gb)
        # y = Gggb + x3 * Ggg - kp2 * (G - Gb)

    # else:
    #     if dG >= 0:
    #         y = Gggb + Ggg - x3 * dG - kp2 * (G - Gb) - x3 * (G - Gb)
    #         y = Gggb - x3 * dG - kp2 * (G - Gb)
    #     else:
    #         y = Gggb + Ggg - kp2 * (G - Gb) - x3 * (G - Gb)
    #         y = Gggb - kp2 * (G - Gb)

    return y
