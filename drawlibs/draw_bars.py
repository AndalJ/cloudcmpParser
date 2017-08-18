import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

patterns = ['-', '+', 'x', '\\', '*', 'o', 'O', '.', '/']

def draw_bars(ax, jsondata, sorted_by, img_name):
    df = pd.DataFrame(jsondata)
    sorted_df = df.sort_values(by=sorted_by, ascending=False)

    cols = list(sorted_df)
    x = cols[0]
    y = cols[1:]
    num_y = len(y)
    sorted_df.plot(x=x, y=y, kind='bar')

    bars = ax.patches
    hatches = ''.join(h*len(df) for h in patterns[:len(df)])

    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    ax.legend(loc='center right', bbox_to_anchor=(1, 1), ncol=4)

    plt.savefig(img_name + ".jpg")
    plt.savefig(img_name + ".pdf")
    plt.savefig(img_name + ".png")
    plt.show()