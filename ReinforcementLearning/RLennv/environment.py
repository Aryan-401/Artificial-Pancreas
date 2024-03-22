from gymnasium import Env
from gymnasium.spaces import Box
from ReinforcementLearning.RLennv.Constants import Constants
import numpy as np
from scipy.integrate import odeint
from math import exp


class Bergman(Env):
    def __init__(self, params: Constants, meal_gram = [], meal_time = []):
        self.params = params
        self.timing = meal_time
        self.dg = meal_gram
        self.__meal_info__()
        self.__min2time__()

        self.basal_glucose = params.G
        self.G = self.basal_glucose
        self.X = params.X
        self.I = params.I
        self.simulation_time = params.MAX_TIME
        self.cur_time = 0
        self.MAX_OPTIMUM_GLUCOSE, self.MIN_OPTIMUM_GLUCOSE = 180, 80
        self.action_space = Box(low=np.array([0]), high=np.array([params.MAX_INSULIN]))
        self.observation_space = Box(low=np.array([0, 0, 0]), high=np.array([1000, 50, 1]))
        self.g_graph_list = []
        self.i_graph_list = []
        self.x_graph_list = []
        self.t_graph_list = []
        self.last_action = [0]
        self.data_points_t = []
        self.data_points = []
        self.overshoot_glucose_time = 0
        self.MAX_OVERSHOOT_CONS = params.MAX_OVERSHOOT_CONS

    def reset(self):
        self.cur_time = 0
        self.G = self.basal_glucose
        self.X = self.params.X
        self.I = self.params.I

        self.g_graph_list = []
        self.i_graph_list = []
        self.x_graph_list = []
        self.t_graph_list = []
        self.last_action = [0]
        self.data_points = []
        self.data_points_t = []
        self.overshoot_glucose_time = 0
        self.dg = self.dg
        self.timing = self.timing
        print(self.__min2time__())

        return (self.G, self.I, self.X)

    def step(self, action):
        overshoot = True
        if self.cur_time % self.params.INSULIN_PUMP_RATE != 0:  # get insulin reading every INSULIN_PUMP_RATE min
            action = self.last_action
        else:
            self.last_action = action
        self.G = self.solve_diff_eqn(action)
        rew = self.reward(self.G) - self.G * action[0]

        self.cur_time += 1
        if not (60 <= self.G <= 600):
            self.overshoot_glucose_time += 1

        if self.cur_time <= self.simulation_time and self.overshoot_glucose_time < self.MAX_OVERSHOOT_CONS:
            terminate = False
        else:
            terminate = True
        # Return observation, reward, done status, and info
        return np.array([self.G, self.I, self.X]), rew, terminate, {}

    def render(self, mode='human'):
        pass

    def reward(self, glucose):
        if 60 <= glucose <= 600:
            return (-(glucose - 130) ** 2) + 1  # Most suitable glucose value --> 130
        return -10e10

    def __meal_info__(self):
        self.timing.append(9999)
        self.dg.append(9999)

    def calc_glucose(self, y, t, action):
        G, X, I = self.G, self.X, self.I
        G = -1 * (self.params.p1 + X) * G + self.params.p1 * self.params.Gb + self.__meal_function__(t)
        X = -1 * (self.params.p2 * X) + (self.params.p3 * I)
        I = -1 * (self.params.n * I) + self.params.tau * action[0]
        return [G, I, X]

    def solve_diff_eqn(self, action):
        t_points = np.arange(self.cur_time - 1, self.cur_time + 1, self.params.h)
        t_points[t_points < 0] = 0
        y = [self.G, self.I, self.X]
        solution = odeint(self.calc_glucose, y, t_points,
                          args=(action,))
        self.G, self.I, self.X = solution.T[0][-1], solution.T[1][-1], solution.T[2][-1]
        self.g_graph_list.append(self.G)
        self.i_graph_list.append(action[0])
        self.x_graph_list.append(self.X)
        self.t_graph_list.append(self.cur_time)
        if (self.G not in self.data_points and self.cur_time % self.params.INSULIN_PUMP_RATE == 0):  # Ask Ma'am
            self.data_points_t.append(self.cur_time)
            self.data_points.append(self.G)
        # print(f'Time: {self.cur_time} | Glucose: {self.G} | Insulin: {self.I} | Effective:{self.X} | Action: {action}')
        return self.G

    def __meal_function__(self, t):
        m = 0
        for i in range(len(self.dg)):
            if i < len(self.dg) - 1 and t >= self.timing[i] and t < self.timing[i + 1]:
                t = t - self.timing[i]
                m = (100 * self.dg[i] * self.params.Ag * t * exp(-t / self.params.tmax_I)) / (
                        self.params.Vg * (pow(self.params.tmax_G, 2)))
        return m

    def __min2time__(self):
        out = ""
        for t in range(len(self.timing[:-1])):
            hour = self.timing[t] // 60
            minu = self.timing[t] - (60 * hour)
            if minu < 10:
                minu = "0" + str(minu)
            out += f"{self.timing[t]} -> {hour}:{minu} ({self.dg[t]}g Carbs)\n"
        return out
