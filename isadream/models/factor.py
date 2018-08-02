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
        self.__refValue = factor_dict.get('RefValue')
        self.__csvColumnIndex = factor_dict.get('csvColumnIndex')
        self.__decimalValue = factor_dict.get('decimalValue')
        self.__stringValue = factor_dict.get('stringValue')

    @classmethod
    def from_dataframe(cls, dataframe):
        '''Extract and build Factors from a pandas dataframe.

        '''
        factor_labels = '''
            studyFactors
            studySampleFactors
            materialCharacteristic
            studySampleFactors
            AssaySampleFactors
        '''.split()



        return

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
        if self.__decimalValue:
            return self.__decimalValue
        return self.__stringValue

    @property
    def factor_type(self):
        '''
        '''
        return self.__factorType

    def __str__(self):
        '''Display something usefull when a print() call is used.
        '''
        return f'{self.factor_type}:\n{self.value}: {self.unit}'
