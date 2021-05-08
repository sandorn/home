"""
PyXLL Examples: Pandas

This module contains example functions that show how pandas DataFrames and Series
can be passed to and from Excel to Python functions using PyXLL.

Pandas needs to be installed for this example to work correctly.

See also the included examples.xlsx file.
"""
from pyxll import xl_func, DataFrameFormatter

@xl_func(volatile=True)
def pandas_is_installed():
    """returns True if pandas is installed"""
    try:
        import pandas
        return True
    except ImportError:
        return False

# The DataFrameFormatter object can be used for format DataFrames returned to Excel from PyXLL.
df_formatter = DataFrameFormatter()

@xl_func("int, int: dataframe<index=True>",
         auto_resize=True,
         formatter=df_formatter)
def random_dataframe(rows, columns):
    """
    Creates a DataFrame of random numbers.

    :param rows: Number of rows to create the DataFrame with.
    :param columns: Number of columns to create the DataFrame with.
    """
    import pandas as pa
    import numpy as np

    data = np.random.rand(rows, columns)
    column_names = [chr(ord('A') + x) for x in range(columns)]
    df = pa.DataFrame(data, columns=column_names)

    return df

@xl_func("dataframe<index=True>, float[], str[], str[]: dataframe<index=True>",
         auto_resize=True,
         formatter=df_formatter)
def describe_dataframe(df, percentiles=[], include=[], exclude=[]):
    """
    Generates descriptive statistics that summarize the central tendency, dispersion and shape of a dataset's
    distribution, excluding NaN values.

    :param df: DataFrame to describe.
    :param percentiles: The percentiles to include in the output. All should fall between 0 and 1.
    :param include: dtypes to include.
    :param exclude: dtypes to exclude.
    :return:
    """
    # filter out any blanks
    percentiles = list([_f for _f in percentiles if _f])
    include = list([_f for _f in include if _f])
    exclude = list([_f for _f in exclude if _f])

    return df.describe(percentiles=percentiles or None,
                       include=include or None,
                       exclude=exclude or None)