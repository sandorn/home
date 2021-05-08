"""
PyXLL Examples: Plotting with seaborn
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pyxll

def plot(xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plot a line chart using matplotlib"""

    # Set the seaborn style to 'darkgrid'
    with sns.axes_style("darkgrid"):

        # Create the figure and plot the line chart
        fig, ax = plt.subplots()

        # Use seaborn to make the line plot
        sns.lineplot(xs, ys, ax=ax)

        # Set the labels on the axes
        ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

        # Plot the figure in Excel
        pyxll.plot(fig, width=width, height=height, zoom=zoom)

        # Close the pyplot figure
        plt.close(fig)