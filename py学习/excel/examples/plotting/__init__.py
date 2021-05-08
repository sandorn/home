"""
PyXLL Examples: Plotting

PyXLL supports different plotting packages so that charts created in
Python can easily be viewed in Excel.

In general, you use the plotting library in exactly the same way
as you would usually but to show the plot in Excel use PyXLL's
'plot' function.

The plot function can be called from menus, macros and worksheet
functions.

If called from a worksheet function the default position of the chart
will be below the calling cell. If called from anywhere else the
default position will be below the current selection.

When called from a worksheet function the chart in Excel is given
a name and the same chart will be updated the next time the function
is called.
"""
from pyxll import xl_func, xl_arg

@xl_func
@xl_arg("xs", "float[]")
@xl_arg("ys", "float[]")
def plot_mpl(enable, xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plots a line chart using matplotlib."""
    if not enable:
        return "[Matplotlib Disabled]"
    try:
        from . import mpl_plot
        mpl_plot.plot(xs, ys, xlabel, ylabel, title, width, height, zoom)
        return "[Plotted with Matplotlib]"
    except ImportError:
        raise RuntimeError("""
matplotlib needs to be installed for this example.
Install using pip or conda and try again.
""".strip())

@xl_func
@xl_arg("xs", "float[]")
@xl_arg("ys", "float[]")
def plot_plotly(enable, xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plots a line chart using plotly."""
    if not enable:
        return "[Plotly Disabled]"
    try:
        from . import plotly_plot
        plotly_plot.plot(xs, ys, xlabel, ylabel, title, width, height, zoom)
        return "[Plotted with Plotly]"
    except ImportError:
        raise RuntimeError("""
plotly needs to be installed for this example.
Install using pip or conda and try again.
""".strip())

@xl_func
@xl_arg("xs", "float[]")
@xl_arg("ys", "float[]")
def plot_pandas(enable, xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plots a line chart using plotly."""
    if not enable:
        return "[Pandas Disabled]"
    try:
        from . import pandas_plot
        pandas_plot.plot(xs, ys, xlabel, ylabel, title, width, height, zoom)
        return "[Plotted with Pandas]"
    except ImportError:
        raise RuntimeError("""
pandas and matplotlib need to be installed for this example.
Install using pip or conda and try again.
""".strip())

@xl_func
@xl_arg("xs", "float[]")
@xl_arg("ys", "float[]")
def plot_seaborn(enable, xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plots a line chart using seaborn."""
    if not enable:
        return "[Seaborn Disabled]"
    try:
        from . import seaborn_plot
        seaborn_plot.plot(xs, ys, xlabel, ylabel, title, width, height, zoom)
        return "[Plotted with Seaborn]"
    except ImportError:
        raise RuntimeError("""
seaborn and matplotlib need to be installed for this example.
Install using pip or conda and try again.
""".strip())

@xl_func
@xl_arg("xs", "float[]")
@xl_arg("ys", "float[]")
def plot_bokeh(enable, xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plots a line chart using bokeh."""
    if not enable:
        return "[Bokeh Disabled]"
    try:
        from . import bokeh_plot
        bokeh_plot.plot(xs, ys, xlabel, ylabel, title, width, height, zoom)
        return "[Plotted with Bokeh]"
    except ImportError:
        raise RuntimeError("""
bokeh and selenium need to be installed for this example.
Install using pip or conda and try again.
""".strip())

@xl_func
@xl_arg("xs", "float[]")
@xl_arg("ys", "float[]")
def plot_altair(enable, xs, ys, xlabel=None, ylabel=None, title=None, width=None, height=None, zoom=None):
    """Plots a line chart using Altair."""
    if not enable:
        return "[Altir Disabled]"
    try:
        from . import altair_plot
        altair_plot.plot(xs, ys, xlabel, ylabel, title, width, height, zoom)
        return "[Plotted with Altair]"
    except ImportError:
        raise RuntimeError("""
altair and altair_save need to be installed for this example.
Install using pip or conda and try again.
""".strip())