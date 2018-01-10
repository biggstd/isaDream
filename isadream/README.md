# ISADREAM

_This package is under active development._

ISADream is a python package that handles:
* Ontology sources for the IDREAM project.
* Generation of ISA metadata documents and their:
	* Conversion to and from `*.json` files to ISA document objects.
	* Storage and retrieval from a MongoDB.
	* Associated data files and their conversion to Pandas dataframes.
* Queries to MongoDB based on Ontologies.

These features allow for ISADream to provide data frames where each point
has been tagged with metadata identifiers. These metadata identifiers can
then be used to either further populate the dataframe with desirable factors,
or as keys to access the entirety of metadata associated with a given
data point.


## TODO

- [ ] 
- [ ]  Implement MongoDB.


## Installation Instructions

Clone the isaDream repository.
```
git clone https://github.com/biggstd/isaDream
```

Navigate to the base directory and run a pip installation.
This should probably be done in a virtual environment.
```
pip install .
```
