'''

'''

class Factor:
    '''One of the Atomic models of isadream.
    '''

    def __init__(self, factor_dict):
        '''

        Each factor is made up of five possible fields:
            1. unitRef
            2. factorType
            3. decimalValue
            4. csvColumnIndex
            5. stringValue

        '''

        # Try to get the five possible values.
        self.__unitRef = factor_dict.get('unitRef')
        self.__factorType = factor_dict.get('factorType')
        self.__csvColumnIndex = factor_dict.get('csvColumnIndex')
        self.__decimalValue = factor_dict.get('decimalValue')
        self.__stringValue = factor_dict.get('stringValue')

    @property
    def unit(self):
        '''
        '''
        return self.__unitRef

    @property
    def csv_index(self):
        '''
        '''
        return self.__factorType

    @property
    def value(self):
        '''
        '''
        return self.__decimalValue, self.__stringValue

    @property
    def factor_type(self):
        '''
        '''
        return self.__csvColumnIndex
