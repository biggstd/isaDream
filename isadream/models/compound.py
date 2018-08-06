'''Compound Classes of the package.

These are classes which are composed of elemental, compound, or a combination
of the two.

'''


from . import elemental
# (Factor, NodeInfo, Species, Comment)
from . import atomic
# (Info, Factors, Comments, Assays, Samples, Species)


class DrupalNode(elemental.NodeInfo, atomic.Factors, atomic.Comments, atomic.Assays,
                 atomic.Samples):
    '''Model of a single DrupalNode.
    '''

    def __init__(self, node_info, factors, comments, assays, samples):
        elemental.NodeInfo.__init__(node_info)
        atomic.Factors.__init__(factors)
        atomic.Comments.__init__(comments)
        atomic.Samples.__init__(samples)
        # Assays get passed their parrents factors and samples.
        atomic.Assays.__init__(assays, self.factors, self.samples)

    def build_frames(self, **kwargs):
        '''Call frame constructors on the child AssayNodes.
        '''
        new_frames = [assay.build_frame(**kwargs)
                      for assay in self.assays]
        return filter(None, new_frames)


class AssayNode(atomic.NodeInfo, atomic.Factors, atomic.Samples, atomic.Comments):
    '''
    '''

    def __init__(self, **kwargs):
        # TODO: Ensure that all factors in the parent DrupalNode are inherited.
        elemental.NodeInfo.__init__(node_info)
        atomic.Factors.__init__(factors)
        atomic.Comments.__init__(comments)
        atomic.Samples.__init__(samples)

        # Find any local or parental csvColumnIndexes and set those attributes.
        self.csv_index_factors = [factor for factor
                                  in self.factors + self.parental_factors
                                  + self.parental_samples.factors
                                  if factor.csv_index]

        # Read the associated csv files, and create an index of those values.
        # self.csv_values = {key: values for key, values in get_csv_column()}

        # self.factors = [factor for factor in parent and children factors]

    def collect_queried_properties(self, **kwargs):
        '''Queries and returns a dictionary of factors and species on this
        AssayNode.
        '''

        # Extract the query terms from the supplied key-value pairs.
        factor_query = kwargs.get('factors')
        species_query = kwargs.get('species')

        # Find the matching factors and species.
        factor_matches = [factor.query(factor_query)
                          for factor in self.factors + self.samples.factors
                          + self.sources.factors]
        species_matches = [species.query(species_query)
                           for species in self.species + self.samples.species
                           + self.sources.species]

        # Return the assay and the found factors.
        return {'factors':factor_matches, 'species': species_matches}


class SampleNode(atomic.NodeInfo, atomic.Factors, atomic.Species, atomic.Sources):
    '''
    '''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class SourceNode(atomic.NodeInfo, atomic.Factors, atomic.Species):
    '''
    '''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
