import numpy as np
import matplotlib.pyplot as plt
import control as ct


# --- Define transfer function ---
tf = ct.tf([25, 25], [1, 4, 20, 32, 0])

ct.bode_plot(tf)
plt.show()

# --- Margins ---
gm, pm, wgc, wpc = ct.margin(tf)
gm_db = 20 * np.log10(gm) if gm not in [0, np.inf] else float('inf')

# --- Print margins ---
print(f"Gain Margin: {gm:.2f} ({gm_db:.2f} dB)")
print(f"Phase Margin: {pm:.2f}°")
print(f"Gain Crossover Frequency: {wgc:.2f} rad/s")
print(f"Phase Crossover Frequency: {wpc:.2f} rad/s")








