"""
PyXLL Examples: Object Cache Example

This module contains example functions that make use of the PyXLL
object cache.

When Python objects that can't be transformed into a basic type that
Excel can display are returned, PyXLL inserts them into a global
object cache and returns a reference id for the object. When this reference
id is passed to another PyXLL function the object is retrieved from the
cache and passed to the PyXLL function.

PyXLL keeps track of uses of the cached objects and removes items from the
cache when they are no longer needed.

See also the included examples.xlsx file.
"""
from pyxll import xl_func

class MyTestClass(object):
    """A basic class for testing the cached_object type"""

    def __init__(self, x):
        self.__x = x

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.__x)

@xl_func("var: object")
def cached_object_return_test(x):
    """returns an instance of MyTestClass"""
    return MyTestClass(x)

@xl_func("object: string")
def cached_object_arg_test(x):
    """takes a MyTestClass instance and returns a string"""
    return str(x)

class MyDataGrid(object):
    """
    A second class for demonstrating cached_object types.
    This class is constructed with a grid of data and has
    some basic methods which are also exposed as worksheet
    functions.
    """

    def __init__(self, grid):
        self.__grid = grid

    def sum(self):
        """returns the sum of the numbers in the grid"""
        total = 0
        for row in self.__grid:
            total += sum(row)
        return total

    def __len__(self):
        total = 0
        for row in self.__grid:
            total += len(row)
        return total

    def __str__(self):
        return "%s(%d values)" % (self.__class__.__name__, len(self))

@xl_func("float[][]: object")
def make_datagrid(x):
    """returns a MyDataGrid object"""
    return MyDataGrid(x)

@xl_func("object: int")
def datagrid_len(x):
    """returns the length of a MyDataGrid object"""
    return len(x)

@xl_func("object: float")
def datagrid_sum(x):
    """returns the sum of a MyDataGrid object"""
    return x.sum()

@xl_func("object: string")
def datagrid_str(x):
    """returns the string representation of a MyDataGrid object"""
    return str(x)
