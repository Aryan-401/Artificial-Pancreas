from typing import List
import numpy as np
import math
from math import pow, exp
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import streamlit as st
from constants import Constants

class Body:

    def __init__(self):
        self.constants = Constants()

    def meal_function(self, dg: List[float], meal_time: List[float], c, t):
        m = 0
        for i in range(len(dg)):
            if i < len(dg) - 1 and t >= meal_time[i] and t < meal_time[i + 1]:
                t = t - meal_time[i]
                m = (100 * dg[i] * c.Ag * t * math.exp(-t / c.tmax_I)) / (c.Vg * (pow(c.tmax_G, 2)))
        return m

    def u_custom(self, t, insulin_time, u_quantity: List[float], c):
        for i in range(len(insulin_time)):
            if t >= insulin_time[i] and t < insulin_time[i + 1]:
                return u_quantity[i]
        else:
            return c.u

    def bergman_model(self, y, t, c, meal_time, insulin_time, u_quantity, Dg):
        G, I, X = y
        G = -1 * (c.p1 + X) * G + c.p1 * c.Gb + self.meal_function(Dg, meal_time, c, t)
        X = -1 * (c.p2 * X) + (c.p3 * I)
        I = -1 * (c.n * I) + (c.tau * self.u_custom(t, insulin_time, u_quantity, c))
        return [G, I, X]

    def get_graph(self, meal_time, insulin_time, u_quantity, Dg):
        t_points = np.arange(0, self.constants.MAX_TIME, self.constants.h)
        y = [self.constants.G, self.constants.I, self.constants.X]
        solution = odeint(self.bergman_model, y, t_points,
                          args=(self.constants, meal_time, insulin_time, u_quantity, Dg))
        G, I, X = solution.T
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 18))
        
        ax1.plot(t_points, G, label='Plasma Glucose')
        ax1.set_title('Glucose Profile')
        ax1.legend()
        ax1.set_xlabel('Time(seconds)')
        ax1.set_ylabel('Glucose Concentration(mg/dl)')

        ax2.plot(t_points, I, label='Plasma Insulin')
        ax2.set_title('\nInsulin Profile')
        ax2.legend()
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Insulin Concentration(mu/l)')

        # ax3.plot(t_points, X, label='X')
        # ax3.set_title('\nX Profile')
        # ax3.legend()
        # ax3.set_xlabel('Time')
        # ax3.set_ylabel('X Values')
        
        plt.tight_layout()
        st.pyplot(fig)