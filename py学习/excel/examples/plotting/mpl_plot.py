"""
PyXLL Examples: Plotting with matplotlib
"""
import matplotlib
import matplotlib.pyplot as plt
import pyxll

def plot(xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plot a line chart using matplotlib"""

    # Create the figure and plot the line chart
    fig, ax = plt.subplots()

    fig.set_edgecolor("black")
    fig.set_tight_layout({"pad": 100})

    ax.plot(xs, ys)

    # Set the labels on the axes
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

    # Plot the figure in Excel
    pyxll.plot(fig, width=width, height=height, zoom=zoom)

    # Close the pyplot figure
    plt.close(fig)