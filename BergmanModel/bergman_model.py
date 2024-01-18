import numpy as np
import matplotlib.pyplot as plt
from constants import Constant, ListMaxSize
from math import exp, pow
from scipy.integrate import odeint

c = Constant()
default = {'inputs': [200, 400, 600, 800, 900, 1000, 1200, 1450], 'max_size': c.NUM_MEALS}  # mg/dl
mealTimes = ListMaxSize(**default)
default = {'inputs': [30, 20, 10, 40, 50, 30, 10, 50], 'max_size': c.NUM_MEALS}
Dg = ListMaxSize(**default)
default = {'inputs': [10, 10, 20, 10, 14, 20, 100, 20], 'max_size': c.NUM_MEALS}  # mu/l
u_meals = ListMaxSize(**default)


#  random values

def m_default(t: float) -> float:
    if t < 3600:
        m = 0.0
    else:
        if t < 14400:
            t = t - 3600
            m = 100 * 30.0 * c.Ag * t * exp(-t / c.tmax_I) / (c.Vg * pow(c.tmax_G, 2))
        else:
            if t < 25200:
                t = t - 14400
                m = 100 * 15.0 * c.Ag * t * exp(-t / c.tmax_I) / (c.Vg * pow(c.tmax_G, 2))
            else:
                if t < 50400:
                    t = t - 25200
                    m = 100 * 80.0 * c.Ag * t * exp(-t / c.tmax_I) / (c.Vg * pow(c.tmax_G, 2))
                else:
                    t = t - 50400
                    m = 100 * 60.0 * c.Ag * t * exp(-t / c.tmax_I) / (c.Vg * pow(c.tmax_G, 2))
    return m


def m_custom(t: float, numberOfMeals: int, mealTimes: ListMaxSize, Dg: ListMaxSize):
    m = 0
    for i in range(numberOfMeals):
        if t < mealTimes.inputs[i]:
            t = t - mealTimes.inputs[i - 1]
            m = 100 * Dg.inputs[i] * c.Ag * t * exp(-t / c.tmax_I) / (c.Vg * pow(c.tmax_G, 2))  # why multiply by 100
            return m


def u_custom(t: float, numberOfMeals: int, mealTimes: ListMaxSize, u_meals: ListMaxSize):
    for i in range(numberOfMeals):
        if t < mealTimes.inputs[i]:
            return u_meals.inputs[i]


def bergman_model(y, t, c, p1, p2, p3, tau, n, Gb):
    G, I, X = y
    dGdt = -1 * (p1 + X) * G + p1 * Gb + m_default(t)
    dXdt = -1 * p2 * X + p3 * I
    dIdt = -1 * n * I + tau * u_custom(t, mealTimes.max_size, mealTimes, u_meals)
    c.G, c.I, c.X = dGdt, dIdt, dXdt
    return [dGdt, dIdt, dXdt]


if __name__ == '__main__':
    t_points = np.arange(c.t, 1440, c.h)
    y = [c.G, c.I, c.X]
    solution = odeint(bergman_model, y, t_points, args=(c, c.p1, c.p2, c.p3, c.tau, c.n, c.Gb))
    G, I, X = solution.T
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12))
    ax1.plot(t_points, G, label='Plasma Glucose')
    ax1.set_title('Glucose Concentration (mg/dl)')
    ax1.legend()
    ax2.plot(t_points, I, label='Plasma Insulin')
    ax2.set_title('Insulin Concentration (mu/l)')
    ax2.legend()
    ax3.plot(t_points, X, label='Subcutaneous Insulin (min-1)')
    ax3.set_title('Subcutaneous Insulin Concentration')
    ax3.legend()

    plt.tight_layout()
    plt.show()

