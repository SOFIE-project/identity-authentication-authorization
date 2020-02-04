# Identity, Authentication and Authorization Component
## Description

The goal of the Identity, Authentication and Authorization (IAA) component is to provide mechanisms that can be used for identifying communicating endpoints, as well as for authenticating and authorising users wishing to access a protected resource. 

In its present form, the IAA component can authenticate users using username/passwords, or Decentralised Identifiers (DIDs) and it uses the OAuth 2.0 protocol for user Authorization. The user Authorization process is enhanced by a smart contract that provides conditional release of an access token (e.g. when a user performs a payment)

### Architecture Overview


A high-level view of how the system is structured, including visual assets (e.g., images).

In particular, this section should also contain class/sequence diagrams along with the description of the different sub-components involved.

The IAA component is composed of 5 sub-scomponents: Client, Smart contracts, IAA blockchain agent, Authorization Server, and IoT platform.

#### Client
This this sub-component includes libraries that can be used by an external client application in order to access a platform using the IAA component. 

#### Smart contracts
The IAA component includes two smart contracts, one for handling DIDs, and another that implements the functionality required by OAuth2-based Authorization using blockchains.

#### IAA blockchain agent
This entity is responsible for mediating the communication between the Authorization server (see next) and the smart contracts. It is responsible for translating smart contract events into the appropriate REST API calls to the Authorization server (see below), as well as for implementing a REST API that can be invoked by an Authorization server when it requires functionality provided by the smart contracts.

#### Authorization server
This entity is an enhanced version of the [OAuth2 php server](https://github.com/bshaffer/oauth2-server-php).

### IoT platform
A sample IoT platform used for testing pursposed. 


### Relation with SOFIE

Nore information about this compoment and its relation to the SOFIE project can be found in [D2.5 Federation Framework, SOFIE deliverable](https://media.voog.com/0000/0042/0957/files/SOFIE_D2.5-Federation_Framework%2C_2nd_version.pdf)


### Key Technologies

The following table includes the key technologies used for each sub-component

| Sub-component | Technologies |
| ------------- | ------------- |
| Client  | Metamask and compatible browser |
| Smart contracts  | Solidity  |
| IAA blockchain agent  | node.js  |
| Authorization server  | php compatilbe web server, OAuth2 |


## Usage


## Installation

### Prerequisites
Python 3, Hyperledger Indy SDK, and the python wrapper are required
* sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE7709D068DB5E88
* sudo add-apt-repository "deb https://repo.sovrin.org/sdk/deb bionic stable"
* sudo apt-get update
* sudo apt-get install -y libindy
* pip3 install install python3-indy


### Configuration
At this point no configuration is reqiured

### Execution
From the root directory run `python3 IAA/iaa.py`


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