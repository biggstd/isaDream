"""Elemental Classes of the package.

These are classes which do not inherit from any other class, and do not
combine (mixin) with any other classes.

"""

# ----------------------------------------------------------------------------
# Boilerplate
# ----------------------------------------------------------------------------

# Standard Python modules.
import re  # Regular expression functions.
import param  # Boiler-plate for controlled class attributes.
from textwrap import dedent  # Prevent indents from percolating to the user.

# Local project imports.
from isadream.models import utils


class Factor(param.Parameterized):
    """The factor is the fundamental storage model for an observation.

    It is designed in such a way that it should be able to store:
        + Floats / decimals
        + strings / references
        + units
        + Factor Category
        + user data reference

    This allows the factor to model / label data contained in user uploaded
    files, as well as 'single-valued' data (eg. experimental temperature).

    """

    factor_type = param.String(
        allow_None=False,
        doc=dedent("""\
        A factor type is the outermost ontology group.
        """)
    )

    decimal_value = param.Number(
        allow_None=True,
        doc=dedent("""\
        The decimal value of this factor.
        """)
    )

    string_value = param.String(
        allow_None=True,
        doc=dedent("""\
        The string value of this factor. This should be used only if no other
        value field will work for the data.
        """)
    )

    reference_value = param.String(
        allow_None=True,
        doc=dedent("""\
        A reference value of this factor. This should be used when The value of
        this factor has a discreet set of possible values.
        """)
    )

    unit_reference = param.String(
        allow_None=True,  # Some string or factor values may not have units.
        doc=dedent("""The unit that describes this factor.""")
    )

    csv_column_index = param.Integer(
        allow_None=True,
        doc=dedent("""\
        An integer reference that points to the column index of the data that this
        factor describes.
        """)
    )

    @property
    def label(self):
        """A label property. These three parameters are the categorical units or
        ontology term of this factor.

        """
        return self.factor_type, self.reference_value, self.unit_reference

    @property
    def is_csv_index(self):
        """A boolean property. True if this factor describes a datafile column,
        and False otherwise.

        """
        if self.csv_column_index is not None:
            return True
        return False

    @property
    def value(self):
        """Build the values for this factor.

        The priority of return order is:
            1. decimal_value
            2. string_value
            3. ref_value

        The first one of these that is present is returned.
        """

        for item in (self.decimal_value, self.string_value, self.reference_value):
            if item is not None:
                return item

    def query(self, query_terms):
        """Query this factors properties with a list of terms.

        :param query_terms:
        :return:

        """

        # Ensure the query is a list to avoid iterating over single strings.
        query_terms = utils.ensure_list(query_terms)

        # Make an tuple to handle the properties easily.
        properties = [val for _, val in self.get_param_values()]

        if any(re.match(term, str(prop))
               for term in query_terms
               for prop in properties):
            return True


class SpeciesFactor(param.Parameterized):
    """A species factor is a pair of values. A species and a stoichiometry coefficient.

    Such stoichiometry coefficients are only comparable within a single Sample or Source
    object.

    """

    species_reference = param.String(
        allow_None=False,
        doc=dedent("""\
        The species being referenced.
        """)
    )

    stoichiometry = param.Number(
        allow_None=False,
        default=1.0,
        doc=dedent("""\
        The coefficient corresponding to this species factor.
        """)
    )

    def query(self, query_term):
        """A boolean search function. Returns True if the query term
        is found, and False otherwise.

        """
        if re.match(query_term, self.species_reference):
            return True


class Comment(param.Parameterized):
    """A node comment model.

    """
    comment_title = param.String(
        allow_None=False,  # There must at least be a comment name.
        doc=dedent("""\
        The title of a comment.
        """)
    )

    body = param.String(
        allow_None=Factor,
        doc=dedent("""\
        The body text of a comment.
        """)
    )


class DataFile(param.Parameterized):
    """FUTURE: This class is not used or implemented.

    In the future it will may handle data file paths / objects.

    """
    pass
