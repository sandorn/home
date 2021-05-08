"""
PyXLL Examples: Plotting with bokeh

To export bokeh plots to Excel you may need to install additional
dependencies. One option is to install them via conda:

conda install selenium geckodriver firefox -c conda-forge

or

conda install selenium python-chromedriver-binary -c conda-forge
"""
from bokeh.plotting import figure
import pyxll

def plot(xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plot a line chart using bokeh"""

    # Create the bokeh figure
    graph = figure(title=title, x_axis_label=xlabel, y_axis_label=ylabel)

    # Plot the line chart
    graph.line(xs, ys)

    # Show the plot in Excel
    pyxll.plot(graph, width=width, height=height, zoom=zoom)