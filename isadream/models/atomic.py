'''Property Classes of the package.

These classes define the properties of the compound Classes.

'''


class Factors:
    '''Factor list property class.

    Adds the factors property and associated functions for groups of factors.
    '''

    def __init__(self, factors=None):
        '''Initialization of a list of factors.
        '''
        self._factors = factors

    @property
    def factors(self):
        return self._factors

    @factors.setter
    def factors(self, value):
        self._factors = value


class Comments:

    def __init__(self, comments=None):
        self._comments = comments

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value):
        self._comments = value


class Assays:

    def __init__(self, assays):
        self._assays = assays

    @property
    def assays(self):
        return self._assays

    @assays.setter
    def assays(self, value):
        self._assays = value


class Samples:

    def __init__(self, samples):
        self._samples = samples

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, value):
        self._samples = value


class Species:

    def __init__(self, species):
        self._species = species

    @property
    def species(self):
        return self._species

    @species.setter
    def species(self, value):
        self._species = value

class Sources:

    def __init__(self, Sources):
        self._sources = None

    @property
    def sources(self):
        return self._sources

    @sources.setter
    def sources(self, value):
        self._sources = value