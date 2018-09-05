"""Shared test fixtures.

"""

# ----------------------------------------------------------------------------
# General Imports
# ----------------------------------------------------------------------------
import os
import pytest

# ----------------------------------------------------------------------------
# Imports for Testing
# ----------------------------------------------------------------------------

from isadream import config, demos

from isadream import io
from isadream.models.elemental import Factor, SpeciesFactor, Comment
from isadream.models.nodal import SourceNode, SampleNode, AssayNode, DrupalNode

# ----------------------------------------------------------------------------
# Globals and constants
# ----------------------------------------------------------------------------
# Json demo files.
SIPOS = demos["SIPOS_NMR"]
RAMAN = demos["SIPOS_RAMAN"]


# ----------------------------------------------------------------------------
# Key-value Fixtures
# ----------------------------------------------------------------------------

@pytest.fixture
def factor_kwargs():
    return [
        {
            "factor_type": "Measurement Condition",
            "decimal_value": 18.0,
            "unit_reference": "Molar"
        },
        {
            "factor_type": "Measurement Condition",
            "unit_reference": "Molar",
            "csv_column_index": 0
        },
        {
            "factor_type": "Measurement Condition",
            "unit_reference": "Integrated Intensity",
            "csv_column_index": 1
        },
        {
            "factor_type": "Measurement Condition",
            "unit_reference": "cm-1",
            "csv_column_index": 2
        }
    ]


@pytest.fixture
def species_factor_kwargs():
    return [
        {
            "species_reference": "Na+",
            "stoichiometry": 1.0
        },
        {
            "species_reference": "OH-",
            "stoichiometry": 1.0
        }
    ]


@pytest.fixture
def comment_kwargs():
    return [
        {
            "comment_title": "Test comment number 1.",
            "body": "Test comment 1 body."
        }
    ]


# ----------------------------------------------------------------------------
# Elemental Model Fixtures
# ----------------------------------------------------------------------------

@pytest.fixture
def factor_fixtures(factor_kwargs):
    return [Factor(**kwargs) for kwargs in factor_kwargs]


@pytest.fixture
def species_factor_fixtures(species_factor_kwargs):
    return [SpeciesFactor(**kwargs) for kwargs in species_factor_kwargs]


@pytest.fixture
def comment_factor_fixtures(comment_kwargs):
    return [Comment(**kwargs) for kwargs in comment_kwargs]


# ----------------------------------------------------------------------------
# Nodal Model Fixtures
# ----------------------------------------------------------------------------


@pytest.fixture
def source_node_fixtures(factor_fixtures, species_factor_fixtures,
                         comment_factor_fixtures):
    return [SourceNode(**dict(source_name="Test Source",
                              species=species_factor_fixtures,
                              factors=factor_fixtures,
                              comments=comment_factor_fixtures))]


@pytest.fixture
def sample_node_fixtures(factor_fixtures, species_factor_fixtures,
                         comment_factor_fixtures, source_node_fixtures):
    return [SampleNode(**dict(source_name="Test Sample",
                              species=species_factor_fixtures,
                              factors=factor_fixtures,
                              sources=source_node_fixtures,
                              comments=comment_factor_fixtures))]


@pytest.fixture
def assay_node_fixtures(factor_fixtures, sample_node_fixtures,
                        comment_factor_fixtures):
    return [AssayNode(**dict(assay_datafile="some_datafile.csv",
                             assay_title="Some assay title.",
                             factors=factor_fixtures,
                             samples=sample_node_fixtures,
                             comments=comment_factor_fixtures))]


@pytest.fixture
def drupal_node_fixture_a(assay_node_fixtures, factor_fixtures,
                          sample_node_fixtures, comment_factor_fixtures):
    return DrupalNode(**dict(title="Drupal Node A",
                             assays=assay_node_fixtures,
                             factors=factor_fixtures,
                             samples=sample_node_fixtures,
                             comments=comment_factor_fixtures))


@pytest.fixture
def sipos_drupal_node(sipos_nmr_json):
    return io.parse_node_json(io.read_idream_json(sipos_nmr_json))


# ----------------------------------------------------------------------------
# JSON Data Fixtures
# ----------------------------------------------------------------------------


@pytest.fixture
def sipos_nmr_json():
    return SIPOS


# ----------------------------------------------------------------------------
# QueryGroup Fixtures
# ----------------------------------------------------------------------------


@pytest.fixture
def nmr_groups():
    x_groups = (('Total Aluminate Concentration', 'Molar', ("Al",)),
                ('Counter Ion Concentration', 'Molar', ("Na+", "Li+", "Cs+", "K+")),
                ('Counter Ion', ('Species',), ("Na+", "Li+", "Cs+", "K+",)),
                ('Base Concentration', 'Molar', ("OH-",)))
    y_groups = (('27 Al ppm', 'ppm', ("Al",)),)
    return x_groups, y_groups


@pytest.fixture
def raman_groups():
    x_groups = (('Total Aluminate Concentration', 'Molar', ("Al",)),
                ('Counter Ion Concentration', 'Molar', ("Na+", "Li+", "Cs+", "K+")),
                ('Counter Ion', ('Species',), ("Na+", "Li+", "Cs+", "K+",)),
                ('Base Concentration', 'Molar', ("OH-",)))
    y_groups = (('Integrated Raman Intensity', 'Integrated Intensity', ("Al",)),)
    return x_groups, y_groups
