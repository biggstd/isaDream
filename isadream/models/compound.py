'''Compound Classes of the package.

These are classes which are composed of atomic, compound, or a combination
of the two.

'''

class AbstractNode:
    '''
    nodeinfo
    factors
    comments
    '''

    def __init__(self, node_info=None, factors=None, comments=None):
        self._node_dict = node_info
        self._factors = factors
        self._comments = comments

    @property
    def nodeinfo(self):
        return self._node_dict

    @property
    def factors(self):
        return self._factors

    @property
    def comments(self):
        return self._comments


class DrupalNode(AbstractNode):
    '''
    assays
    samples
    '''

    def __init__(self, assays=None, samples=None, **kwargs):
        # Call the AbstractNode __init__().
        self._assays = assays
        self._samples = samples
        super().__init__(**kwargs)

    @property
    def assays(self):
        return self._assays

    @property
    def samples(self):
        return self._samples

    def __str__(self):
        return str(self.nodeinfo)

class AssayNode(AbstractNode):
    '''
    samples
    '''
    def __init__(self, samples=None, **kwargs):
        # Call the AbstractNode __init__().
        self._samples = samples
        super().__init__(**kwargs)

    @property
    def samples(self):
        return self._samples

    def __str__(self):
        sample_strs = [str(s) for s in self.samples]
        return '\n'.join(sample_strs)


class SampleNode(AbstractNode):
    '''
    species
    sources
    '''
    def __init__(self, species=None, sources=None, **kwargs):
        # Call the AbstractNode __init__().
        self._species = species
        self._sources = sources
        super().__init__(**kwargs)

    @property
    def species(self):
        return self._species

    @property
    def sources(self):
        return self._sources

    def __str__(self):
        species_strs = [str(s) for s in self.species]
        sources_strs = [str(s) for s in self.sources]
        return '\n'.join(species_strs + sources_strs)

class SourceNode(SampleNode):
    '''
    species
    sources
    '''
