import random


class Constants:
    def __init__(self):
        self.I = 0.054
        self.X = 0.0067
        self.G = 120.0
        self.t = 0.0
        self.h = 1.0

        self.p1 = 0.0337
        self.p2 = 0.0209
        self.p3 = 7.5 * pow(10, -6)
        self.tau = 0.083333
        self.n = 0.214
        self.Gb = 144.0

        self.u = 0.054

        self.Ag = 0.8
        self.tmax_I = 33.0
        self.tmax_G = 24.0
        self.Vg = 13.79

        self.MAX_TIME = 1440
        self.MAX_INSULIN = 50
        self.INSULIN_PUMP_RATE = 15 #min
        self.MAX_OVERSHOOT_CONS = 20

    def __str__(self):
        return f"Constants(I={self.I}, X={self.X}, G={self.G}, t={self.t}, h={self.h}, p1={self.p1}, p2={self.p2}, p3={self.p3}, tau={self.tau}, n={self.n}, Gb={self.Gb}, u={self.u}, Ag={self.Ag}, tmax_I={self.tmax_I}, tmax_G={self.tmax_G}, Vg={self.Vg}, MAX_TIME={self.MAX_TIME}, MAX_INSULIN={self.MAX_INSULIN}, INSULIN_PUMP_RATE={self.INSULIN_PUMP_RATE})"

    def add_randomness(self, value):
        percentage_change = random.uniform(-0.2, 0.2)  # Generates a random percentage change between -20% and +20%
        random_value = value + (value * percentage_change)
        return random_value

    def randomise_constants(self):
        self.I = self.add_randomness(0.054)
        self.X = self.add_randomness(0.0067)
        self.G = self.add_randomness(120.0)

        self.p1 = self.add_randomness(0.0337)
        self.p2 = self.add_randomness(0.0209)
        self.p3 = self.add_randomness(7.5 * pow(10, -6))
        self.tau = self.add_randomness(0.083333)
        self.n = self.add_randomness(0.214)
        self.Gb = self.add_randomness(144.0)

        self.u = self.add_randomness(0.054)

        self.Ag = self.add_randomness(0.8)
        self.tmax_I = self.add_randomness(33.0)
        self.tmax_G = self.add_randomness(24.0)
        self.Vg = self.add_randomness(13.79)

    def set_values(self, dict_):
        self.I = dict_['I']
        self.X = dict_['X']
        self.G = dict_['G']
        self.p1 = dict_['p1']
        self.p2 = dict_['p2']
        self.p3 = dict_['p3']
        self.tau = dict_['tau']
        self.n = dict_['n']
        self.Gb = dict_['Gb']
        self.u = dict_['u']
        self.Ag = dict_['Ag']
        self.tmax_I = dict_['tI']
        self.tmax_G = dict_['tG']
        self.Vg = dict_['Vg']