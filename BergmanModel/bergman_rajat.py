from constants import Constant
from math import exp, pow
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


def meal_function(dg: list, meal_time: list,c,t):
    m=0
    for i in range(len(dg)):
        
        if i < len(dg) - 1 and t >= meal_time[i] and t < meal_time[i + 1]:
            t= t- meal_time[i]
            m= (100 * dg[i] * c.Ag * t * exp(-t/ c.tmax_I)) / (c.Vg *(pow(c.tmax_G, 2)))
    return m

def u_custom(t, insulin_time: list, u_quantity: list, c):
    for i in range(c.NUM_MEALS):
        if t <= insulin_time[i]:
            return u_quantity[i]
    else:
        return c.u

def bergman_model(y, t, c, meal_time, u_quantity, Dg):
    G, I, X = y
    G = -1 * (c.p1 + X) * G + c.p1 * c.Gb + meal_function(Dg, meal_time, c, t)
    X = -1 * (c.p2 * X) + (c.p3 * I)
    I = -1 * (c.n * I) + (c.tau * u_custom(t, meal_time, u_quantity, c))
    return [G, I, X]

def get_graph(c, meal_time, u_quantity, Dg):
    t_points = np.arange(0, c.MAX_TIME, c.h)
    y = [c.G, c.I, c.X]
    solution = odeint(bergman_model, y, t_points, args=(c, meal_time, u_quantity, Dg))
    G, I, X = solution.T
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))
    ax1.plot(t_points, G, label='Plasma Glucose')
    ax1.set_title('Glucose Concentration (mg/dl)')
    ax1.legend()
    ax2.plot(t_points, I, label='Plasma Insulin')
    ax2.set_title('\nInsulin Concentration (mu/l)')
    ax2.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    c = Constant()
    meal_time = [200, 400, 600, 800, 900, 1000, 1200,1300]
    Dg = [30, 20, 10, 40, 50, 30, 10, 50]

    u_quantity = [10, 10, 20, 10, 14, 20, 100, 20]
    insulin_time = [200, 400, 600, 800, 900, 1000, 1200, 1300]

    get_graph(c, meal_time,u_quantity, Dg)
