"""Elemental Classes of the package.

These are classes which do not inherit from any other class, and do not
combine with any other classes.

"""

# Standard Python modules.
import re

# Local project imports.
from . import utils


class Factor:
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

    def __init__(self, input_dict):
        """
        Args:
            input_dict (dict): Assumed to be a valid isadream factor
                entry.

        """
        self._input_dict = input_dict

        # There are two general types of values, string and floats and
        # then reference(string) values.
        self._factor_type = input_dict.get('factorType')

        # There will usually only be one of a decimal or string value.
        self._decimal_value = input_dict.get('decimalValue')
        self._string_value = input_dict.get('stringValue')

        # Or there may be one reference value.
        self._ref_value = input_dict.get('RefValue')

        # There will almost always be a unit string.
        self._unit_ref = input_dict.get('unitRef')

        # Special case of the csv index.
        self._csv_column_index = input_dict.get('csvColumnIndex')

    def __repr__(self):
        """Displays more useful information if print() is called.

        """

        return (f'Factor Type: {self._factor_type}, '
                f'Float Value: {self._decimal_value}, '
                f'String Value:  {self._string_value}'
                f'Ref Value: {self._ref_value}, '
                f'Unit: {self._unit_ref}, '
                f'CSV Index: {self._csv_column_index}')

    @property
    def is_csv_index(self):
        """Boolean check to see if a csv index value is stored.

        """

        # We accept values of 0, so just check that the value is not None,
        # and that it can be cast to an integer.
        if self._csv_column_index is not None:
            if int(self._csv_column_index) >= 0:  # if 0: returns False.
                return True

        return False

    @property
    def csv_index(self):
        """Return the csv index as an integer string.

        (eg, "1", not "1.0")

        """

        if self.is_csv_index:
            return str(int(self._csv_column_index))

    @property
    def label(self):
        """Build the dictionary key label for this factor.

        """

        return tuple([self._factor_type, self._ref_value, self._unit_ref])

    @property
    def value(self):
        """Build the values for this factor.

        The priority of return order is:
            1. decimal_value
            2. string_value
            3. ref_value

        """

        for item in (self._decimal_value, self._string_value, self._ref_value):
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
        properties = (self._factor_type, self._decimal_value,
                      self._string_value, self._ref_value, self._unit_ref,
                      self._csv_column_index)

        # Return True if any of the properties match any of the given terms.
        # TODO: Change to use re.match() ?
        if any(term in properties for term in query_terms):
            return True


class SpeciesFactor:
    """

    """

    def __init__(self, input_dict):
        """

        :param input_dict:
        """
        self._input_dict = input_dict
        self._species_reference = input_dict.get('speciesReference')
        self._stoichiometry = input_dict.get('stoichiometry')

    def __repr__(self):
        """Displays more useful information if print() is called.

        """

        return f'{self._species_reference}: {self._stoichiometry}'

    @property
    def label(self):
        """

        :return:
        """
        return self._species_reference

    @property
    def value(self):
        return self._stoichiometry

    def query(self, query_terms):
        query_terms = utils.ensure_list(query_terms)

        if any(re.match(term, self._species_reference)
               for term in query_terms):
            return True


class NodeInfo:

    def __init__(self, node_info):
        """Set all key: value pairs to the info dictionary property."""
        self._node_dict = dict()

        if node_info is not None:
            for key, value in node_info.items():
                self._node_dict[key] = value

    def __repr__(self):
        return str(self.info)

    @property
    def info(self):
        if self._node_dict:
            return self._node_dict

    @info.setter
    def info(self, value):
        self._node_dict = value


class Comment:

    def __init__(self, input_dict):
        self._comment_name = input_dict.get('name')
        self._comment_body = input_dict.get('body')
        self._input_dict = input_dict

    def __repr__(self):
        return str(f'Comment: {self._comment_name}\n'
                   f'Body:    {self._comment_body}')

    @property
    def dict_label(self):
        return self._comment_name

    @property
    def dict_value(self):
        return self._comment_body

    @property
    def as_dict(self):
        if self.dict_value and self.dict_label:
            return {self.dict_label: self.dict_value}


class DataFile:
    """

    """
    pass
