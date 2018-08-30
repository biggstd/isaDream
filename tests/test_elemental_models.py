"""Tests

"""

# ----------------------------------------------------------------------------
# Imports for Testing
# ----------------------------------------------------------------------------

from isadream.models.elemental import Factor, SpeciesFactor, Comment


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------

def test_factor_creation(factor_kwargs):
    for kwargs in factor_kwargs:
        factor = Factor(**kwargs)
        assert factor.factor_type == kwargs["factor_type"]
        assert factor.label == (kwargs["factor_type"],
                                kwargs.get("reference_value", ""),
                                kwargs.get("unit_reference"))


def test_species_factor_creation(species_factor_kwargs):
    for kwargs in species_factor_kwargs:
        species_factor = SpeciesFactor(**kwargs)
        assert species_factor.species_reference == kwargs["species_reference"]
        assert species_factor.stoichiometry == kwargs["stoichiometry"]


def test_comment_creation(comment_kwargs):
    for kwargs in comment_kwargs:
        comment = Comment(**kwargs)
        assert comment.comment_title == kwargs["comment_title"]
        assert comment.body == kwargs["body"]
