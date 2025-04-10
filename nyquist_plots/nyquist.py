import os
import numpy as np
import matplotlib.pyplot as plt
import control as ct

# === Helper to save or show plots ===
def save_or_show(fig, name):
    if 'CONTROL_PLOT_DIR' in os.environ:
        fig.savefig(os.path.join(os.environ['CONTROL_PLOT_DIR'], name))
    else:
        plt.show()

# === Define key transfer functions ===

# 1. Stable first-order system
G1 = ct.tf([1], [1, 1])  # G1(s) = 1 / (s + 1)

# 2. Unstable open-loop (RHP pole), but feedback-stabilized
G2 = ct.tf([1], [1, -1])  # G2(s) = 1 / (s - 1)

# 3. Under-damped second-order system
G3 = ct.tf([1], [1, 1, 1])  # G3(s) = 1 / (s^2 + s + 1)

# 4. High-gain system with risk of instability
G4 = ct.tf([10], [1, 2, 1])  # G4(s) = 10 / (s^2 + 2s + 1)

systems = [G1, G2, G3, G4]
labels = [
    "Stable 1st-Order",
    "Unstable OL, RHP Pole",
    "Underdamped 2nd-Order",
    "High Gain Risk"
]

# === Analysis Loop ===
omega = np.logspace(-2, 2, 1000)

for G, label in zip(systems, labels):
    print(f"\n=== {label} ===")

    # === 1. Poles and Zeros ===
    poles = ct.poles(G)
    zeros = ct.zeros(G)
    print("Poles :", poles)
    print("Zeros:", zeros)

    # === 2. Gain/Phase Margins ===
    gm, pm, wgc, wpc = ct.margin(G)
    print(f"Gain Margin (dB): {20*np.log10(gm) if gm != np.inf else '∞'}")
    print(f"Phase Margin (deg): {pm:.2f}")
    print(f"Gain crossover freq (rad/s): {wgc:.2f}")
    print(f"Phase crossover freq (rad/s): {wpc:.2f}")

    # === 3. Bode Plot ===
    fig_bode = plt.figure()
    mag, phase, omega_out = ct.bode_plot(G, omega, dB=True, deg=True, Hz=False, plot=True)
    plt.suptitle(f"Bode Plot: {label}")
    save_or_show(fig_bode, label.lower().replace(" ", "_") + "_bode.pdf")

    # === 4. Nyquist Plot ===
    fig_nyq = plt.figure()
    ct.nyquist_plot(G, omega, color='b')
    plt.plot(-1, 0, 'rx', markersize=10, label='Critical Point (-1)')
    plt.axhline(0, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(0, color='k', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.title(f"Nyquist Plot: {label}")
    plt.grid(True)
    save_or_show(fig_nyq, label.lower().replace(" ", "_") + "_nyquist.pdf")

    # === 5. Pole-Zero Map ===
    fig_pz = plt.figure()
    ct.pzmap(G, plot=True, grid=True)
    plt.title(f"Pole-Zero Map: {label}")
    save_or_show(fig_pz, label.lower().replace(" ", "_") + "_pzmap.pdf")

# === Nyquist Stability Recap ===
print("\n=== Nyquist Stability Criterion Recap ===")
print("If OL system has P unstable poles, and encircles -1 N times CW,")
print("Then CL system has Z = N + P unstable poles.")
print("We want Z = 0 for stability ⇒ N = -P.")



