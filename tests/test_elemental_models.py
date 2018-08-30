"""Tests

"""

# ----------------------------------------------------------------------------
# Imports for Testing
# ----------------------------------------------------------------------------

from isadream.models.elemental import Factor, SpeciesFactor, Comment
import pytest


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------

def test_factor_creation(factor_kwargs):
    for factor_kwargs in factor_kwargs:
        factor = Factor(**factor_kwargs)
        assert factor.factor_type == factor_kwargs["factor_type"]
        assert factor.label == (factor_kwargs["factor_type"],
                                factor_kwargs.get("reference_value", ""),
                                factor_kwargs.get("unit_reference"))


def test_species_factor_creation(species_factor_kwargs):
    for species_kwargs in species_factor_kwargs:
        species_factor = SpeciesFactor(**species_kwargs)
        assert species_factor.species_reference == species_kwargs["species_reference"]
        assert species_factor.stoichiometry == species_kwargs["stoichiometry"]
