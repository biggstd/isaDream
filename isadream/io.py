"""Input and Output Operations

"""

import json
import uuid
import collections

from . import modelUtils
from .models.elemental import Factor, SpeciesFactor, Comment, NodeInfo, DataFile
from .models.nodal import DrupalNode, AssayNode, SampleNode, SourceNode


def read_idream_json(json_path):
    """Read a json from a path and return as a python dictionary. """
    with open(json_path) as json_file:
        data = json.load(json_file)
    return data


def build_elemental_model(json_dict, model, key):
    # Many entries are optional, ensure the entry exists.
    if json_dict.get(key):
        model_list = json_dict.get(key)
        return [model(**kwargs) for kwargs in model_list]
    return []


def build_nodal_model(json_dict, model, key):
    if json_dict.get(key):
        model_list = json_dict.get(key)
        return [model(item) for item in model_list]
    return []


def parse_sources(json_dict):
    source_name = json_dict.get("source_name")
    factors = build_elemental_model(json_dict, Factor, "source_factors")
    species = build_elemental_model(json_dict, SpeciesFactor, "source_species")
    comments = build_elemental_model(json_dict, Comment, "source_comments")

    return SourceNode(source_name=source_name, species=species, factors=factors,
                      comments=comments)


def parse_samples(json_dict):
    sample_name = json_dict.get("sample_name")
    factors = build_elemental_model(json_dict, Factor, "sample_factors")
    species = build_elemental_model(json_dict, SpeciesFactor, "sample_species")
    comments = build_elemental_model(json_dict, Comment, "sample_comments")

    sources = build_nodal_model(json_dict, parse_sources, "sample_sources")

    return SampleNode(sample_name=sample_name, factors=factors, species=species,
                      sources=sources, comments=comments)


def parse_assays(json_dict):
    assay_title = json_dict.get("assay_title")
    assay_datafile = json_dict.get("assay_datafile")

    comments = build_elemental_model(json_dict, Comment, "assay_comments")
    factors = build_elemental_model(json_dict, Factor, "assay_factors")

    samples = build_nodal_model(json_dict, parse_samples, "assay_samples")

    return AssayNode(assay_title=assay_title, assay_datafile=assay_datafile,
                     comments=comments, factors=factors, samples=samples)


def parse_node_json(json_dict):
    """Convert a dictionary to a DrupalNode object. """
    # Info, factors and comments can be directly created from the json.
    info = json_dict.get("node_information")
    factors = build_elemental_model(json_dict, Factor, "node_factors")
    comments = build_elemental_model(json_dict, Comment, "node_comments")

    # Samples and assays have nested items, and require more processing.
    samples = build_nodal_model(json_dict, parse_samples, "node_samples")
    assays = build_nodal_model(json_dict, parse_assays, "node_assays")

    for assay in assays:
        assay.parental_factors = factors
        assay.parental_samples = samples
        assay.parental_info = info
        assay.parental_comments = comments

    return DrupalNode(info=info, assays=assays, factors=factors,
                      samples=samples, comments=comments)


def build_node_data(node, groups):
    """Constructs a dictionary for data display based on given groups.

    :param groups:
    :return:
    """

    def matching_factors(items, label, unit, species):
        return [(label, unit, species, item)
                for item in items
                if modelUtils.query_factor(item, unit)
                or modelUtils.query_species(item, species)]

    datafile_dict = modelUtils.load_csv_as_dict(node.assay_datafile)

    factor_size = max(len(values) for values in datafile_dict.values())

    # Create the output dictionaries.
    col_data_source = dict()  # collections.defaultdict(tuple)
    metadata_dictionary = dict()

    # Create node hashes for the metadata dictionary.
    # uuid.uuid4() gives a universally unique identifier.
    parent_key = str(uuid.uuid4())
    assay_key = str(uuid.uuid4())

    # Add the uuids to the column data source.
    col_data_source['parent_node'] = [parent_key for _ in range(factor_size)]
    col_data_source['assay_node'] = [assay_key for _ in range(factor_size)]
    # col_data_source['sample node'] = sample_key

    # Use the uuids as keys in the metadata dictionary.
    metadata_dictionary[parent_key] = (node.parental_info, node.parental_comments)
    metadata_dictionary[assay_key] = (node.assay_title, node.comments)

    # Iterate through and extract the values within the groups provided.
    for group_label, group_unit, group_species in groups:

        # Iterate through the top level samples and their factors.
        parental_factor_matches = matching_factors(
            node.parental_factors, group_label, group_unit, group_species)

        parental_sample_matches = matching_factors(
            node.parental_samples, group_label, group_unit, group_species)

        # All of the parental factors apply to all of the parental samples.
        for sample_label, sample_unit, sample_species, parental_sample in parental_sample_matches:

            sample_key = str(uuid.uuid4())

            # Check if a species reference column is requested.
            if sample_unit == "Species":

                # Find the species in both the query and the sample.
                matching_species = list(parental_sample.unique_species & set(sample_species))[0]
                data = [matching_species for _ in range(factor_size)]
                metadata_dictionary[sample_key] = parental_sample.info
                col_data_source['sample_node'] = [sample_key for _ in range(factor_size)]
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
                        data = datafile_dict.get(str(factor.csv_column_index))
                        metadata_dictionary[sample_key] = parental_sample.sample_name
                        col_data_source['sample_node'] = [sample_key for _ in range(factor_size)]
                        col_data_source[group_label] = data

                    elif sample_label == factor_label:
                        data = [factor.value for _ in range(factor_size)]
                        col_data_source[sample_label] = data
                        metadata_dictionary[sample_key] = parental_sample.sample_name
                        col_data_source['sample_node'] = [sample_key for _ in range(factor_size)]

        assay_factor_matches = matching_factors(
            node.factors, group_label, group_unit, group_species)

        assay_sample_matches = matching_factors(
            node.samples, group_label, group_unit, group_species)

        # All of the parental factors apply to all of the parental samples.
        for sample_label, sample_unit, sample_species, assay_sample in assay_sample_matches:

            sample_key = str(uuid.uuid4())

            # Check if a species reference column is requested.
            if sample_unit == "Species":

                # Find the species in both the query and the sample.
                matching_species = list(assay_sample.unique_species & set(sample_species))[0]
                data = [matching_species for _ in range(factor_size)]
                col_data_source[sample_label] = data
                metadata_dictionary[sample_key] = assay_sample.sample_name
                col_data_source['sample_node'] = [sample_key for _ in range(factor_size)]

            else:
                # Get the factors that are private to this sample, as well as those from the parent.
                sample_factors = matching_factors(
                    assay_sample.factors, sample_label, sample_unit, sample_species)

                # Check each of the factors which apply to this sample for a group match.
                for factor_group in assay_factor_matches + sample_factors + parental_factor_matches:

                    factor_label, factor_unit, factor_species, factor = factor_group

                    # Check if this factor is a csv column index.
                    if factor.is_csv_index:
                        data = datafile_dict.get(str(factor.csv_column_index))
                        col_data_source[group_label] = data
                        col_data_source['sample_node'] = [sample_key for _ in range(factor_size)]
                        metadata_dictionary[sample_key] = assay_sample.sample_name

                    elif sample_label == factor_label:
                        data = [factor.value for _ in range(factor_size)]
                        col_data_source[sample_label] = data
                        col_data_source['sample_node'] = [sample_key for _ in range(factor_size)]
                        metadata_dictionary[sample_key] = assay_sample.sample_name

    return col_data_source, metadata_dictionary
