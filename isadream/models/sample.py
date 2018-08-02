

import pandas as pd


from . import utils

from .factor import Factor
from .species import Species
from .source import Source


class Sample:

    def __init__(self, sample_df):
        self.sample_df = sample_df

    def __str__(self):
        return str(self.sample_df)

    # @property
    # def sources(self):
    #     sources = self.sample_df.xs('sources').to_dict('records')
    #     return [Source(data) for data in sources]

    @property
    def species(self):
        species = self.sample_df.xs('species').to_dict('records')
        print(species)
        return [Species(data) for data in species]

    @property
    def factors(self):
        factors = self.sample_df.xs('studySampleFactors').to_dict('records')
        return [Factor(data) for data in factors]
