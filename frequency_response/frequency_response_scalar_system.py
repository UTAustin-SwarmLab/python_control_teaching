"""
This code simulates a simple 1D LTI system. It shows the exponential response for unstable and stable systems and contrasts them.

"""

import os
import matplotlib.pyplot as plt   # MATLAB plotting functions
from control.matlab import *  # MATLAB-like functions
import control as ct



# time horizon to simulate
time_horizon = 3
# initial condition
X0 = [1]

a_list = [-2, -0.5]
b_list = [1, 3]
c_list = [1, 2]
d_list = [0, 1.5]

plot_index = 0

# initialize two plots
step_response_plot = plt.figure()
initial_condition_plot = plt.figure()
impulse_response_plot = plt.figure()


for a, b, c, d, in zip(a_list, b_list, c_list, d_list):


	# System matrices
    A = [a]
    B = [b]
    C = [c]
    D = [d]
    sys = ss(A, B, C, D)

    # calculate the expected gain = -b/a
    gain = d-c*b/a
    legend_str = 'A: ' + str(a) + ', B: ' + str(b) + ', C: ' + str(c) + ', D: ' + str(d) + ', gain: ' + str(gain)
    print(legend_str)

    # Step response for the system
    plt.figure(step_response_plot.number)
    yout, T = step(sys)

    plt.plot(T.T, yout.T, label=legend_str)

    # initial condition response
    T,yout = ct.initial_response(sys, T=time_horizon, X0=X0)
    plt.figure(initial_condition_plot.number)
    plt.plot(T.T, yout.T, label=legend_str)


    # impulse response

	# modified system for impulse response with no direct term
    modified_sys = ss(A, B, C, [0])

    T,yout = ct.impulse_response(modified_sys, T=time_horizon)
    plt.figure(impulse_response_plot.number)
    plt.plot(T.T, yout.T, label=legend_str)

    # response to a sinusoid of a specific frequency

    # calculate phase offset, magnitude etc. analytically

    # compute the bode plot



    # plot in two separate plots
    plt.figure(step_response_plot.number)
    plt.legend()
    if 'CONTROL_PLOT_DIR' not in os.environ:
        plt.show()
    else:
        plt.savefig(os.environ['CONTROL_PLOT_DIR'] + '/Lec6_scalar_step_' + str(plot_index) + '.pdf')

    plt.figure(initial_condition_plot.number)
    plt.legend()

    if 'CONTROL_PLOT_DIR' not in os.environ:
        plt.show()
    else:
        plt.savefig(os.environ['CONTROL_PLOT_DIR'] + '/Lec6_scalar_init_' + str(plot_index) + '.pdf')

    plt.figure(impulse_response_plot.number)
    plt.legend()
    if 'CONTROL_PLOT_DIR' not in os.environ:
        plt.show()
    else:
        plt.savefig(os.environ['CONTROL_PLOT_DIR'] + '/Lec6_scalar_impulse_' + str(plot_index) + '.pdf')

    # increment the plot index
    plot_index += 1

