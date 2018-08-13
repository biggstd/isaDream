"""Compound Classes of the package.

These are classes which are composed of elemental, compound, or a combination
of the two.

"""

import collections

from . import elemental
from . import containers
from . import utils


class DrupalNode:
    """Model of a single DrupalNode.

    """

    def __init__(self, assays, node_info, factors=None, comments=None, samples=None):
        """DrupalNode initialization function.

        :param node_info: A dictionary of information concerning this node object.
        :param factors: A list of factors that apply to the node and all its childeren.
        :param comments: A list of comments that apply to the node and all its childeren.
        :param samples: A list of samples that apply to the node and all its childeren.
        :param assays: A list of assays, each assay inherits the factors, samples,
            and comments above.

        """
        # Populate node attributes and properties by running parent init functions.
        self.assays = containers.Assays(assays)
        self.info = elemental.NodeInfo(node_info)
        self.title = node_info.get('title')
        # Optional values.
        self.factors = containers.Factors(factors)
        self.comments = containers.Comments(comments)
        self.samples = containers.Samples(samples)

    @property
    def all_factors(self):
        return set(utils.get_all_elementals(self, 'factors'))

    @property
    def all_species(self):
        nodes_out = list()
        for species in set(utils.get_all_elementals(self, 'species')):
            if species.dict_label is not None and species.dict_value is not None:
                nodes_out.append(species)
        return nodes_out

    @property
    def all_samples(self):
        return set(utils.get_all_elementals(self, 'samples'))

    @property
    def as_dict(self):
        return {self.title: {
            'assays': [assay.as_dict for assay in self.assays],
            'factors': [factor.as_dict for factor in self.factors],
            'samples': [sample.as_dict for sample in self.samples]
        }}


class AssayNode:
    """Model of a single assay, experiment, or user file and its metadata within a DrupalNode.

    """

    def __init__(self, datafile, node_info=None, factors=None, samples=None, comments=None,
                 parental_factors=None, parental_samples=None):
        """

        :param datafile:
        :param node_info:
        :param factors:
        :param samples:
        :param comments:
        :param parental_factors:
        :param parental_samples:
        """

        # Assay-specific factors, samples and comments.
        self._datafile = datafile

        # Merge the given parental and assay factors.
        factors = utils.join_lists([factors, parental_factors])
        samples = utils.join_lists([samples, parental_samples])

        # Initialize the container properties with their elemental instances.
        self.factors = containers.Factors(factors)
        self.samples = containers.Samples(samples)
        self.comments = containers.Comments(comments)
        self.node_info = elemental.NodeInfo(node_info)

        # Read the associated csv files, and create an index of those values.
        self.datafile_dict = utils.load_csv_as_dict(self._datafile)

    @property
    def all_factors(self):
        return utils.get_all_elementals(self, 'factors')

    @property
    def all_species(self):
        nodes_out = list()
        for species in set(utils.get_all_elementals(self, 'species')):
            if species.dict_label is not None and species.dict_value is not None:
                nodes_out.append(species)

        return nodes_out

    @property
    def species_tuple(self):
        species_maps = [{s.dict_label: s.dict_value} for s in self.all_species]
        return tuple(collections.ChainMap(*species_maps))

    @property
    def all_samples(self):
        return utils.get_all_elementals(self, 'samples')

    @property
    def csv_index_factors(self):
        """

        :return:
        """
        return [factor for factor in self.all_factors
                if factor.is_csv_index]

    @property
    def factor_size(self):
        """Get the length of the data vectors loaded from the .csv fil.e

        Consider moving this and other csv functions to a datafile class!

        :return: Integer length of the data read (if applicable) or 1.

        """
        if self.datafile_dict:
            return max(len(vals) for vals in self.datafile_dict.values())
        else:
            return 1

    # @property
    # def as_dict(self):
    #     return {self._datafile: {
    #         'data': self.datafile_dict,
    #         'factors': [factor.as_dict for factor in self.all_factors],
    #         'samples': [sample.as_dict for sample in self.samples],
    #     }}

    @property
    def as_dict(self):
        """


        :return:
        """
        # The data to be returned.
        data_source = dict()

        # We must iterate by samples so that species can properly be
        # adjusted based on their stoichiometry.
        for sample in self.all_samples:

            # Get the csv data associated with this sample.
            sample_csv_factors = (set(sample.all_factors) | set(self.all_factors)) \
                                 & set(self.csv_index_factors)

            # Get all the species associated with this sample node.
            sample_hash = list(set((s.dict_label, s.dict_value)
                                   for s in sample.all_species))
            sample_hash = '__'.join(str(x) for x in sample_hash),

            # Add the factors with csv data to data_source.
            for sample_idx_factor in sample_csv_factors:
                # Get the corresponding data array.
                data = self.datafile_dict.get(str(sample_idx_factor.csv_index))
                # Merge the factor and species keys.
                key = sample_hash + sample_idx_factor.dict_label
                # Update the output source.
                data_source[key] = data

            # Get all the factors that apply to this sample that are not csv indexes.
            sample_factors = set(sample.all_factors) - set(sample_csv_factors)

            # Iterate through the remaining, non-csv index, factors and update the dict.
            for factor in sample_factors:
                key = sample_hash + factor.dict_label
                data_source[key] = [factor.dict_value for _ in range(self.factor_size)]

        return data_source


class SampleNode:
    """SampleNode model.

    """

    def __init__(self, species, node_info=None, factors=None, sources=None):
        # Call inherited classes initialization functions.
        self.node_info = elemental.NodeInfo(node_info)
        self.sample_name = node_info.get('sampleName')
        self.factors = containers.Factors(factors)
        self.species = containers.Species(species)
        self.sources = containers.Sources(sources)

    @property
    def all_factors(self):
        return utils.get_all_elementals(self, 'factors')

    @property
    def all_species(self):
        nodes_out = list()
        for species in set(utils.get_all_elementals(self, 'species')):
            if species.dict_label is not None and species.dict_value is not None:
                nodes_out.append(species)

        return nodes_out

    @property
    def species_tuple(self):
        species_maps = [{s.dict_label: s.dict_value} for s in self.all_species]
        return tuple(collections.ChainMap(*species_maps))

    @property
    def all_sources(self):
        return utils.get_all_elementals(self, 'sources')


class SourceNode:
    """

    """

    def __init__(self, species, node_info=None, factors=None):
        self.species = containers.Species(species)
        self.node_info = elemental.NodeInfo(node_info)
        self.factors = containers.Factors(factors)

    @property
    def all_factors(self):
        return collections.ChainMap(utils.get_all_elementals(self, 'factors'))

    @property
    def all_species(self):
        return utils.get_all_elementals(self, 'species')
