"""
PyXLL Examples: Custom types

Worksheet functions can use a number of standard types
as shown in the worksheetfuncs example.

It's also possible to define custom types that
can be used in the PyXLL function signatures
as shown by these examples.

For a more complicated custom type example see the
object cache example.
"""

#
# xl_arg_type and xl_return type are decorators that can
# be used to declare types that our excel functions
# can use in addition to the standard types
#
from pyxll import xl_func, xl_arg_type, xl_return_type

#
# 1) Custom types
#

#
# All variables are passed to and from excel as the basic types,
# but it's possible to register conversion functions that will
# convert those basic types to whatever types you like before
# they reach your function, (or after you function returns them
# in the case of returned values).
#

#
# CustomType1 is a very simple class used to demonstrate
# custom types.
#
class CustomType1:

    def __init__(self, name):
        self.name = name

    def greeting(self):
        return "Hello, my name is %s" % self.name

#
# To use CustomType1 as an argument to a pyxll function you have to
# register a function to convert from a basic type to our custom type.
#
# xl_arg_type takes two arguments, the new custom type name, and the
# base type.
#

@xl_arg_type("custom1", "string")
def string_to_custom1(name):
    return CustomType1(name)

#
# now the type 'custom1' can be used as an argument type 
# in a function signature.
#

@xl_func("custom1 x: string")
def customtype_pyxll_function_1(x):
    """returns x.greeting()"""
    return x.greeting()

#
# To use CustomType1 as a return type for a pyxll function you have
# to register a function to convert from the custom type to a basic type.
#
# xl_return_type takes two arguments, the new custom type name, and
# the base type.
#

@xl_return_type("custom1", "string")
def custom1_to_string(x):
    return x.name

#
# now the type 'custom1' can be used as the return type.
#

@xl_func("custom1 x: custom1")
def customtype_pyxll_function_2(x):
    """check the type and return the same object"""
    assert isinstance(x, CustomType1), "expected an CustomType1 object"""
    return x

#
# CustomType2 is another example that caches its instances
# so they can be referred to from excel functions.
#

class CustomType2:

    __instances__ = {}

    def __init__(self, name, value):
        self.value = value
        self.id = "%s-%d" % (name, id(self))
        
        # overwrite any existing instance with self
        self.__instances__[name] = self
      
    def getValue(self):
        return self.value

    @classmethod
    def getInstance(cls, id):
        name, unused = id.split("-")
        return cls.__instances__[name]

    def getId(self):
        return self.id

@xl_arg_type("custom2", "string")
def string_to_custom2(x):
    return CustomType2.getInstance(x)

@xl_return_type("custom2", "string")
def custom2_to_string(x):
    return x.getId()

@xl_func("string name, float value: custom2")
def customtype_pyxll_function_3(name, value):
    """returns a new CustomType2 object"""
    return CustomType2(name, value)

@xl_func("custom2 x: float")
def customtype_pyxll_function_4(x):
    """returns x.getValue()"""
    return x.getValue()

#
# custom types may be base types of other custom types, as
# long as the ultimate base type is a basic type.
#
# This means you can chain conversion functions together.
#

class CustomType3:

    def __init__(self, custom2):
        self.custom2 = custom2

    def getValue(self):
        return self.custom2.getValue() * 2

@xl_arg_type("custom3", "custom2")
def custom2_to_custom3(x):
    return CustomType3(x)

@xl_return_type("custom3", "custom2")
def custom3_to_custom2(x):
    return x.custom2

#
# when converting from an excel cell to a CustomType3 object,
# the string will first be used to get a CustomType2 object
# via the registed function string_to_custom2, and then
# custom2_to_custom3 will be called to get the final 
# CustomType3 object.
#

@xl_func("custom3 x: float")
def customtype_pyxll_function_5(x):
    """return x.getValue()"""
    return x.getValue()