import numpy as np
import matplotlib.pyplot as plt
import control as ct
import os

# --- Utility functions ---
def poly_to_latex(coeffs):
    terms = []
    order = len(coeffs) - 1
    for i, c in enumerate(coeffs):
        power = order - i
        if c == 0:
            continue
        if power == 0:
            term = f"{c}"
        elif power == 1:
            term = f"{c}s"
        else:
            term = f"{c}s^{power}"
        terms.append(term)
    return " + ".join(terms)

def tf_to_latex(tf):
    num_str = poly_to_latex(tf.num[0][0])
    den_str = poly_to_latex(tf.den[0][0])
    return rf"$G(s) = \dfrac{{{num_str}}}{{{den_str}}}$"

def tf_to_filename(tf, label=""):
    num_str = "_".join(str(c) for c in tf.num[0][0])
    den_str = "_".join(str(c) for c in tf.den[0][0])
    base = f"bode_{label}_num_{num_str}_den_{den_str}.pdf"
    return base

# --- Define lead and lag compensators ---
K = 5

# Lead: a < b ⇒ phase lead
a_lead = 2
b_lead = 10
lead_tf = ct.tf([K, K * a_lead], [1, b_lead])

# Lag: a > b ⇒ phase lag
a_lag = 10
b_lag = 2
lag_tf = ct.tf([K, K * a_lag], [1, b_lag])

# --- Plot Lead ---
plt.figure()
ct.bode_plot(lead_tf, omega_limits=(1e-2, 1e2), dB=True, deg=True, Hz=False)
plt.suptitle("Lead Compensator: " + tf_to_latex(lead_tf), fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.95])

filename_lead = tf_to_filename(lead_tf, "lead")
if 'CONTROL_PLOT_DIR' in os.environ:
    path = os.path.join(os.environ['CONTROL_PLOT_DIR'], filename_lead)
    plt.savefig(path)
    print(f"Lead plot saved to: {path}")
else:
    plt.show()

# --- Print Lead Margins ---
gm, pm, wgc, wpc = ct.margin(lead_tf)
gm_db = 20 * np.log10(gm) if gm not in [0, np.inf] else float('inf')
print("\n--- Lead Compensator ---")
print(f"Gain Margin: {gm:.2f} ({gm_db:.2f} dB)")
print(f"Phase Margin: {pm:.2f}°")
print(f"Gain Crossover Frequency: {wgc:.2f} rad/s")
print(f"Phase Crossover Frequency: {wpc:.2f} rad/s")

# --- Plot Lag ---
plt.figure()
ct.bode_plot(lag_tf, omega_limits=(1e-2, 1e2), dB=True, deg=True, Hz=False)
plt.suptitle("Lag Compensator: " + tf_to_latex(lag_tf), fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.95])

filename_lag = tf_to_filename(lag_tf, "lag")
if 'CONTROL_PLOT_DIR' in os.environ:
    path = os.path.join(os.environ['CONTROL_PLOT_DIR'], filename_lag)
    plt.savefig(path)
    print(f"Lag plot saved to: {path}")
else:
    plt.show()

# --- Print Lag Margins ---
gm, pm, wgc, wpc = ct.margin(lag_tf)
gm_db = 20 * np.log10(gm) if gm not in [0, np.inf] else float('inf')
print("\n--- Lag Compensator ---")
print(f"Gain Margin: {gm:.2f} ({gm_db:.2f} dB)")
print(f"Phase Margin: {pm:.2f}°")
print(f"Gain Crossover Frequency: {wgc:.2f} rad/s")
print(f"Phase Crossover Frequency: {wpc:.2f} rad/s")


