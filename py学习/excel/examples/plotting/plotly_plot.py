"""
PyXLL Examples: Plotting with plotly
"""
import plotly.express as px
import pyxll

def plot(xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plot a line chart using plotly"""

    # Create the figure and plot the line chart
    fig = px.line(x=xs, y=ys, title=title, labels={"x": xlabel, "y": ylabel})

    # Plot the figure in Excel
    pyxll.plot(fig, width=width, height=height, zoom=zoom)