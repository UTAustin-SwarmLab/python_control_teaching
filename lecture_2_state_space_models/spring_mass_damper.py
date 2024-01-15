import os
import matplotlib.pyplot as plt   # MATLAB plotting functions
from control.matlab import *  # MATLAB-like functions
import control as ct


# Parameters defining the system (list)
m_list = [250.0, 250]           	# system mass
k_list = [20, 40, 40.0]            	# spring constant
b_list = [60.0, 40.0, 80.0]         # damping constant

# loop through different configurations

step_response_plot = plt.figure()
initial_condition_plot = plt.figure()

for m, k, b in zip(m_list, k_list, b_list):

    # print the parameters
	print('mass: ', m, 'spring_const: ', k, 'damping: ', b)

	# System matrices
	A = [[0, 1.], [-k/m, -b/m]]
	B = [[0], [1/m]]
	C = [[1., 0]]
	sys = ss(A, B, C, 0)

	# Step response for the system
	plt.figure(step_response_plot.number)
	yout, T = step(sys)
	plt.plot(T.T, yout.T)

	# initial condition response
	time_horizon = 100
	X0 = [5, 0]
	T,yout = ct.initial_response(sys, T=time_horizon, X0=X0)
	plt.figure(initial_condition_plot.number)
	plt.plot(T.T, yout.T)

plt.figure(step_response_plot.number)
plt.savefig('step.pdf')


plt.figure(initial_condition_plot.number)
plt.savefig('init.pdf')
