"""
PyXLL Examples: Plotting with pandas
"""
import pandas as pd
import matplotlib.pyplot as plt
import pyxll

def plot(xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plot a line chart using matplotlib"""

    # Create the pandas DataFrame
    df = pd.DataFrame({"y": ys}, index=xs)

    # Add the labels
    if xlabel:
        df.index.name = xlabel

    if ylabel:
        df.rename(columns={"y": ylabel}, inplace=True)

    # Create the figure and axes to plot the series onto
    fig, ax = plt.subplots()

    # Plot the series onto the axes
    df.plot(ax=ax, title=title)

    # Plot the figure in Excel
    pyxll.plot(fig, width=width, height=height, zoom=zoom)

    # Close the pyplot figure
    plt.close(fig)