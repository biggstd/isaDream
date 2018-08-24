"""Elemental Classes of the package.

These are classes which do not inherit from any other class, and do not
combine (mixin) with any other classes.

"""

# Standard Python modules.
import re  # Regular expression functions.
import param  # Boiler-plate for controlled class attributes.
from textwrap import dedent  # Prevent indents from percolating to the user.


# Local project imports.
from .. import modelUtils


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

    decimal_value = param.Parameter()

    string_value = param.Parameter()

    reference_value = param.Parameter()

    unit_reference = param.Parameter()

    csv_column_index = param.Integer(allow_None=True)

    # label = param.Tuple(default=(factor_type, reference_value, unit_reference))

    @property
    def label(self):
        return (self.factor_type, self.reference_value, self.unit_reference)

    @property
    def is_csv_index(self):
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
        query_terms = modelUtils.ensure_list(query_terms)

        # Make an tuple to handle the properties easily.
        properties = [val for _, val in self.get_param_values()]

        if any(re.match(term, str(prop))
               for term in query_terms
               for prop in properties):
            return True


class SpeciesFactor(param.Parameterized):
    """

    """
    species_reference = param.Parameter(allow_None=False)
    stoichiometry = param.Parameter(allow_None=True)

    def query(self, query_term):
        if re.match(query_term, self.species_reference):
            return True


class NodeInfo(param.Parameterized):
    info = param.Parameter(allow_None=True)


class Comment(param.Parameterized):
    comment_name = param.String()
    body = param.String()


class DataFile(param.Parameterized):
    """

    """
    pass
