from .species import Species
from .factor import Factor


class Source:
    '''
    '''

    def __init__(self, source_df):
        self.df = source_df

    @property
    def species(self):
        species = self.df.xs('species').to_dict('records')
        return [Species(data) for data in species]

    @property
    def factors(self):
        factors = self.df.xs('materialCharacteristic').to_dict('records')
        return [Factor(data) for data in factors]
