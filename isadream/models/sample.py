
from . import utils


class Sample:

    def __init__(self, sample_df):
        self.df = sample_df.T

    @property
    def sources(self):
        return self.df.xs('sources')

    @property
    def species(self):
        return self.df.xs('species')

    @property
    def factors(self):
        return self.df.xs('studySampleFactors')