import matplotlib.pyplot as plt
import numpy as np

from harambot.lib import analyze
from harambot.lib.utils import NameGetter


def plot_cumsum(data_path, name_path):
    """
    Compute and vizualize the cumsum plot
    Args:
        data_path (str): path to the data.json
        name_path (str): path to the names mapping
    """
    names = NameGetter(name_path)
    dt = analyze.read(data_path)
    cumsum_data, date_range = analyze.get_cumsum(dt)

    # Create the x_ticks
    years = np.array(['{} {}'.format(k.month, k.year) for k in date_range])
    _, idx = np.unique(years, return_index=True)
    years = years[np.sort(idx)]
    x = [i * (len(years) / len(date_range)) for i in range(len(date_range))]
    plt.subplot(223)

    # Plot the cumsum foreach user
    for senderId, cumsum in sorted(cumsum_data.items(), key=lambda it: it[1][-1]):
        plt.plot(x, cumsum, label=names[senderId])
    plt.legend(bbox_to_anchor=(1.05, 2.), loc=2, borderaxespad=0.)
    plt.xticks(np.arange(len(years)), (years), rotation=70)
    plt.tight_layout()
    plt.show()
