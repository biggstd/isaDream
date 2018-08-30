"""Input and Output Operations

"""

import os
import csv
import json
import uuid
import collections

from .models import utils
from isadream import DATA_MOUNT

from .models.elemental import Factor, SpeciesFactor, Comment
from .models.nodal import DrupalNode, AssayNode, SampleNode, SourceNode


def read_idream_json(json_path):
    """Read a json from a path and return as a python dictionary.

    """

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


def load_csv_as_dict(path, base_path=DATA_MOUNT):
    """Load a CSV file as a Python dictionary.

    The header in each file will be skipped.

    :param path:
    :param base_path:
    :return: A dictionary object with integer keys representing the csv
        column index the data was found in.

    """

    csv_path = os.path.join(str(base_path), str(path))

    data = collections.defaultdict(list)

    # Open the file and create a reader (an object that when iterated
    # on gives the values of each row.
    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)

        # Pop the header and get its length.
        field_int_index = range(len(next(reader)))
        field_int_index = [str(x) for x in field_int_index]

        # Iterate over the remaining rows and append the data.
        for row in reader:
            for idx, header in zip(field_int_index, reader.fieldnames):
                data[idx].append(float(row[header]))

    return dict(data)


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


def build_node_data(node: AssayNode, groups):
    """Constructs a dictionary for data display based on given groups.

    :param node:
    :param groups:

    :returns:
    """

    # Load the assay node data.
    datafile_dict = load_csv_as_dict(node.assay_datafile)

    # Get the size of this retrieved data array.
    factor_size = max(len(values) for values in datafile_dict.values())

    def matching_factors(items, label, unit, species):
        return [(label, unit, species, item)
                for item in items
                if utils.query_factor(item, unit)
                or utils.query_species(item, species)]

    def add_species(parent_sample, species_query, key, label):
        # Get the species of the provided parent sample.
        parent_species = [species for species in
                          utils.get_all_elements(parent_sample, "species")]

        # Get only those species objects which match the query.
        matching_species = [species for species in parent_species
                            if species.species_reference in species_query]

        # Add the species to the column data source.
        col_data_source[label] = [matching_species for _ in range(factor_size)]

        # Add the sample of this factor to the metadata dictionary.
        metadata_dictionary[key] = parent_sample

        # Add the sample key to the column data source.
        col_data_source["sample_node"] = [key for _ in range(factor_size)]

    def add_csv_factor(csv_factor, parent_sample, key, label):
        # Get the data using the factors csv index value, and add the
        # data to the column data source.
        col_data_source[label] = datafile_dict.get(str(csv_factor.csv_column_index))

        # Add the sample of this factor to the metadata dictionary.
        metadata_dictionary[key] = parent_sample

        # Add the key to the metadata dictionary entry to the data source.
        col_data_source["sample_node"] = [key for _ in range(factor_size)]

    def add_factor_array(factor, parent_sample, label):
        # Add the factor value to the column data source.
        col_data_source[label] = [factor.value for _ in range(factor_size)]

        # Add the sample of this factor to the metadata dictionary.
        metadata_dictionary[sample_key] = parent_sample

        # Add the key to the metadata dictionary entry to the data source.
        col_data_source["sample_node"] = [sample_key for _ in range(factor_size)]

    # Create the output dictionaries.
    col_data_source = dict()
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
        for group_sample_label, group_sample_unit, group_sample_species, parental_sample \
                in parental_sample_matches:

            sample_key = str(uuid.uuid4())

            # Check if a species reference column is requested.
            if group_sample_unit == "Species":
                add_species(parental_sample, group_sample_species, sample_key,
                            group_sample_label)

            else:
                # Get the factors that are private to this sample.
                sample_factors = matching_factors(parental_sample.factors,
                                                  group_sample_label, group_sample_unit,
                                                  group_sample_species)

                # Check each of the factors which apply to this sample for a group match.
                for factor_group in parental_factor_matches + sample_factors:
                    factor_label, factor_unit, factor_species, active_factor = factor_group

                    # Check if this factor is a csv column index.
                    if active_factor.is_csv_index:
                        add_csv_factor(active_factor, parental_sample, sample_key,
                                       group_sample_label)

                    elif group_sample_label == factor_label:
                        add_factor_array(active_factor, parental_sample, group_sample_label)

        assay_factor_matches = matching_factors(
            node.factors, group_label, group_unit, group_species)

        assay_sample_matches = matching_factors(
            node.samples, group_label, group_unit, group_species)

        # All of the parental factors apply to all of the parental samples.
        for assay_sample_label, assay_sample_unit, assay_sample_species, assay_sample \
                in assay_sample_matches:

            sample_key = str(uuid.uuid4())

            # Check if a species reference column is requested.
            if assay_sample_unit == "Species":
                add_species(assay_sample, assay_sample_species, sample_key,
                            assay_sample_label)

            else:
                # Get the factors that are private to this sample, as well as those from the parent.
                sample_factors = matching_factors(
                    assay_sample.factors, assay_sample_label, assay_sample_unit,
                    assay_sample_species)

                # Check each of the factors which apply to this sample for a group match.
                for factor_group in assay_factor_matches + sample_factors + parental_factor_matches:

                    factor_label, factor_unit, factor_species, active_factor = factor_group

                    # Check if this factor is a csv column index.
                    if active_factor.is_csv_index:
                        add_csv_factor(active_factor, assay_sample, sample_key, assay_sample_label)

                    elif assay_sample_label == factor_label:
                        add_factor_array(active_factor, assay_sample, assay_sample_label)

    return col_data_source, metadata_dictionary
