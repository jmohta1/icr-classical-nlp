import matplotlib.pyplot as plt
import numpy as np

"""For plotting the lemmatizers' data. Currently, the numbers are entered manually, but soon data will be imported and directly inputted instead."""


def plot_lemmas(errors, blanks, corrects, lemmatizers):
    colors = ["tab:orange", "gray", "tab:green"]
    lemmatizers = tuple(lemmatizers)

    performance = {
    "Incorrect": np.array(errors),
    "Blank": np.array(blanks),
    "Correct": np.array(corrects)
}

    width = 0.5
    fig, ax = plt.subplots()

    bottom = np.zeros(len(lemmatizers))

    color_index = 0
    for accuracy, weight in performance.items():
        p = ax.bar(lemmatizers, weight, width, label=accuracy, bottom=bottom, color = colors[color_index])
        bottom += weight
        color_index += 1

    ax.legend()
    
    plt.show()
