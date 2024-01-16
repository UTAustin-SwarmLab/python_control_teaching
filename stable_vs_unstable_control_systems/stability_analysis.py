"""
This code simulates a simple 1D LTI system. It shows the exponential response for unstable and stable systems and contrasts them.

"""

import os
import matplotlib.pyplot as plt   # MATLAB plotting functions
from control.matlab import *  # MATLAB-like functions
import control as ct


# Do the scalar case, exp(-a*t)
a_list = [-2, -1, -0.5, 0, 0.1]

# initialize two plots
step_response_plot = plt.figure()
initial_condition_plot = plt.figure()

# time horizon to simulate
time_horizon = 5
# initial condition
X0 = [1]

# loop through different stable and unstable configurations
for a in zip(a_list):
    # print the parameters
    legend_str = 'exp(' + str(a) + 't)'
    print(legend_str)

    # System matrices
    A = [a]
    B = [1]
    C = [1]
    sys = ss(A, B, C, 0)

    # Step response for the system
    plt.figure(step_response_plot.number)
    yout, T = step(sys)
    plt.plot(T.T, yout.T, label=legend_str)

    # initial condition response
    T,yout = ct.initial_response(sys, T=time_horizon, X0=X0)
    plt.figure(initial_condition_plot.number)
    plt.plot(T.T, yout.T, label=legend_str)

# plot in two separate plots
plt.figure(step_response_plot.number)
plt.legend()
if 'CONTROL_PLOT_DIR' not in os.environ:
    plt.show()
else:
    plt.savefig(os.environ['CONTROL_PLOT_DIR'] + '/Lec3_scalar_stability_step.pdf')

plt.figure(initial_condition_plot.number)
plt.legend()

if 'CONTROL_PLOT_DIR' not in os.environ:
    plt.show()
else:
    plt.savefig(os.environ['CONTROL_PLOT_DIR'] + '/Lec3_scalar_stability_init.pdf')

