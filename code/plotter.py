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

    
def plot_accuracy(plotlines, labels):
    fig, ax = plt.subplots()
    ax.autoscale(False)
    ax.set_ybound(0, 100)
    min_xval = 0
    max_xval = 215
    ax.set_xbound(min_xval, max_xval)
    for i in range(len(plotlines)):
        print("onto the next one")
        x = np.array(plotlines[i][0])
        y = np.array(plotlines[i][1])
        ax.plot(x, y, label=labels[i]) 

    plt.legend()
    plt.show()
