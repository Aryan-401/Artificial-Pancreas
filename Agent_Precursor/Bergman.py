import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from math import exp, pow
from constants import Constant, ListMaxSize

c = Constant()

t = np.linspace(0, 1440, 1441)
Gb = 92
Ib = 7.3
Xb = 0.00
G0 = 258
x_ext = 0.000
y0 = [Gb + G0, Xb, Ib]

params = (0.03082, 0.014, 1.062e-5, 0.3, 100, 0.003349, Gb, Ib)

meal_dict = {'inputs': [200, 400, 600, 800, 900, 1000, 1200, 1450], 'max_size': c.NUM_MEALS}
mealTimes = ListMaxSize(**meal_dict)
u_dict = {'inputs': [10, 10, 20, 10, 14, 20, 100, 20], 'max_size': c.NUM_MEALS}  # mu/l
u_meals = ListMaxSize(**u_dict)


def u_custom(t):
    for i in range(c.NUM_MEALS):
        if t <= mealTimes.inputs[i]:
            return u_meals.inputs[i]
    else:
        return c.u

def odes(y, t, args):
    p1, p2, p3, n, h, gamma, Gb, Ib = args

    G = y[0]
    X = y[1]
    I = y[2]

    dGdt = -(p1 + X) * G + (p1 * Gb)
    dXdt = -(p2 * X) + p3 * (I - Ib)
    dIdt = gamma * (G - h) * t - n * (I - Ib)
    if G < h:
        dIdt = -n * (I - Ib)

    return [dGdt, dXdt, dIdt]


y = odeint(odes, y0, t, args=(params,))

G = y[:, 0]
X = y[:, 1]
I = y[:, 2]

plt.axhline(y=Gb, color='g', linestyle='--', label="Gb")
plt.plot(t, G, 'g', label="Normal Glucose")
plt.legend()
plt.show()
