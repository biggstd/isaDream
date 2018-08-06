import json


from .models import elemental
# Factor, NodeInfo, Species, Comment
from .models import compound
# DrupalNode, SampleNode, AssayNode, SourceNode


FACTOR_NAMES = '''studyFactors studySampleFactors materialCharacteristic
    studySampleFactors AssaySampleFactors'''.split()


def parse_factors(json_str):
    '''Find and return a factor, regardless of what the factors name
    within the json specification.
    '''
    for factor_name in FACTOR_NAMES:
        if json_str.get(factor_name):
            return [elemental.Factor(fact)
                    for fact in json_str.get(factor_name)]
        else:
            return None


def read_idream_json(json_path):
    '''Read a json from a path and return as a python dictionary.
    '''
    with open(json_path) as json_file:
        data = json.load(json_file)
    return data


def _build_from_field(callable, json_data, key=None):
    '''Returns a callable() or None for every entry found from json_data.
    '''
    if key and json_data.get(key):
        return [callable(dat) for dat in json_data.get(key) if dat]
    else:
        return callable(json_data)


# TODO: Rename me.
def parse_json(raw_json_dict):
    '''Convert a dictionary to a DrupalNode object.

    '''

    # Create the NodeInfo.
    info_node = _build_from_field(elemental.NodeInfo, raw_json_dict,
                                 'nodeInformation')

    # Create the Factors.
    factor_nodes = _build_from_field(parse_factors, raw_json_dict)

    # Parse the samples.
    sample_nodes = _build_from_field(parse_samples, raw_json_dict,
                                    'studySamples')

    # Parse the assays.
    assay_nodes = _build_from_field(parse_assays, raw_json_dict, 'assays')

    # Create the Comments.
    comment_nodes = _build_from_field(elemental.Comment, raw_json_dict,
                                     'comments')

    # Create the DrupalNode
    return compound.DrupalNode(info=info_node, factors=factor_nodes,
                               comments=comment_nodes, assays=assay_nodes,
                               samples=sample_nodes)


def parse_samples(study_json):
    '''
    '''
    # Create the Factors.
    factor_nodes = _build_from_field(parse_factors, study_json)

    # Create the Species.
    species_nodes = _build_from_field(elemental.Species, study_json, 'species')

    # Create the Sources.
    source_nodes = _build_from_field(parse_source, study_json, 'sources')

    return compound.SampleNode(factors=factor_nodes, species=species_nodes,
                      sources=source_nodes)


def parse_source(source_json):
    '''Parse a json for sources.
    '''
    # Get the factors within this source.
    factor_nodes = _build_from_field(parse_factors, source_json)

    # Get the species within this source.
    species_nodes = _build_from_field(elemental.Species, source_json, 'species')

    # # Sources can be nested!
    # source_json = source_json.get('sources')
    # if source_json:
    #     source_nodes = _build_from_field(parse_source, source_json)
    # else:
    #     source_nodes = None

    # Build the source node and return it.
    return compound.SourceNode(factors=factor_nodes, species=species_nodes)


def parse_assays(assay_json):
    # Create the Samples
    sample_nodes = _build_from_field(parse_samples, assay_json, 'samples')

    # Create the Comments.
    comment_nodes = _build_from_field(elemental.Comment, assay_json, 'comments')

    return compound.AssayNode(samples=sample_nodes, comments=comment_nodes)
