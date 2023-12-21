from static.constants import Constants
from static.type_check import GlucagenolysisSModel
from math import tanh

c = Constants()


def GlucagenolysisS(data: GlucagenolysisSModel) -> float:
    Gb = c.Gb  # mg/dL
    # Ggnb = c.Ggnb
    GggB = 0.7425  # mg / dL / min
    Sc = 297  # mg/dl/mim per mg/dl # TODO: mim? or min
    Cth = 80 * 10 ** -7  # mg/dl
    K6GP = c.K6GP  # / min
    tD = 59.90  # min
    tau = 23.24  # min
    kp2 = c.KP2  # / min

    E = 0.5 * (1 - tanh((data.t - tD) / tau))
    Ggg = [(GggB + (Sc * max(0, (C_item - Cth)))) * E for C_item in data.C]
    return Ggg
