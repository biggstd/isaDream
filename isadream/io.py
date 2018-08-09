import json

from .models import utils
from .models import elemental
from .models import nodal


FACTOR_NAMES = '''studyFactors studySampleFactors materialCharacteristic
    studySampleFactors AssaySampleFactors parameters assayParameters'''.split()

FACTOR_FIELDS = '''factorType decimalValue unitRef csvColumnIndex RefValue
stringValue'''.split()

SAMPLE_NAMES = '''studySamples samples'''.split()

SAMPLE_VALUES = '''species sources'''.split()

SPECIES_VALUES = '''speciesReference stoichiometry'''.split()


def parse_factors(json_str):
    """Find and return a factor, regardless of what the factors name
    within the json specification.
    """

    for factor_name in FACTOR_NAMES:
        if json_str.get(factor_name):
            return list(elemental.Factor(fact) for fact in json_str.pop(factor_name))
        else:
            continue
    return []


def read_idream_json(json_path):
    """Read a json from a path and return as a python dictionary.
    """

    with open(json_path) as json_file:
        data = json.load(json_file)
    return data


def _build_from_field(callable_fn, json_data, key=None):
    """Returns a callable() or None for every entry found from json_data.

    """

    if key and json_data.get(key):
        return list(callable_fn(dat) for dat in json_data.pop(key) if dat)
    else:
        return utils.ensure_list(callable_fn(json_data))


# TODO: Rename me.
def parse_json(raw_json_dict):
    """Convert a dictionary to a DrupalNode object.

    """

    # Create the Factors.
    factor_nodes = _build_from_field(parse_factors, raw_json_dict)

    # Parse the samples.
    sample_nodes = _build_from_field(parse_sample, raw_json_dict,
                                     'studySamples')

    # Parse the assays.
    assay_nodes = _build_from_field(parse_assays, raw_json_dict, 'assays')
    # Add the parental factors and samples to the assay_nodes.
    for node in assay_nodes:
        node.factors.extend(factor_nodes)
        node.samples.extend(sample_nodes)

    # Create the Comments.
    comment_nodes = _build_from_field(elemental.Comment, raw_json_dict,
                                      'comments')

    # Create the DrupalNode
    return nodal.DrupalNode(assays=assay_nodes, node_info=raw_json_dict.get('nodeInformation'),
                            factors=factor_nodes, comments=comment_nodes,
                            samples=sample_nodes)


def parse_sample(sample_json):
    """

    :param sample_json:
    :return:
    """
    # Create the Factors.
    factor_nodes = _build_from_field(parse_factors, sample_json)

    # Create the Species.
    species_nodes = _build_from_field(elemental.SpeciesFactor, sample_json, 'species')

    # Create the Sources.
    source_nodes = _build_from_field(parse_source, sample_json, 'sources')

    return nodal.SampleNode(node_info=sample_json, species=species_nodes,
                            factors=factor_nodes, sources=source_nodes)


def parse_source(source_json):
    """

    :param source_json:
    :return:
    """
    # print(source_json)

    # Get the factors within this source.
    factor_nodes = _build_from_field(parse_factors, source_json)

    # Get the species within this source.
    species_nodes = _build_from_field(elemental.SpeciesFactor, source_json, 'species')

    # TODO: Rexamine nested sources (low priority).
    # Sources can be nested!
    # source_json = source_json.get('sources')
    # if source_json:
    #     source_nodes = _build_from_field(parse_source, source_json)
    # else:
    #     source_nodes = None

    # Build the source node and return it.
    return nodal.SourceNode(node_info=source_json, factors=factor_nodes,
                            species=species_nodes)


def parse_assays(assay_json):
    """

    :param assay_json:
    :return:
    """
    # Get the datafile.
    data_file = assay_json.get('dataFile')

    # Create the Samples
    sample_nodes = _build_from_field(parse_sample, assay_json, 'samples')

    factor_nodes = _build_from_field(parse_factors, assay_json)
    # print(factor_nodes)

    # Create the Comments.
    # TODO: Examine comment nodes, gives strange results sometimes.
    comment_nodes = _build_from_field(elemental.Comment, assay_json, 'comments')

    return nodal.AssayNode(datafile=data_file, node_info=assay_json,
                           factors=factor_nodes, samples=sample_nodes,
                           comments=comment_nodes)


def source_to_dict(source_node):
    """
    # TODO: Consider having this as a part of the DataFile class.

    :param assay_node:
    :return:
    """
    # Get a set of all unique factors of this assay.

    # Get a set of all unique samples of this assay.

    # Get a set of all unique species of this assay.
