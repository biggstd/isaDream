'''

'''

class Factor:
    '''
    '''

    def __init__(self, factor_df):
        '''

        Each factor is made up of five possible fields:
            1. unitRef
            2. factorType
            3. decimalValue
            4. csvColumnIndex
            5. stringValue

        '''

        # Try to get the five possible values.
        self.__unitRef = factor_df.get('unitRef')
        self.__factorType = factor_df.get('factorType')
        self.__csvColumnIndex = factor_df.get('csvColumnIndex')
        self.__decimalValue = factor_df.get('decimalValue')
        self.__stringValue = factor_df.get('stringValue')

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
        if self.__stringValue:
            return self.__stringValue
        elif self.__decimalValue:
            return self.__decimalValue

    @property
    def factor_type(self):
        '''
        '''
        return self.__csvColumnIndex
