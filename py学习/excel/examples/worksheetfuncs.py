"""
PyXLL Examples: Worksheet functions

The PyXLL Excel Addin is configured to load one or more
python modules when it's loaded. Functions are exposed
to Excel as worksheet functions by decorators declared in
the pyxll module.

Functions decorated with the xl_func decorator are exposed
to Excel as UDFs (User Defined Functions) and may be called
from cells in Excel.
"""

#
# 1) Basics - exposing functions to Excel
#

#
# xl_func is the main decorator and is used for exposing
# python functions to excel.
#
from pyxll import xl_func

#
# Decorating a function with xl_func is all that's required
# to make it callable in Excel as a worksheet function.
#
@xl_func
def basic_pyxll_function_1(x, y, z):
    """returns (x * y) ** z """
    return (x * y) ** z

#
# xl_func takes an optional signature of the function to be exposed to excel.
# There are a number of basic types that can be used in
# the function signature. These include:
#   int, float, bool and string
# There are more types that we'll come to later.
#

@xl_func("int x, float y, bool z: float")
def basic_pyxll_function_2(x, y, z):
    """if z return x, else return y"""
    if z:
        # we're returning an integer, but the signature
        # says we're returning a float.
        # PyXLL will convert the integer to a float for us.
        return x
    return y

#
# You can change the category the function appears under in
# Excel by using the optional argument 'category'.
#

@xl_func(category="My new PyXLL Category")
def basic_pyxll_function_3(x):
    """docstrings appear as help text in Excel"""
    return x

#
# 2) The var type
#

#
# A basic type is the var type. This can represent any
# of the basic types, depending on what type is passed to the
# function, or what type is returned.
#
# When no type information is given the var type is used.
#

@xl_func("var x: string")
def var_pyxll_function_1(x):
    """takes an float, bool, string, None or array"""
    # we'll return the type of the object passed to us, pyxll
    # will then convert that to a string when it's returned to
    # excel.
    return type(x)

#
# If var is the return type. PyXll will convert it to the
# most suitable basic type. If it's not a basic type and
# no suitable conversion can be found, it will be converted
# to a string and the string will be returned.
#

@xl_func("bool x: var")
def var_pyxll_function_2(x):
    """if x return string, else a number"""
    if x:
        return "var can be used to return different types"
    return 123.456

#
# 3) Date and time types
#

#
# There are three date and time types: date, time, datetime
#
# Excel represents dates and times as floating point numbers.
# The pyxll datetime types convert the excel number to a
# python datetime.date, datetime.time and datetime.datetime
# object depending on what type you specify in the signature.
#
# dates and times may be returned using their type as the return
# type in the signature, or as the var type.
#

import datetime

@xl_func("date x: string")
def datetime_pyxll_function_1(x):
    """returns a string description of the date"""
    return "type=%s, date=%s" % (type(x), x)

@xl_func("time x: string")
def datetime_pyxll_function_2(x):
    """returns a string description of the time"""
    return "type=%s, time=%s" % (type(x), x)

@xl_func("datetime x: string")
def datetime_pyxll_function_3(x):
    """returns a string description of the datetime"""
    return "type=%s, datetime=%s" % (type(x), x)

@xl_func("datetime[][] x: datetime")
def datetime_pyxll_function_4(x):
    """returns the max datetime"""
    m = datetime.datetime(1900, 1, 1)
    for row in x:
        m = max(m, max(row))
    return m

#
# 4) xl_cell
#
# The xl_cell type can be used to receive a cell
# object rather than a plain value. The cell object
# has the value, address, formula and note of the
# reference cell passed to the function.
#
# The function must be a macro sheet equivalent function
# in order to access the value, address, formula and note
# properties of the cell.
#

@xl_func("xl_cell cell : string", macro=True)
def xl_cell_example(cell):
    """a cell has a value, address, formula and note"""
    return "[value=%s, address=%s, formula=%s, note=%s]" % (cell.value,
                                                            cell.address,
                                                            cell.formula,
                                                            cell.note)

#
# 5) recalc_on_open
#
# Functions can be marked to be recalculated when the workbook opens.
# With this set, when the workbook is saved some metadata is written
# with the workbook and then the cell containing the function is marked
# as dirty when the workbook is loaded, causing it to be recalculated.
#

@xl_func(recalc_on_open=True)
def recalc_on_open_test():
    now = datetime.datetime.now()
    return now.strftime("Updated at %Y-%m-%d %H:%M:%S")

#
# 6) Formatting
#
# PyXLL can automatically apply a formatter to the range the function is called from.
#
from pyxll import Formatter

date_formatter = Formatter(number_format="YYYY-mm-dd")

@xl_func(formatter=date_formatter, recalc_on_open=True)
def formatted_datetime_pyxll_function():
    return datetime.date.today()

# Formatters can be combined by adding them
highlight_formatter = Formatter(interior_color=Formatter.rgb(255, 255, 0), bold=True)

@xl_func(formatter=date_formatter + highlight_formatter, recalc_on_open=True)
def formatted_datetime_pyxll_function_2():
    return datetime.date.today()