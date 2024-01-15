import os
import matplotlib.pyplot as plt   # MATLAB plotting functions
from control.matlab import *  # MATLAB-like functions
import control as ct


# Do the scalar case
a_list = [-2, -1, -0.5, 0, 0.1]

# loop through different configurations
step_response_plot = plt.figure()
initial_condition_plot = plt.figure()

time_horizon = 5
X0 = [1]

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

plt.figure(step_response_plot.number)
plt.legend()
plt.savefig('step.pdf')


plt.figure(initial_condition_plot.number)
plt.legend()
plt.savefig('init.pdf')
