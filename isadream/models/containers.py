"""Container classes for isadream.

These classes (list place-holders for now) are where the logic of ensuring valid
objects are added to containers.

"""


import collections


class Factors(collections.UserList):
    """Factor list property class."""
    pass


class Comments(collections.UserList):
    pass


class Assays(collections.UserList):
    pass


class Samples(collections.UserList):
    """Property class for those classes that must hold a list of SampleNode objects."""
    pass


class Species(collections.UserList):
    """Property class for those that must hold a list of SpeciesFactor objects."""
    pass


class Sources(collections.UserList):
    """Property class for classes that must hold a list of SourceNode objects. """
    pass
