from constants import Constant
from math import exp, pow
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import streamlit as st


class Body():

    def meal_function(self, dg: list, meal_time: list, c, t):
        m = 0
        for i in range(len(dg)):
            if i < len(dg) - 1 and t >= meal_time[i] and t < meal_time[i + 1]:
                t = t - meal_time[i]
                m = (100 * dg[i] * c.Ag * t * exp(-t / c.tmax_I)) / (c.Vg * (pow(c.tmax_G, 2)))
        return m

    def u_custom(self,t, meal_time: list, u_quantity: list, c):
        insulin_time = meal_time
        for i in range(len(insulin_time)):
            if i < len(insulin_time) and t >= insulin_time[i] and t < insulin_time[i + 1]:
                return u_quantity[i]
            
            return c.u

    def bergman_model(self,y, t, c, meal_time,insulin_time, u_quantity, Dg):
        G, I, X = y
        G = -1 * (c.p1 + X) * G + c.p1 * c.Gb + self.meal_function(Dg, meal_time, c, t)
        X = -1 * (c.p2 * X) + (c.p3 * I)
        I = -1 * (c.n * I) + (c.tau * self.u_custom(t, insulin_time, u_quantity, c))
        return [G, I, X]

    def get_graph(self,c, meal_time,insulin_time, u_quantity, Dg):
        t_points = np.arange(0, c.MAX_TIME, c.h)
        y = [c.G, c.I, c.X]
        solution = odeint(self.bergman_model, y, t_points, args=(c, meal_time,insulin_time, u_quantity, Dg))
        G, I, X = solution.T
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))
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
        plt.tight_layout()
        st.pyplot(fig)

    
