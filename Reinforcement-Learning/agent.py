from constants import Constant, ListMaxSize
from math import exp, pow
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class Body:
    def __init__(self, mealTimes: ListMaxSize, u_meals: ListMaxSize, Dg: ListMaxSize):
        self.c = Constant()
        self.G, self.I, self.X = self.c.G, self.c.I, self.c.X
        self.t = 0
        self.p1 = self.c.p1
        self.p2 = self.c.p2
        self.p3 = self.c.p3
        self.tau = self.c.tau
        self.n = self.c.n
        self.Gb = self.c.Gb
        self.mealTimes = mealTimes
        self.u_meals = u_meals
        self.Dg = Dg

    def m_default(self, t: float) -> float:
        if t < 3600:
            m = 0.0
        else:
            if t < 14400:
                t = t - 3600
                m = 100 * 30.0 * self.c.Ag * t * exp(-t / self.c.tmax_I) / (self.c.Vg * pow(self.c.tmax_G, 2))
            else:
                if t < 25200:
                    t = t - 14400
                    m = 100 * 15.0 * self.c.Ag * t * exp(-t / self.c.tmax_I) / (self.c.Vg * pow(self.c.tmax_G, 2))
                else:
                    if t < 50400:
                        t = t - 25200
                        m = 100 * 80.0 * self.c.Ag * t * exp(-t / self.c.tmax_I) / (self.c.Vg * pow(self.c.tmax_G, 2))
                    else:
                        t = t - 50400
                        m = 100 * 60.0 * self.c.Ag * t * exp(-t / self.c.tmax_I) / (self.c.Vg * pow(self.c.tmax_G, 2))
        return m

    def m_custom(self, t):
        m = 0
        for i in range(self.c.NUM_MEALS):
            if t < self.mealTimes.inputs[i]:
                t = t - self.mealTimes.inputs[i - 1]
                m = 100 * self.Dg.inputs[i] * self.c.Ag * t * exp(-t / self.c.tmax_I) / (
                        self.c.Vg * pow(self.c.tmax_G, 2))
                return m

    def u_custom(self, t):
        for i in range(self.c.NUM_MEALS):
            if t < mealTimes.inputs[i]:
                return u_meals.inputs[i]

    def bergman_model(self, y, t):
        self.G, self.I, self.X = y
        self.G = -1 * (self.c.p1 + self.X) * self.G + self.c.p1 * self.c.Gb + self.m_default(t)
        self.X = -1 * self.c.p2 * self.X + self.c.p3 * self.I
        self.I = -1 * self.c.n * self.I + self.c.tau * self.u_custom(t)
        return [self.G, self.I, self.X]

    def get_graph(self):
        t_points = np.arange(0, 1441, self.c.h)
        y = [self.G, self.I, self.X]
        solution = odeint(self.bergman_model, y, t_points)
        self.G, self.I, self.X = solution.T
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12))
        ax1.plot(t_points, self.G, label='Plasma Glucose')
        ax1.set_title('Glucose Concentration (mg/dl)')
        ax1.legend()
        ax2.plot(t_points, self.I, label='Plasma Insulin')
        ax2.set_title('Insulin Concentration (mu/l)')
        ax2.legend()
        ax3.plot(t_points, self.X, label='Subcutaneous Insulin')
        ax3.set_title('Subcutaneous Insulin Concentration (min-1)')
        ax3.legend()
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    c = Constant()
    meal_dict = {'inputs': [200, 400, 600, 800, 900, 1000, 1200, 1450], 'max_size': c.NUM_MEALS}
    mealTimes = ListMaxSize(**meal_dict)
    dg_dict = {'inputs': [30, 20, 10, 40, 50, 30, 10, 50], 'max_size': c.NUM_MEALS}
    Dg = ListMaxSize(**dg_dict)
    u_dict = {'inputs': [10, 10, 20, 10, 14, 20, 100, 20], 'max_size': c.NUM_MEALS}
    u_meals = ListMaxSize(**u_dict)
    body = Body(mealTimes, u_meals, Dg)
    body.get_graph()

