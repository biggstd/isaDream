"""Groups are simple Tuple constructs that are used to collate data.

"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import param  # Boiler-plate for controlled class attributes.
from typing import Tuple, Callable, Union


QueryGroupType = Tuple[str, Tuple[str, ...], Tuple[str, ...]]
DerivedGroupType = Tuple[str, Tuple[str, ...], Callable]
GroupTypes = Union[QueryGroupType, DerivedGroupType]


class QueryGroup(param.Parameterized):
    """A QueryGroup constructs a column for a data set based on Factor and
    SpeciesFactor entries.

    Generally, a query group has the following form:
        Tuple[str, Tuple[str, ...], Tuple[str, ...]]

    ***Note***: This helper class has no function other than ensuring
    query groups are properly formatted. Use of this class is not
    required.

    """

    column_name = param.String(allow_None=False)
    factor_filter = param.Tuple(allow_None=False)
    species_filter = param.Tuple(allow_None=False)

    @property
    def group(self) -> QueryGroupType:
        return self.column_name, self.factor_filter, self.species_filter


class DerivedGroup(param.Parameterized):
    """A DerivedGroup constructs a column based on existing columns.

    """

    column_name = param.String(allow_None=False)
    source_names = param.Tuple(allow_None=False)
    callable_ = param.Callable(allow_None=False)

    @property
    def group(self) -> DerivedGroupType:
        return self.column_name, self.source_names, self.callable_
