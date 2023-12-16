from static.constants import Constants

c = Constants()


def GlucagonS(G, I, dG):
    Gb = c.Gb
    Gth = 60  # not set in constants.py
    P = 0.86  # not set in constants.py
    sigma = 1 / (10 ** 9 * 6.945 * c.VI)  # not set in constants.py
    delta = 0.98  # not set in constants.py
    SRhb = c.n * c.Hb
    SRhs = SRhb

    if G >= Gb:
        SRhs = P * (SRhs - SRhb)
    else:
        SRhs = P * (SRhs - max(((sigma * (Gth - G) / (I + 1)) + SRhb), 0))

    SRhd = delta * max(-dG, 0)
    SRh = SRhs + SRhd
    return SRh
