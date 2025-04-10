import os
import numpy as np
import matplotlib.pyplot as plt
import control as ct

# === Helper: Save or show plots based on CONTROL_PLOT_DIR ===
def save_or_show(fig, filename):
    if 'CONTROL_PLOT_DIR' in os.environ:
        fig.savefig(os.path.join(os.environ['CONTROL_PLOT_DIR'], filename), bbox_inches='tight')
    else:
        plt.show()

# === Define a few important example transfer functions ===

# 1. Stable 1st-order system
G1 = ct.tf([1], [1, 1])  # G1(s) = 1 / (s + 1)

# 2. Unstable open-loop system (RHP pole)
G2 = ct.tf([1], [1, -1])  # G2(s) = 1 / (s - 1)

# 3. Underdamped 2nd-order system
G3 = ct.tf([1], [1, 1, 1])  # G3(s) = 1 / (s^2 + s + 1)

# 4. High gain second-order system
G4 = ct.tf([10], [1, 2, 1])  # G4(s) = 10 / (s^2 + 2s + 1)

# === Pack into lists for easy iteration ===
systems = [G1, G2, G3, G4]
labels = [
    "Stable 1st-Order",
    "Unstable Open-Loop",
    "Underdamped 2nd-Order",
    "High-Gain System"
]

# === Frequency range for Bode and Nyquist ===
omega = np.logspace(-2, 2, 1000)

# === Loop over all systems ===
for G, label in zip(systems, labels):
    print(f"\n=== {label} ===")

    # --- Poles and Zeros ---
    poles = ct.poles(G)
    zeros = ct.zeros(G)
    print("Poles :", poles)
    print("Zeros:", zeros)

    # --- Gain & Phase Margins ---
    gm, pm, wgc, wpc = ct.margin(G)
    gm_db = 20 * np.log10(gm) if gm not in [np.inf, 0] else float('inf')
    print(f"Gain Margin (dB): {gm_db:.2f}")
    print(f"Phase Margin (deg): {pm:.2f}")
    print(f"Gain crossover freq (rad/s): {wgc:.2f}")
    print(f"Phase crossover freq (rad/s): {wpc:.2f}")

    # --- Bode Plot with Margin Annotations ---
    fig_bode, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    mag, phase, omega_out = ct.bode_plot(G, omega, dB=True, deg=True, plot=False)
    mag_db = 20 * np.log10(mag)

    ax_mag.semilogx(omega_out, mag_db, label='|G(jω)| [dB]')
    ax_phase.semilogx(omega_out, phase, label='∠G(jω) [deg]', color='orange')

    # Annotate Phase Margin
    if np.isfinite(wgc):
        ax_phase.axvline(wgc, color='red', linestyle='--', label=f'PM @ {wgc:.2f} rad/s')
        ax_phase.annotate(f'PM ≈ {pm:.1f}°', xy=(wgc, -180 + pm), xytext=(wgc, -180 + pm + 20),
                          arrowprops=dict(arrowstyle='->'), fontsize=10)

    # Annotate Gain Margin
    if np.isfinite(wpc) and gm not in [np.inf, 0]:
        ax_mag.axvline(wpc, color='green', linestyle='--', label=f'GM @ {wpc:.2f} rad/s')
        ax_mag.annotate(f'GM ≈ {gm_db:.1f} dB', xy=(wpc, 0), xytext=(wpc, gm_db + 10),
                        arrowprops=dict(arrowstyle='->'), fontsize=10)

    ax_mag.set_title(f"Bode Plot with Margins: {label}")
    ax_mag.set_ylabel("Magnitude (dB)")
    ax_phase.set_ylabel("Phase (deg)")
    ax_phase.set_xlabel("Frequency (rad/s)")
    ax_mag.grid(True)
    ax_phase.grid(True)
    ax_mag.legend()
    ax_phase.legend()
    save_or_show(fig_bode, label.lower().replace(" ", "_") + "_bode_margins.pdf")

    # --- Nyquist Plot ---
    fig_nyq = plt.figure(figsize=(6, 6))
    ct.nyquist_plot(G, omega, color='b', label='Nyquist Curve')

    # Critical Point
    plt.plot(-1, 0, 'rx', markersize=10, label='Critical Point (-1)')
    plt.axhline(0, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(0, color='k', linestyle='--', linewidth=0.5)

    # Optional: unit circle
    theta = np.linspace(0, 2 * np.pi, 300)
    plt.plot(np.cos(theta), np.sin(theta), linestyle=':', color='gray', label='Unit Circle')

    plt.title(f"Nyquist Plot: {label}")
    plt.xlabel("Re[G(jω)]")
    plt.ylabel("Im[G(jω)]")
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    save_or_show(fig_nyq, label.lower().replace(" ", "_") + "_nyquist_annotated.pdf")

    # --- Pole-Zero Map ---
    fig_pz = plt.figure()
    ct.pzmap(G, plot=True, grid=True)
    plt.title(f"Pole-Zero Map: {label}")
    save_or_show(fig_pz, label.lower().replace(" ", "_") + "_pzmap.pdf")

# === Summary for Teaching ===
print("\n=== Nyquist Stability Criterion Recap ===")
print("If open-loop system has P unstable poles, and Nyquist plot encircles -1 N times CW,")
print("Then closed-loop system has Z = N + P unstable poles.")
print("For stability, we want Z = 0 ⇒ N = -P.")


