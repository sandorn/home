"""
PyXLL Examples: Plotting with Altair

To export altair plots to Excel you may need to install additional
dependencies. One option is to install them via conda:

conda install altair_saver selenium geckodriver firefox -c conda-forge

or

conda install altair_saver selenium python-chromedriver-binary -c conda-forge
"""
import altair as alt
import pandas as pd
import pyxll

def plot(xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plot a line chart using bokeh"""

    # Set default values for the x and y labels if they're not set
    if not xlabel:
        xlabel = "x"

    if not ylabel:
        ylabel = "y"

    # Create the pandas DataFrame
    df = pd.DataFrame({xlabel: xs, ylabel: ys})

    # Create the Altair chart
    chart = alt.Chart(df, title=title).mark_line().encode(x=xlabel, y=ylabel)

    # Show the chart in Excel
    pyxll.plot(chart, width=width, height=height, zoom=zoom)