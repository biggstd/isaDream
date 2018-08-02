

import pandas as pd


from . import utils

from .factor import Factor
from .species import Species
from .source import Source


class Sample:

    def __init__(self, sample_data):
        self.sample_data = sample_data
        # pd.DataFrame(sample_data)

    @property
    def sources(self):
        sources = self.sample_data.xs('sources').to_dict('sources')
        return [Source(data) for data in sources]
    #
    # @property
    # def species(self):
    #     species = self.df.xs('species').to_dict('records')
    #     return [Species(data) for data in species]
    #
    # @property
    # def factors(self):
    #     factors = self.df.xs('studySampleFactors').to_dict('records')
    #     return [Factor(data) for data in factors]
