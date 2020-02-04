# Identity, Authentication, and Authorization Component
## Description


### Architecture Overview



### Relation with SOFIE

Nore information about this compoment and its relation to the SOFIE project can be found in [D2.5 Federation Framework, SOFIE deliverable](https://media.voog.com/0000/0042/0957/files/SOFIE_D2.5-Federation_Framework%2C_2nd_version.pdf)


### Key Technologies



## Usage


## Installation

### Prerequisites
Python 3, Hyperledger Indy SDK, and the python wrapper are required. Use the following commands to install the prerequisites in Ubuntu 18.04 

* sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE7709D068DB5E88
* sudo add-apt-repository "deb https://repo.sovrin.org/sdk/deb bionic stable"
* sudo apt-get update
* sudo apt-get install -y libindy
* pip3 install install python3-indy


### Configuration
At this point no configuration is reqiured

### Execution
From the root directory run `python3 IAA/iaa.py`

### Usage
The executed script creates an HTTP server that listens for REST API calls at port 9000. The REST API of IAA component is documented in [https://app.swaggerhub.com/apis-docs/nikosft/SOFIE-PDS-IAA/1.0.0#/IAA/vertoken] Please select *schema* to see all available API parameters and their documentation.

## Testing

### Prerequisites

Tests are executed using pytest. To install it execute `pip3 install -U pytest` 

### Running the tests
From the root directory run `python3 -m pytest tests/`


## Integration

To be provided.

## Deployment

To be provided.

## Known/Open Issues

No known issues

## Contact info

Please contact Nikos Fotiou or Dimitris Dimopoulos (AUEB) in case of any questions.

***