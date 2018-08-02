'''

'''


class Species:
    '''
    '''

    def __init__(self, species_dict):
        '''Creation of a Species instance.

        Args:
            dataframe (list[pd.DataFrame]): A list of species dataframes from
                the parent DrupalNode instance.
        '''

        self.species_reference = species_dict.get('speciesReference')
        self.stoichiometry = species_dict.get('stoichiometry')

    @property
    def reference(self):
        '''
        '''
        return self.species_reference

    @property
    def stoichiometry(self):
        '''
        '''
        return self.stoichiometry
