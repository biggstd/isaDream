# ISADREAM

[![Build Status](https://travis-ci.org/biggstd/isadream.svg?branch=master)](https://travis-ci.org/biggstd/isadream)

_This package is under active development._

ISADream is a python package that handles:
* Ontology sources for the IDREAM project.
* Generation of ISA metadata documents and their:
	* Conversion to and from `*.json` files to ISA document objects.
	* Associated data files and their conversion to Pandas dataframes.

These features allow for ISADream to provide data frames where each point
has been tagged with metadata identifiers. These metadata identifiers can
then be used to either further populate the dataframe with desirable factors,
or as keys to access the entirety of metadata associated with a given
data point.


## TODO



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

```bash
docker build -t isadream .
```


### To run the container off of docker hub
- docker run -p 0.0.0.1:8001:5006 -v /data/dir/on/host:/opt/isadream/data -t -d --name isadream tylerbiggs/idreamvis:VERSION
- Test that it is running by visiting http://localhost:8001 in your browser


### Open a bash shell into the container

```bash
docker exec -it isadream bash
```


### Stop and delete the container

```bash
docker stop isadream && docker rm isadream
```

```bash
docker run -p 0.0.0.1:8123:5006 -v /home/bigg006/public_html/idreamdrupal/sites/default/files/vizdata:/opt/isadream/data -t -d --name isadream tylerbiggs/idreamvis:45
```
