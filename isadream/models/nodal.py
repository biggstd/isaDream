"""Compound Classes of the package.

These are classes which are composed of elemental, compound, or a combination
of the two.

"""

# Standard library imports.
import uuid
import collections

# Local project imports.
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


class AssayNode:
    """Model of a single assay, experiment, or user file and its metadata within a DrupalNode.

    """

    def __init__(self, datafile, node_info=None, factors=None, samples=None, comments=None,
                 parental_factors=None, parental_samples=None, parent_info=None):
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

        # Initialize the container properties with their elemental instances.
        self.factors = containers.Factors(factors)
        self.parental_factors = containers.Factors(parental_factors)
        self.parental_samples = containers.Factors(parental_samples)
        self.samples = containers.Samples(samples)
        self.comments = containers.Comments(comments)
        self.node_info = elemental.NodeInfo(node_info)
        self.parent_info = parent_info

        # Read the associated csv files, and create an index of those values.
        self.datafile_dict = utils.load_csv_as_dict(self._datafile)

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

    def build_column_data_dicts(self, groups):
        """Constructs a dictionary for data display based on given groups.

        :param groups:
        :return:
        """

        def matching_factors(items, label, unit, species):
            return [(label, unit, species, item)
                    for item in items
                    if utils.query_factor(item, unit)
                    or utils.query_species(item, species)]

        # Create the output dictionaries.
        col_data_source = dict()
        metadata_dictionary = dict()

        # Create node hashes for the metadata dictionary.
        # uuid.uuid4() gives a universally unique identifier.
        parent_key = str(uuid.uuid4())
        assay_key = str(uuid.uuid4())

        # Add the uuids to the column data source.
        col_data_source['parent_node'] = [parent_key for _ in range(self.factor_size)]
        col_data_source['assay_node'] = [assay_key for _ in range(self.factor_size)]
        # col_data_source['sample node'] = sample_key

        # Use the uuids as keys in the metadata dictionary.
        metadata_dictionary[parent_key] = self.parent_info
        metadata_dictionary[assay_key] = self.node_info

        # Iterate through and extract the values within the groups provided.
        for group_label, group_unit, group_species in groups:

            # Iterate through the top level samples and their factors.
            parental_factor_matches = matching_factors(
                self.parental_factors, group_label, group_unit, group_species)

            parental_sample_matches = matching_factors(
                self.parental_samples, group_label, group_unit, group_species)

            # All of the parental factors apply to all of the parental samples.
            for sample_label, sample_unit, sample_species, parental_sample in parental_sample_matches:

                sample_key = str(uuid.uuid4())

                # Check if a species reference column is requested.
                if sample_unit == "Species":

                    # Find the species in both the query and the sample.
                    matching_species = list(parental_sample.unique_species & set(sample_species))[0]
                    data = [matching_species for _ in range(self.factor_size)]
                    metadata_dictionary[sample_key] = parental_sample.node_info
                    col_data_source['sample_node'] = [sample_key for _ in range(self.factor_size)]
                    col_data_source[sample_label] = data

                else:
                    # Get the factors that are private to this sample.
                    sample_factors = matching_factors(
                        parental_sample.factors, sample_label, sample_unit, sample_species)

                    # Check each of the factors which apply to this sample for a group match.
                    for factor_group in parental_factor_matches + sample_factors:

                        factor_label, factor_unit, factor_species, factor = factor_group

                        # Check if this factor is a csv column index.
                        if factor.is_csv_index:
                            data = self.datafile_dict.get(factor.csv_index)
                            metadata_dictionary[sample_key] = parental_sample.node_info
                            col_data_source['sample_node'] = [sample_key for _ in range(self.factor_size)]
                            col_data_source[group_label] = data

                        elif sample_label == factor_label:
                            data = [factor.value for _ in range(self.factor_size)]
                            col_data_source[sample_label] = data
                            metadata_dictionary[sample_key] = parental_sample.node_info
                            col_data_source['sample_node'] = [sample_key for _ in range(self.factor_size)]

            assay_factor_matches = matching_factors(
                self.factors, group_label, group_unit, group_species)

            assay_sample_matches = matching_factors(
                self.samples, group_label, group_unit, group_species)

            # All of the parental factors apply to all of the parental samples.
            for sample_label, sample_unit, sample_species, assay_sample in assay_sample_matches:

                sample_key = str(uuid.uuid4())

                # Check if a species reference column is requested.
                if sample_unit == "Species":

                    # Find the species in both the query and the sample.
                    matching_species = list(assay_sample.unique_species & set(sample_species))[0]
                    data = [matching_species for _ in range(self.factor_size)]
                    col_data_source[sample_label] = data
                    metadata_dictionary[sample_key] = assay_sample.node_info
                    col_data_source['sample_node'] = [sample_key for _ in range(self.factor_size)]

                else:
                    # Get the factors that are private to this sample, as well as those from the parent.
                    sample_factors = matching_factors(
                        assay_sample.factors, sample_label, sample_unit, sample_species)

                    # Check each of the factors which apply to this sample for a group match.
                    for factor_group in assay_factor_matches + sample_factors + parental_factor_matches:

                        factor_label, factor_unit, factor_species, factor = factor_group

                        # Check if this factor is a csv column index.
                        if factor.is_csv_index:
                            data = self.datafile_dict.get(factor.csv_index)
                            col_data_source[group_label] = data
                            col_data_source['sample_node'] = [sample_key for _ in range(self.factor_size)]
                            metadata_dictionary[sample_key] = assay_sample.node_info

                        elif sample_label == factor_label:
                            data = [factor.value for _ in range(self.factor_size)]
                            col_data_source[sample_label] = data
                            col_data_source['sample_node'] = [sample_key for _ in range(self.factor_size)]
                            metadata_dictionary[sample_key] = assay_sample.node_info

        return col_data_source, metadata_dictionary


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

    def __repr__(self):
        return str(self.node_info)

    @property
    def all_factors(self):
        return utils.get_all_elementals(self, 'factors')

    @property
    def all_species(self):
        nodes_out = list()
        for species in set(utils.get_all_elementals(self, 'species')):
            if species.label is not None and species.value is not None:
                nodes_out.append(species)

        return nodes_out

    @property
    def unique_species(self):
        return set((s.label for s in self.all_species))

    # @property
    # def unique_species_tuples(self):
    #     species_maps = [{s.label: s.value} for s in self.all_species]
    #     return tuple(collections.ChainMap(*species_maps))

    @property
    def all_sources(self):
        return utils.get_all_elementals(self, 'sources')

    def query(self, query_terms):
        query_terms = utils.ensure_list(query_terms)
        if any(species.query(term)
               for term in query_terms
               for species in self.all_species):
            return True


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
