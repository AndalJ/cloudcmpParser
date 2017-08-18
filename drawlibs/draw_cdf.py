import numpy as np
import matplotlib.pyplot as plt

styles = ['k-', 'b.-', 'r--', 'm:', 'ys-', 'go-', 'c^-',
          'k.-', 'b--', 'r:', 'ms-','yo-', 'g^-', 'c-',
          'k--', 'b:', 'rs-', 'mo-', 'y^-', 'g-', 'c.-',
          'k:', 'bs-', 'ro-', 'm^-', 'y-', 'g.-', 'c--',
          'ks-', 'bo-', 'r^-', 'm-', 'y.-', 'g--', 'c-',
          'ko-', 'b^-', 'r-', 'm.-', 'y--', 'g-', 'cs-']

def draw_cdf(data, ls, lg):
    sorted_data = np.sort(data)
    yvals = np.arange(len(sorted_data))/float(len(sorted_data))
    plt.plot(sorted_data, yvals, ls, label=lg, linewidth=2.0)