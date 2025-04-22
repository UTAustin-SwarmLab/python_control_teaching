import numpy as np
import matplotlib.pyplot as plt
import control as ct

# --- Define transfer function ---
tf = ct.tf([25, 25], [1, 4, 20, 32, 0])

# --- Margins ---
gm, pm, wgc, wpc = ct.margin(tf)
gm_db = 20 * np.log10(gm) if gm not in [0, np.inf] else float('inf')

# --- Frequency range ---
omega = np.logspace(-2, 2, 1000)  # 0.01 to 100 rad/s

# --- Frequency response ---
_, H, _ = ct.frequency_response(tf, omega)  # modern, correct
mag_db = 20 * np.log10(np.abs(H).squeeze())
phase_deg = np.angle(H.squeeze(), deg=True)

# --- Plot ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

ax1.semilogx(omega, mag_db)
ax1.set_ylabel("Magnitude (dB)")
ax1.grid(True)

ax2.semilogx(omega, phase_deg, color='orange')
ax2.set_ylabel("Phase (deg)")
ax2.set_xlabel("Frequency (rad/s)")
ax2.grid(True)

plt.suptitle("Bode Plot with Margins")
plt.tight_layout()
plt.show()

# --- Print margins ---
print(f"Gain Margin: {gm:.2f} ({gm_db:.2f} dB)")
print(f"Phase Margin: {pm:.2f}°")
print(f"Gain Crossover Frequency: {wgc:.2f} rad/s")
print(f"Phase Crossover Frequency: {wpc:.2f} rad/s")








