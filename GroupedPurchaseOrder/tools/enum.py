####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2014 Fabrice Salvaire
# 
####################################################################################################

"""This module extends the enum module provided in the standard Python library."""

####################################################################################################

from enum import IntEnum, EnumMeta
from types import DynamicClassAttribute

####################################################################################################

class ChoiceEnumMetaClass(EnumMeta):

    ##############################################

    def to_list(self):
        return [(item.value, item.label) for item in self]

####################################################################################################

class ChoiceEnum(IntEnum, metaclass=ChoiceEnumMetaClass):

    """This class implements integer enumerants with labels.

    >>> class Color(ChoiceEnum):
           red = ('red colour')
           green = ('green colour')
           blue = ('blue colour')

    >>> Color.red.name
    'red'

    >>> Color.red.value
    1

    >>> Color.red.label
    'red colour'

    >>> Color.to_list()
    [(1, 'red colour'), (2, 'green colour'), (3, 'blue colour')]

    """

    # Fixme: not int ! Color.red == 1 return Falsz

    ##############################################

    def __new__(cls, label):

        value = len(cls.__members__) + 1
        # TypeError: object.__new__(OrderStatus) is not safe, use int.__new__()
        obj = int.__new__(cls)
        obj._value_ = value
        obj._label_ = label
        return obj

    ##############################################

    # cf. enum, but I don't understand what is mean ...
    @DynamicClassAttribute
    def label(self):
        return self._label_

    ##############################################

    def __str__(self):
        # overwritten
        return self._label_

####################################################################################################
# 
# End
# 
####################################################################################################
