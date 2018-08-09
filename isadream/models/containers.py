"""Property Classes of the package.

These classes define the properties of the compound Classes. Such properties
contain lists of `elemental` classes.

"""

from . import utils

import collections


class Factors(collections.UserList):
    """Factor list property class."""

    @property
    def as_dict(self):
        return collections.ChainMap(*[item.as_dict for item in self])


class Comments(collections.UserList):
    @property
    def as_dict(self):
        return collections.ChainMap(*[item.as_dict for item in self])


class Assays(collections.UserList):
    @property
    def as_dict(self):
        return collections.ChainMap(*[item.as_dict for item in self])


class Samples(collections.UserList):
    """Property class for those classes that must hold a list of SampleNode objects."""

    @property
    def as_dict(self):
        return collections.ChainMap(*[item.as_dict for item in self])


class Species(collections.UserList):
    """Property class for those that must hold a list of SpeciesFactor objects."""

    @property
    def as_dict(self):
        return collections.ChainMap(*[item.as_dict for item in self])


class Sources(collections.UserList):
    """Property class for classes that must hold a list of SourceNode objects. """

    @property
    def as_dict(self):
        return collections.ChainMap(*[item.as_dict for item in self])
