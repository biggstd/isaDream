"""Tests

"""

# ----------------------------------------------------------------------------
# Imports for Testing
# ----------------------------------------------------------------------------

from isadream.models.nodal import DrupalNode, SampleNode, SourceNode, AssayNode


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


def test_source_node_creation(source_node_fixtures):
    for source_node in source_node_fixtures:
        assert isinstance(source_node, SourceNode)


def test_sample_node_creation(sample_node_fixtures):
    for sample_node in sample_node_fixtures:
        assert isinstance(sample_node, SampleNode)


def test_assay_node_creation(assay_node_fixtures):
    for assay_node in assay_node_fixtures:
        assert isinstance(assay_node, AssayNode)


def test_drupal_node_creation(drupal_node_fixture_a):
    assert isinstance(drupal_node_fixture_a, DrupalNode)
