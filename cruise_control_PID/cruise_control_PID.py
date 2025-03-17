import os
import numpy as np
import matplotlib.pyplot as plt
import control as ct

# === 1. Define the Cruise Control System ===
# Dynamics: m*v_dot = -b*v + u + d
m = 1000  # Mass of the car (kg)
b = 50    # Damping coefficient (N·s/m)
g = 9.81  # Gravity (m/s^2)

# State-space representation: v_dot = (-b/m) v + (1/m) u + (1/m) d
A = np.array([[-b/m]])
B = np.array([[1/m]])  # Control input (engine force)
C = np.array([[1]])    # Output is velocity
D = np.array([[0]])

# Disturbance (hill incline force = mg sin(theta))
disturbance = 100  # Simulating a hill (constant force)

# Create the open-loop system
sys_ol = ct.ss(A, B, C, D)

# === 2. Open-loop Step Response (Unstable to Disturbance) ===
T = np.linspace(0, 50, 500)  # Time vector
T, y_ol = ct.forced_response(sys_ol, T, np.zeros_like(T) + disturbance)

plt.figure()
plt.plot(T, y_ol, label="Open-loop Response (Unstable)")
plt.title("Open-loop Step Response: Cruise Control")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.grid()

if "CONTROL_PLOT_DIR" in os.environ:
    plt.savefig(os.path.join(os.environ["CONTROL_PLOT_DIR"], "open_loop_response.pdf"))
else:
    plt.show()

# === 3. Proportional Control (P-Only, No Perfect Tracking) ===
Kp = 200  # Proportional gain
controller_P = ct.tf([Kp], [1])  # P controller in transfer function form
sys_cl_P = ct.feedback(controller_P * sys_ol)  # Closed-loop system

T, y_cl_P = ct.step_response(sys_cl_P, T)

plt.figure()
plt.plot(T, y_cl_P, label="Proportional Control Response")
plt.title("Step Response with P Control")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.grid()

if "CONTROL_PLOT_DIR" in os.environ:
    plt.savefig(os.path.join(os.environ["CONTROL_PLOT_DIR"], "P_control_response.pdf"))
else:
    plt.show()

# === 4. Proportional-Integral Control (PI: Perfect Tracking & Disturbance Rejection) ===
Ki = 50  # Integral gain
controller_PI = ct.tf([Kp, Ki], [1, 0])  # PI controller
sys_cl_PI = ct.feedback(controller_PI * sys_ol)

T, y_cl_PI = ct.step_response(sys_cl_PI, T)

plt.figure()
plt.plot(T, y_cl_PI, label="PI Control Response (Perfect Tracking)")
plt.title("Step Response with PI Control")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.grid()

if "CONTROL_PLOT_DIR" in os.environ:
    plt.savefig(os.path.join(os.environ["CONTROL_PLOT_DIR"], "PI_control_response.pdf"))
else:
    plt.show()

# === 5. Compute Reference Tracking & Disturbance Rejection Gains ===
# Reference to output gain = steady-state response to step input
K_ss_ref = ct.dcgain(sys_cl_PI)
print(f"\nSteady-state gain for reference tracking (should be 1): {K_ss_ref}")

# Disturbance to output gain = steady-state response to step disturbance
dist_tf = ct.feedback(sys_ol, controller_PI)  # Closed-loop with disturbance
K_ss_dist = ct.dcgain(dist_tf)
print(f"Steady-state gain for disturbance rejection (should be 0): {K_ss_dist}")

# === 6. Proportional-Integral-Derivative Control (PID: Adds Damping) ===
Kd = 20  # Derivative gain
controller_PID = ct.tf([Kd, Kp, Ki], [1, 0])  # PID controller

sys_tf = ct.ss2tf(sys_ol)  # Convert state-space to transfer function
sys_cl_PID = ct.feedback(controller_PID * sys_tf)  # Now use transfer function representation

T, y_cl_PID = ct.step_response(sys_cl_PID, T)

plt.figure()
plt.plot(T, y_cl_PID, label="PID Control Response (Damping Added)")
plt.title("Step Response with PID Control")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.grid()

if "CONTROL_PLOT_DIR" in os.environ:
    plt.savefig(os.path.join(os.environ["CONTROL_PLOT_DIR"], "PID_control_response.pdf"))
else:
    plt.show()

# === 7. Compare All Controllers ===
plt.figure()
plt.plot(T, y_cl_P, "--", label="P Control")
plt.plot(T, y_cl_PI, "-.", label="PI Control (Perfect Tracking)")
plt.plot(T, y_cl_PID, "-", label="PID Control (Damping Added)")
plt.title("Comparison of P, PI, and PID Controllers")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.grid()

if "CONTROL_PLOT_DIR" in os.environ:
    plt.savefig(os.path.join(os.environ["CONTROL_PLOT_DIR"], "PID_comparison.pdf"))
else:
    plt.show()



