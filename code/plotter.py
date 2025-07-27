import matplotlib.pyplot as plt
import numpy as np

"""For plotting the lemmatizers' data. The functions are called by the classes in data_presentation.py."""

#plots wrong, blank, right per lemmatizer; used with StackedBarGraph class
def plot_lemmas(errors, blanks, corrects, lemmatizers, x_label, y_label):
    colors = ["darkorange", "darkgray", "steelblue"]
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
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    plt.show()

#used with AdjBarGraph class
def plot_adj_accuracies(pipelines, performances, x_label, y_label):

    x = np.arange(len(pipelines))
    width = 0.3
    shifts = 0

 
    fig, ax = plt.subplots()
    
    for ver, performance in performances.items():
        offset = width*shifts
        rects = ax.bar(x + offset, performance, width, label=ver)
        ax.bar_label(rects, padding=3)
        shifts += 1

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    ax.set_xticks(x+width*0.5, pipelines)
    ax.set_ylim(80, 90)

    plt.legend()
    
    plt.show()

#used with accuracy over time graph
def plot_accuracy(plotlines, labels, x_label, y_label):
    fig, ax = plt.subplots()
    ax.autoscale(False)
    ax.set_ybound(0, 100)
    min_xval = 0
    max_xval = 215
    ax.set_xbound(min_xval, max_xval)
    for i in range(len(plotlines)):
        x = np.array(plotlines[i][0])
        y = np.array(plotlines[i][1])
        ax.plot(x, y, label=labels[i])
        
    plt.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc="lower left", ncols=6, mode="expand")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    plt.show()
