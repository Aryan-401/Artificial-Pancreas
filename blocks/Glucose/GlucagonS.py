from blocks.static.constants import Constants
from blocks.static.type_check import GlucagonSModel


c = Constants()


def GlucagonS(data: GlucagonSModel) -> float:
    Gb = c.Gb
    Gth = 60  # not set in constants.py
    P = 0.86  # not set in constants.py
    sigma = 1 / (10 ** 9 * 6.945 * c.VI)  # not set in constants.py
    delta = 0.98  # not set in constants.py
    SRhb = c.n * c.Hb
    SRhs = SRhb

    if data.G >= Gb:
        SRhs = P * (SRhs - SRhb)
    else:
        SRhs = P * (SRhs - max(((sigma * (Gth - data.G) / (data.I + 1)) + SRhb), 0))

    SRhd = delta * max(-1 * data.dG, 0)
    SRh = SRhs + SRhd
    return SRh
