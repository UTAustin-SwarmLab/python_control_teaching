import os
import numpy as np
import matplotlib.pyplot as plt
import control as ct

# === Define a few example transfer functions ===

# First-order stable system: G(s) = 1 / (s + 1)
G1 = ct.tf([1], [1, 1])

# First-order unstable system: G(s) = 1 / (s - 1)
G2 = ct.tf([1], [1, -1])

# Second-order underdamped system: G(s) = 1 / (s^2 + 2ζωs + ω^2)
zeta = 0.3
omega = 2
G3 = ct.tf([1], [1, 2*zeta*omega, omega**2])

# Second-order critically damped system
zeta_cd = 1.0
G4 = ct.tf([1], [1, 2*zeta_cd*omega, omega**2])

# Second-order overdamped system
zeta_od = 2.0
G5 = ct.tf([1], [1, 2*zeta_od*omega, omega**2])

# === List of systems and labels for looping ===
systems = [G1, G2, G3, G4, G5]
labels = [
    "Stable First-Order",
    "Unstable First-Order",
    "Underdamped Second-Order",
    "Critically Damped",
    "Overdamped"
]

# === Step Responses ===
plt.figure()
for G, label in zip(systems, labels):

	T = np.linspace(0, 2.25, 500)  # Define time vector from 0 to 3 seconds
	T, y = ct.step_response(G, T)
	plt.plot(T, y, label=label)


plt.title("Step Responses for Different Transfer Functions")
plt.xlabel("Time (s)")
plt.ylabel("Output")
plt.grid()
plt.legend()

if "CONTROL_PLOT_DIR" in os.environ:
    plt.savefig(os.path.join(os.environ["CONTROL_PLOT_DIR"], "tf_step_responses.pdf"))
else:
    plt.show()

# === Pole-Zero Maps and Bode Plots ===
for G, label in zip(systems, labels):
    poles = ct.poles(G)
    zeros = ct.zeros(G)

    print(f"\nTransfer Function: {label}")
    print("  Poles :", poles)
    print("  Zeros:", zeros)

    # Pole-Zero Map
    plt.figure()
    ct.pzmap(G, grid=True, plot=True)
    plt.title(f"Pole-Zero Map: {label}")

    if "CONTROL_PLOT_DIR" in os.environ:
        filename = label.lower().replace(" ", "_").replace("-", "") + "_pzmap.pdf"
        plt.savefig(os.path.join(os.environ["CONTROL_PLOT_DIR"], filename))
    else:
        plt.show()

    # Bode Plot
    plt.figure()
    mag, phase, omega = ct.bode_plot(G, dB=True, Hz=False, deg=True, omega_limits=(0.1, 100), plot=True)
    plt.suptitle(f"Bode Plot: {label}")

    if "CONTROL_PLOT_DIR" in os.environ:
        filename = label.lower().replace(" ", "_").replace("-", "") + "_bode.pdf"
        plt.savefig(os.path.join(os.environ["CONTROL_PLOT_DIR"], filename))
    else:
        plt.show()


