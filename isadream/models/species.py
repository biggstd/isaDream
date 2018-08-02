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

        self._species_reference = species_dict.get('speciesReference')
        self._stoichiometry = species_dict.get('stoichiometry')

    @property
    def reference(self):
        '''
        '''
        return self._species_reference

    @property
    def stoichiometry(self):
        '''
        '''
        return self._stoichiometry
