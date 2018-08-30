"""Test the input/output (io) module.

"""

# ----------------------------------------------------------------------------
# Imports for Testing
# ----------------------------------------------------------------------------

from isadream import io
from isadream.models.nodal import DrupalNode


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


def test_drupal_node_io(sipos_nmr_json):
    drupal_node = io.parse_node_json(io.read_idream_json(sipos_nmr_json))
    assert isinstance(drupal_node, DrupalNode)


def test_csv_load(sipos_drupal_node):
    for assay in sipos_drupal_node.assays:
        file_path = assay.assay_datafile
        data = io.load_csv_as_dict(file_path)
        assert isinstance(data, dict)


def test_build_node_data(sipos_drupal_node, nmr_groups):
    assays = sipos_drupal_node.assays
    x_groups, y_groups = nmr_groups

    for assay in assays:
        column_data_source, metadata_dict = io.build_node_data(
            assay, x_groups + y_groups)

        assert isinstance(column_data_source, dict)
        assert isinstance(metadata_dict, dict)
