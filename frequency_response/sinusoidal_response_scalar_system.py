"""
This code simulates a simple 1D LTI system. It applies a sinusoidal input, calculates the amplitude and phase of the response, and plots the bode plot.

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



# initial condition
x_0 = 3

bode_plot = plt.figure()

# System matrices
A = [-1]
B = [1]
C = [1]
D = [0]
sys = ss(A, B, C, D)

# time horizon to simulate
T = 20
# how finely to discretize
num_discretization_points = 500

omega_list = [3, 5]

for omega in omega_list:

    # initialize two plots
    sinusoidal_response_plot = plt.figure()
    t = np.linspace(0,T,num_discretization_points)
    u = np.sin(omega*t)
    yout,time_vec,xout = lsim(sys,u,t,x_0)

    # plot sinusoidal response for the system
    plt.figure(sinusoidal_response_plot.number)
    plt.plot(t, yout, 'r', label='y_t')
    plt.plot(t, xout, 'b', label='x_t')
    plt.plot(t, u, 'k', label='u_t')
    plt.xlabel('Time t')
    plt.ylabel('Control, Output, and State')
    plt.title('Frequency omega: ' + str(omega))
    plt.legend()

    # sinusoidal response plot
    plot_name = 'Lec6_scalar_sinusoidal_frequency' + str(omega)
    save_plot(sinusoidal_response_plot.number, plot_name)

# calculate phase offset, magnitude etc. analytically
plt.figure(bode_plot.number)
out = bode(sys,dB=False,deg=True)
plot_name = 'matlab_bode'
save_plot(bode_plot.number, plot_name)
