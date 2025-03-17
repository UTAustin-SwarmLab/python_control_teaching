import os
import numpy as np
import matplotlib.pyplot as plt
import control as ct
from control.matlab import *

# Define an open-loop unstable second-order system
A = np.array([[0, 1], [2, 1]])  # Unstable: has eigenvalues in the right half-plane
B = np.array([[0], [1]])        # Input matrix
C = np.array([[1, 0]])          # Output matrix
D = np.array([[0]])             # No direct feedthrough

# Create the state-space system
sys_ol = ct.ss(A, B, C, D)

# Compute open-loop eigenvalues (should include at least one positive real part)
eigenvalues_ol, _ = np.linalg.eig(A)
print("Open-loop eigenvalues (should show instability):", eigenvalues_ol)

# Plot open-loop step response (short horizon to see divergence)
T_short = np.linspace(0, 2, 100)
T, y_ol = ct.step_response(sys_ol, T_short)

plt.figure()
plt.plot(T, y_ol, label="Open-loop Step Response")
plt.title("Open-loop Step Response (Unstable System)")
plt.xlabel("Time (s)")
plt.ylabel("Output")
plt.legend()
plt.grid()

# Save or show plot
if 'CONTROL_PLOT_DIR' in os.environ:
    plt.savefig(os.path.join(os.environ['CONTROL_PLOT_DIR'], 'open_loop_step.pdf'))
else:
    plt.show()

# State feedback control: Place poles for two stable cases
desired_poles_fast = np.array([-2, -3])  # Fast response
desired_poles_slow = np.array([-0.5, -0.8])  # Slow response

# Compute state feedback gains using pole placement
K_fast = ct.place(A, B, desired_poles_fast)
K_slow = ct.place(A, B, desired_poles_slow)

# Closed-loop system dynamics
A_cl_fast = A - B @ K_fast
A_cl_slow = A - B @ K_slow

# Compute closed-loop eigenvalues
eigenvalues_cl_fast = np.linalg.eigvals(A_cl_fast)
eigenvalues_cl_slow = np.linalg.eigvals(A_cl_slow)

print("\nState feedback gain K (fast response):", K_fast)
print("Closed-loop eigenvalues (fast response):", eigenvalues_cl_fast)

print("\nState feedback gain K (slow response):", K_slow)
print("Closed-loop eigenvalues (slow response):", eigenvalues_cl_slow)

# Create closed-loop systems
sys_cl_fast = ct.ss(A_cl_fast, B, C, D)
sys_cl_slow = ct.ss(A_cl_slow, B, C, D)

# Plot step response for both cases
T_long = np.linspace(0, 10, 100)  # Longer horizon for stable cases
T, y_cl_fast = ct.step_response(sys_cl_fast, T_long)
T, y_cl_slow = ct.step_response(sys_cl_slow, T_long)

plt.figure()
plt.plot(T, y_cl_fast, label="Fast Closed-loop Step Response")
plt.plot(T, y_cl_slow, label="Slow Closed-loop Step Response")
plt.title("Closed-loop Step Responses (Fast vs. Slow)")
plt.xlabel("Time (s)")
plt.ylabel("Output")
plt.legend()
plt.grid()

if 'CONTROL_PLOT_DIR' in os.environ:
    plt.savefig(os.path.join(os.environ['CONTROL_PLOT_DIR'], 'closed_loop_step.pdf'))
else:
    plt.show()

# Compute steady-state gain using final value theorem
def steady_state_gain(A, B, C, D):
    """
    Computes the steady-state gain K_ss using the final value theorem:
    K_ss = C * (-A)^(-1) * B + D
    """
    K_ss = -C @ np.linalg.inv(A) @ B + D
    return K_ss.item()  # Convert 1x1 array to scalar

# Compute steady-state gains for fast and slow closed-loop systems
K_ss_fast = steady_state_gain(A_cl_fast, B, C, D)
K_ss_slow = steady_state_gain(A_cl_slow, B, C, D)

print("\nSteady-state gain for fast response system:", K_ss_fast)
print("Steady-state gain for slow response system:", K_ss_slow)



# Plot sinusoidal response (forced response to sin input)
T_sin = np.linspace(0, 10, 100)
U_sin = np.sin(T_sin)  # Sinusoidal input
T, y_sin_fast = ct.forced_response(sys_cl_fast, T_sin, U_sin)
T, y_sin_slow = ct.forced_response(sys_cl_slow, T_sin, U_sin)

plt.figure()
plt.plot(T, y_sin_fast, label="Fast Closed-loop Sinusoidal Response")
plt.plot(T, y_sin_slow, label="Slow Closed-loop Sinusoidal Response")
plt.title("Closed-loop Sinusoidal Response")
plt.xlabel("Time (s)")
plt.ylabel("Output")
plt.legend()
plt.grid()

if 'CONTROL_PLOT_DIR' in os.environ:
    plt.savefig(os.path.join(os.environ['CONTROL_PLOT_DIR'], 'closed_loop_sin.pdf'))
else:
    plt.show()

# Compute closed-loop transfer function for Bode plot
sys_tf_fast = ct.ss2tf(sys_cl_fast)
sys_tf_slow = ct.ss2tf(sys_cl_slow)



# Plot Bode plot for fast and slow closed-loop systems
plt.figure()
ct.bode_plot(sys_tf_fast, dB=True, label="Fast Response")
ct.bode_plot(sys_tf_slow, dB=True, label="Slow Response")
plt.title("Bode Plot of Closed-loop System")

if 'CONTROL_PLOT_DIR' in os.environ:
    plt.savefig(os.path.join(os.environ['CONTROL_PLOT_DIR'], 'bode_plot.pdf'))
else:
    plt.show()



