'''


'''

# Data science imports.
import pandas as pd


from . import utils

from .factor import Factor
from .sample import Sample


class Assay:
    '''Model for an individual assay contained within a DrupalNode.

    There can be one or more Assay class instance per DrupalNode, depeding
    on how many datafiles are supplied by the user.

    An assay likely has it's own unique datafile, as well as csv column index
    references. It is also possible for csv column index references to be
    defined outside the assay-level metadata. ie. a common measurement can be
    specified once, while sample measurements must be more granuarly defined.


    '''

    def __init__(self, assay_data, samples, factors, comments):
        '''initialization for an Assay instance.

        '''
        self._assay_data = assay_data
        self._parent_samples = samples
        self._parent_factors = factors  # Not in the demo json!
        self._parent_comments = comments

        self.data_file = self._assay_data.get('dataFile')

    @property
    def sample_groups(self):
        '''
        '''
        _sample_groups = self._assay_data.copy()
        _sample_groups = _sample_groups.set_index('samples.name').T
        _sample_groups = utils.split_index(_sample_groups, 'index').T
        _sample_groups.columns = pd.MultiIndex.from_tuples(_sample_groups.columns)
        _sample_groups = _sample_groups.groupby(level=0)
        _sample_groups = [data for _, data in _sample_groups]

        return _sample_groups

    @property
    def factors(self):
        sample_factors = [s.factors for s in self.samples]
        factors = self._parent_factors + sample_factors
        return factors

    @property
    def samples(self):
        assay_samples = [data for _, data in self.sample_groups]
        assay_samples = [Sample(data) for data in assay_samples]
        assay_samples += self._parent_samples
        return assay_samples

    def __str__(self):
        return str(self.data_file)
