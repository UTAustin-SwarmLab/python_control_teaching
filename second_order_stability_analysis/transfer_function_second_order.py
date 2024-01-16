import os
import matplotlib.pyplot as plt   # MATLAB plotting functions
from control.matlab import *  # MATLAB-like functions
import control as ct
import numpy as np


# Parameters defining the system (list)
damping_list = [0.2, 0.4, 1., 1.2, 1.2]       # damping ratio
natfreq_list = [1., 1., 1., 1., 1., 1., 1., 1.]                   # nat frequency

# create two plots, one for step response and other from initial condition
step_response_plot = plt.figure()
initial_condition_plot = plt.figure()

# loop through different configurations

time_horizon = 100
# initial condition
X0 = [1, 0]

for zeta, w0 in zip(damping_list, natfreq_list):
    # print the parameters
    legend_str = 'zeta: ' + str(zeta) + ', w0: ' + str(w0)
    print(legend_str)

    # System matrices
    A = [[0, 1.], [-w0**2, -2*zeta*w0]]
    B = [[0], [1]]
    C = [[1., 0]]

    # define the dynamical system
    sys = ss(A, B, C, 0)

    # Step response for the system
    plt.figure(step_response_plot.number)
    yout, T = step(sys)
    plt.plot(T.T, yout.T, label=legend_str)

    # initial condition response
    T,yout = ct.initial_response(sys, T=time_horizon, X0=X0)
    plt.figure(initial_condition_plot.number)
    plt.plot(T.T, yout.T, label=legend_str)

    # compute the eigenvalues
    eigenvals, eigenvecs = np.linalg.eig(np.array(A))
    print('eig: ', eigenvals)
    print('')

    # analytical eigenvalues
    analytical_eig1 = -zeta*w0 + w0*np.emath.sqrt(zeta**2-1)
    analytical_eig2 = -zeta*w0 - w0*np.emath.sqrt(zeta**2-1)
    print('analytical eig: ', analytical_eig1, analytical_eig2)
    print('')

# plot the step response and save to a directory or directly show
plt.figure(step_response_plot.number)
plt.legend()

if 'CONTROL_PLOT_DIR' not in os.environ:
    plt.show()
else:
    plt.savefig(os.environ['CONTROL_PLOT_DIR'] + '/tf_step.pdf')


# plot the initial condition response and save to a directory or directly show
plt.figure(initial_condition_plot.number)
plt.legend()

if 'CONTROL_PLOT_DIR' not in os.environ:
    plt.show()
else:
    plt.savefig(os.environ['CONTROL_PLOT_DIR'] + '/tf_init.pdf')

