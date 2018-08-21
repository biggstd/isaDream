"""Compound Classes of the package.

These are classes which are composed of elemental, compound, or a combination
of the two.

"""

# Standard library imports.
import uuid
import collections

import param  # For type-setting.
import networkx as nx

# Local project imports.
from . import elemental
from . import containers
from .. import modelUtils


class DrupalNode(param.Parameterized):
    assays = param.List()
    info = param.Dict()
    title = param.String()
    factors = param.List()
    comments = param.List()
    samples = param.List()
    

class AssayNode:
    """Model of a single assay, experiment, or user file and its metadata within a DrupalNode.

    """

    def __init__(self, datafile, node_info=None, factors=None, samples=None, comments=None,
                 parental_factors=None, parental_samples=None, parent_info=None,
                 parent_comments=None):
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
        self.node_info = elemental.NodeInfo(info=node_info)
        self.parent_info = parent_info
        self.parent_comments = containers.Comments(parent_comments)

        # Read the associated csv files, and create an index of those values.
        self.datafile_dict = modelUtils.load_csv_as_dict(self._datafile)

    @property
    def factor_size(self):
        """Get the length of the data vectors loaded from the .csv fil.e

        Consider moving this and other csv functions to a datafile class!

        :return: Integer length of the data read (if applicable) or 1.

        """
        if self.datafile_dict:
            return max(len(values) for values in self.datafile_dict.values())
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
                    if modelUtils.query_factor(item, unit)
                    or modelUtils.query_species(item, species)]

        # Create the output dictionaries.
        col_data_source = collections.defaultdict(tuple)
        # metadata_dictionary = collections.defaultdict(tuple)
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
        metadata_dictionary[parent_key] = (self.parent_info, self.parent_comments)
        metadata_dictionary[assay_key] = (self.node_info, self.comments)

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
                    metadata_dictionary[sample_key] = parental_sample.info
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
                            data = self.datafile_dict.get(str(factor.csv_column_index))
                            metadata_dictionary[sample_key] = parental_sample.info
                            col_data_source['sample_node'] = [sample_key for _ in range(self.factor_size)]
                            col_data_source[group_label] = data

                        elif sample_label == factor_label:
                            data = [factor.value for _ in range(self.factor_size)]
                            col_data_source[sample_label] = data
                            metadata_dictionary[sample_key] = parental_sample.info
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
                    metadata_dictionary[sample_key] = assay_sample.info
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
                            data = self.datafile_dict.get(str(factor.csv_column_index))
                            col_data_source[group_label] = data
                            col_data_source['sample_node'] = [sample_key for _ in range(self.factor_size)]
                            metadata_dictionary[sample_key] = assay_sample.info

                        elif sample_label == factor_label:
                            data = [factor.value for _ in range(self.factor_size)]
                            col_data_source[sample_label] = data
                            col_data_source['sample_node'] = [sample_key for _ in range(self.factor_size)]
                            metadata_dictionary[sample_key] = assay_sample.info

        return col_data_source, metadata_dictionary


class SampleNode(param.Parameterized):
    info = param.Dict()
    sample_name = param.String()
    factors = param.List()
    species = param.List()
    sources = param.List()
    
    @property
    def all_factors(self):
        return modelUtils.get_all_elementals(self, 'factors')

    @property
    def all_species(self):
        nodes_out = list()
        for species in set(modelUtils.get_all_elementals(self, 'species')):
            if species.species_reference is not None and species.stoichiometry is not None:
                nodes_out.append(species)

        return nodes_out

    @property
    def unique_species(self):
        return set((s.species_reference for s in self.all_species))

    @property
    def all_sources(self):
        return modelUtils.get_all_elementals(self, 'sources')

    def query(self, query_terms):
        query_terms = modelUtils.ensure_list(query_terms)
        if any(species.query(term)
               for term in query_terms
               for species in self.all_species):
            return True

    @property
    def as_nx_graph(self):
        """Gives this node object as a NetworkX graph object."""
        graph = nx.DiGraph()
        graph.add_node(self)

        #         for sp in self.species:
        #             if sp:
        #                 graph.add_edge(self, sp, label="species")

        #         for factor in self.factors:
        #             if factor:
        #                 graph.add_edge(self, factor, label="factors")

        for source in self.sources:
            if source:
                # Create the graph as a balanced tree and find the root node.
                source_graph = source.as_nx_graph
                #                 root_node = list(nx.topological_sort(source_graph))[0]
                graph.add_edge(self, source, label="sources")

                #                 graph.add_nodes_from(source_graph.nodes(data=True))
                #                 graph.add_edges_from(source_graph.edges(data=True))
                graph = nx.disjoint_union(graph, source_graph)

        return graph


class SourceNode(param.Parameterized):
    species = param.List()
    info = param.Dict()
    factors = param.List()
    
    @property
    def all_factors(self):
        return collections.ChainMap(modelUtils.get_all_elementals(self, 'factors'))

    @property
    def all_species(self):
        return modelUtils.get_all_elementals(self, 'species')

    @property
    def as_nx_graph(self):
        """Gives this node object as a NetworkX graph object."""
        graph = nx.DiGraph()
        graph.add_node(self)

        for sp in self.species:
            if sp:
                graph.add_edge(self, sp, label="species")

        for factor in self.factors:
            if factor:
                graph.add_edge(self, factor, label="factors")

        return graph
