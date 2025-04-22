import numpy as np
import matplotlib.pyplot as plt
import control as ct
import os

# --- Define transfer function here ---
#num = [25, 25]
#den = [1, 4, 20, 32, 0]

# a few more examples

num = [3.8, 4]
den = [1, -1, 0]

tf = ct.tf(num, den)

# --- Generate LaTeX string for the title manually ---
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

# --- Generate safe filename from TF ---
def tf_to_filename(tf):
    num_str = "_".join(str(c) for c in tf.num[0][0])
    den_str = "_".join(str(c) for c in tf.den[0][0])
    return f"bode_plot_num_{num_str}_den_{den_str}.pdf"

# --- Create Bode plot ---
ct.bode_plot(tf, omega_limits=(1e-2, 1e2), dB=True, deg=True, Hz=False)
plt.suptitle("Bode Plot of " + tf_to_latex(tf), fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.95])

# --- Save or show figure ---
filename = tf_to_filename(tf)
if 'CONTROL_PLOT_DIR' in os.environ:
    filepath = os.path.join(os.environ['CONTROL_PLOT_DIR'], filename)
    plt.savefig(filepath)
    print(f"Figure saved to: {filepath}")
else:
    plt.show()

# --- Compute and print margins ---
gm, pm, wgc, wpc = ct.margin(tf)
gm_db = 20 * np.log10(gm) if gm not in [0, np.inf] else float('inf')

print(f"Gain Margin: {gm:.2f} ({gm_db:.2f} dB)")
print(f"Phase Margin: {pm:.2f}°")
print(f"Gain Crossover Frequency: {wgc:.2f} rad/s")
print(f"Phase Crossover Frequency: {wpc:.2f} rad/s")



