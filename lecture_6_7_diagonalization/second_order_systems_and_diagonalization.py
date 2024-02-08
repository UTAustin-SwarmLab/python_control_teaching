"""
This code simulates a simple 1D LTI system. It shows the exponential response for unstable and stable systems and contrasts them.

"""

import os
import matplotlib.pyplot as plt   # MATLAB plotting functions
from control.matlab import *  # MATLAB-like functions
import control as ct
import numpy as np


def save_plot(figure_number, plot_name):
    # plot in two separate plots
    plt.figure(figure_number)
    plt.legend()
    if 'CONTROL_PLOT_DIR' not in os.environ:
        plt.show()
    else:
        plt.savefig(os.environ['CONTROL_PLOT_DIR'] + '/' + plot_name + '.pdf')
    plt.close()



# time horizon to simulate
time_horizon = 10
# initial condition
X0 = [1, 1]

alpha_list = [0, 0, -1, -1, -2, -2]
beta_list = [1, 2, 1, 2, 1, 2]

plot_index = 0


for alpha, beta in zip(alpha_list, beta_list):
    legend_str = ' '.join(['alpha: ', str(alpha), 'beta: ', str(beta)])
    print(legend_str)
    # System matrices
    A = [[alpha, beta], [-beta, alpha]]
    B = [[0],[0]]
    C = np.eye(2)
    D = np.zeros([2,1])
    sys = ss(A, B, C, D)

    # initialize two plots
    initial_condition_plot = plt.figure()

    # initial condition response
    T,yout = ct.initial_response(sys, T=time_horizon, X0=X0)
    plt.figure(initial_condition_plot.number)
    plt.plot(T.T, yout.T, label=legend_str)


    # init response plot
    plot_name = 'Lec7_matrix_exponential_' + str(plot_index)
    save_plot(initial_condition_plot.number, plot_name)


    # increment the plot index
    plot_index += 1
