'''Atomic Classes of the package.

These are classes which do not inherit from any other class.

'''

class Factor:

    def __init__(self, input_dict):
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

    def __str__(self):
        return (
            f'Factor Type:   {self._factor_type}\n'
            f'Float Value:   {self._decimal_value}\n'
            f'String Value:  {self._string_value}\n'
            f'Ref Value:     {self._ref_value}\n'
            f'Unit:          {self._unit_ref}\n'
            f'CSV Index:     {self._csv_column_index}\n'
        )


class NodeInfo:

    def __init__(self, input_dict):
        self._input_dict = input_dict

    def __str__(self):
        return str(self._input_dict)


class Species:

    def __init__(self, input_dict):
        self._input_dict = input_dict

    def __str__(self):
        return str(self._input_dict)


class Comment:

    def __init__(self, input_dict):
        self._input_dict = input_dict

    def __str__(self):
        return str(self._input_dict)
