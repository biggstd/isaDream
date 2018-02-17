# ISADREAM


[![Build Status](https://travis-ci.org/biggstd/isadream.svg?branch=master)](https://travis-ci.org/biggstd/isadream)

Python packages needed to run this demo:

+ bokeh
+ pandas
+ isatools

`pip install bokeh pandas isatools`


**isaDream** is a set of tools that extends [isaTools](https://github.com/ISA-tools/isa-api)
for use in the IDREAM EFRC.

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

- [x] Create hard coded demo dataset.
- [x] Develop Ontologies for NMR demo.
- [x] Create a Comment format that allows for column labeling of `.csv` files.
	  This should allow for defined ontologies to be linked to specific columns
	  in a data file.
- [x] Query ISA objects by design descriptor.
- [x] Query ISA objects by measurement type.
- [ ] Add a process to the NMR demo.
- [ ] Implement MongoDB.


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

## Run in Docker
### To build the image locally
- docker build -t isadream .

### To run the container off of docker hub
- docker run -p 127.0.0.1:8001:5006 -v /data/dir/on/host:/opt/isadream/data -t -d --name isadream tylerbiggs/isadreamvis:VERSION
- Test that it is running by visiting http://localhost:8001 in your browser

### Open a bash shell into the container
- docker exec -it isadream bash

### Stop and delete the container
- docker stop isadream && docker rm isadream
