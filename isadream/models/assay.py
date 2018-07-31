'''


'''


class Assay:
    '''Model for an individual assay contained within a DrupalNode.

    There can be one or more Assay class instance per DrupalNode, depeding
    on how many datafiles are supplied by the user.

    An assay likely has it's own unique datafile, as well as csv column index
    references. It is also possible for csv column index references to be
    defined outside the assay-level metadata. ie. a common measurement can be
    specified once, while sample measurements must be more granuarly defined.

    + View classes are based on the data contained within a set of Assays.

    In addition to the assays own set of metadata, there are four other basic
    sets of data that need to be incorporated.

    '''

    def __init__(self, assay_df, metadata):
        '''initialization for an Assay instance.

        Args:
            assay_df: A pd.DataFrame with the data unique to this instance.
            metadata: A list of four pd.Dataframe objects. This is metadata
                from the parent object.

        '''
        self.__assay_df = assay_df
        self.__drupal_node_metadata_frame = metadata

    @property
    def factors(self):
        '''All the factors, including parental, of this node.

        Each factor is made up of five possible fields:
            1. unitRef
            2. factorType
            3. decimalValue
            4. csvColumnIndex
            5. stringValue

        The `csvColumnIndex` factor is a special type. All others are one-
        dimensional values.

        The `csvColumnIndex` factor indicates that the factor described has
        its values within the .csv file associated with this Assay (or its
        parent DrupalNode object.)
        '''
        pass

    # @property
    # def metadata(self):
    #     '''Contains the merged Assay and Drupal metadata information, as well
    #     as the data loaded from the associated `.csv` file.
    #
    #     '''
    #     pass
