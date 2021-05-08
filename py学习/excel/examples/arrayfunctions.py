"""
PyXLL Examples: Array functions

As well as scalar types, worksheet functions can also accept
2d arrays as arguments and return 2d arrays to Excel.

2d arrays are represented in Python as lists of lists (lists of rows),
eg:
    array = [
        [a, b, c],
        [d, e, f]
    ]

PyXLL has support for numpy arrays as well as lists of lists, and
custom types may also be array types.

When an Excel function returns an array of data it needs to be
entered by selecting the range the result will be written to,
entering the formula, and then pressing Ctrl+Shift+Enter.

PyXLL can automatically resize the range the formula result is
written to by expanding the formula range to match the size of
the returned array. To enable that the function must be registered
using the "auto_resize" option to xl_func. Alternatively, the
'auto_reisze_arrays' option may be set to 1 in the PYXLL section
of the pyxll.cfg config file to make all array functions resize
automatically.
"""
from pyxll import xl_func

#
# 1) Arrays
#

#
# Arrays in PyXll are 2d arrays that correspond to the grid in
# Excel. In python, they are represented as lists of lists.
# Arrays of any type can be used, and the var type may be
# an array of vars.
#
# Arrays of floats are more efficient to marshall between
# python and Excel than other array types so should be used
# when possible instead of var.
#
# NumPy arrays are also supported. For those, see the
# next section.
#

@xl_func("float[][] x: float")
def array_pyxll_function_1(x):
    """returns the sum of a range of floats"""
    total = 0.0
    # x is a list of lists - iterate through the rows:
    for row in x:
        # each row is a list of floats
        for element in row:
            total += element
    return total

#
# Functions can also accept and return 1d arrays.
# These can be used as array formulas in excel to return a
# column of data.
#

@xl_func("string[][] array, string sep: string[]")
def array_pyxll_function_2(x, sep):
    """joins each row by 'sep' and returns a column of strings"""
    # x is a 2d list of lists and result is a simple 1d list
    result = []
    for row in x:
        result.append(sep.join(row))
    return result

#
# the var type may also be used to pass and return arrays, but
# the python function should do any necessary type checking.
#

@xl_func("var x: string[][]")
def array_pyxll_function_3(x):
    """returns the types of the elements as strings"""
    # x may not be an array
    if not isinstance(x, list):
        return [[type(x)]]

    # x is a 2d array - list of lists.
    return [[type(e) for e in row] for row in x]

#
# The 'auto_resize' option automatically resizes the range in Excel
# to match the size of the returned array.
#

@xl_func("int rows, int cols: int[][]", auto_resize=True)
def array_resize_example(rows, cols):
    """returns an array of size rows * cols"""
    result = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(i * cols + j)
        result.append(row)
    return result

#
# var arrays may also be used.
#

@xl_func("var[][] x: string[][]", auto_resize=True)
def array_pyxll_function_4(x):
    """returns the types of the elements as strings"""
    # x will always be a 2d array - list of lists.
    return [[type(e) for e in row] for row in x]

#
# xlfCaller can be used to get information about the
# calling cell or range
#
from pyxll import xlfCaller

@xl_func("var[][] x: var[][]")
def array_pyxll_function_5(x):
    """
    return the input array with row and col numbers.

    This example shows how to use xlfCaller to get the range
    of the cells the array function is being called by.
    """
    # get the size of the rect the array function was called over
    # i.e. the size of the array to be returned
    caller = xlfCaller()
    width = caller.rect.last_col - caller.rect.first_col + 1
    height = caller.rect.last_row - caller.rect.first_row + 1

    # check the input array is the same size
    assert len(x) == height
    assert len(x[0]) == width

    # construct the return value as a list of lists with the
    # same dimensions as the calling cells.
    result = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append("%s (col=%d, row=%d)" % (x[i][j], j, i))
        result.append(row)

    return result

#
# 2) NumPy arrays
#
# the numpy_array type corresponds to the numpy.ndarray
# type.
#
# You must have numpy installed to be able to use the
# numpy_array type.
#
#

@xl_func("numpy_array x: numpy_array", auto_resize=True)
def numpy_array_function_1(x):
    # return the transpose of the array
    return x.transpose()

@xl_func("numpy_array<float_nan> x: numpy_array<float_nan>", auto_resize=True)
def numpy_array_function_2(x):
    # simply return the  array to demonstrate how errors from
    # excel may be passed to python as NaN
    return x

#
# As well as 2d arrays, 1d rows and columns may also be used
# as argument and return types.
#

@xl_func("numpy_row x: string")
def numpy_row_function_1(x):
    return str(x)

@xl_func("numpy_row x: numpy_column", auto_resize=True)
def numpy_row_function_2(x):
    return x.transpose()

@xl_func("numpy_column x: string")
def numpy_col_function_1(x):
    return str(x)

@xl_func("numpy_column x: numpy_row", auto_resize=True)
def numpy_col_function_2(x):
    return x.transpose()
