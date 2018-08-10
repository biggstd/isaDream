"""Elemental Classes of the package.

These are classes which do not inherit from any other class, and do not
combine with any other classes.

"""


class Factor:

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
        return (f'Factor Type:   {self._factor_type}\n'
                f'Float Value:   {self._decimal_value}\n'
                f'String Value:  {self._string_value}\n'
                f'Ref Value:     {self._ref_value}\n'
                f'Unit:          {self._unit_ref}\n'
                f'CSV Index:     {self._csv_column_index}\n')

    @property
    def is_csv_index(self):
        # We accept values of 0, so just check that the value is not None,
        # and that it can be cast to an integer.
        if self._csv_column_index is not None:
            try:
                int(self._csv_column_index)
                return True
            except ValueError:
                return False

    @property
    def csv_index(self):
        if self.is_csv_index:
            return int(self._csv_column_index)

    @property
    def dict_label(self):
        """Build the dictionary key label for this factor.

        """

        # if self._string_value and self._decimal_value:
        #     labels = list(filter(None, (self._factor_type, self._ref_value,
        #                                 self._unit_ref, self._string_value)))
        #
        # else:
        #     labels = list(filter(None, (self._factor_type, self._ref_value,
        #                                 self._unit_ref)))
        #
        # # Replace any spaces in these labels with underscores.
        # labels = [str(lab).replace(' ', '_') for lab in labels]
        # # return '_'.join(labels)
        # return tuple(labels)
        return self._factor_type, self._unit_ref

    @property
    def hash_str(self):
        return str(hash(self))

    @property
    def dict_value(self):
        """Build the values for this factor.

        The priority of return order is:
            1. decimal_value
            2. string_value
            3. ref_value

        """
        for item in (self._decimal_value, self._string_value, self._ref_value):
            if item is not None:
                return item

    @property
    def as_dict(self):
        if self.dict_value and self.dict_label:
            return {self.dict_label: self.dict_value}

    def query(self, query_terms):
        properties = (self._factor_type, self._decimal_value,
                      self._string_value, self._ref_value, self._unit_ref,
                      self._csv_column_index)
        if any(term in properties for term in query_terms):
            return True


class SpeciesFactor:

    def __init__(self, input_dict):
        self._input_dict = input_dict
        self._species_reference = input_dict.get('speciesReference')
        self._stoichiometry = input_dict.get('stoichiometry')

    def __repr__(self):
        """Create a human readable output for the print() function."""
        return (f'Species Reference:  {self._species_reference}\n'
                f'Stoichiometry:      {self._stoichiometry}')

    @property
    def dict_label(self):
        return self._species_reference

    @property
    def dict_value(self):
        return self._stoichiometry

    @property
    def as_dict(self):
        if self.dict_value and self.dict_label:
            return {self.dict_label: self.dict_value}

    def query(self, terms):
        properties = (self._species_reference, self._stoichiometry)
        if any(term in properties for term in terms):
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
