# Identity, Authentication and Authorisation Component
## Description

The goal of the Identity, Authentication and Authorisation (IAA) component is to provide mechanisms that can be used for identifying communicating endpoints, as well as for authenticating and authorising users wishing to access a protected resource. 

In its present form, the IAA component can authenticate users using username/passwords, or Decentralised Identifiers (DIDs) and it uses the OAuth 2.0 protocol for user authorisation. The user authorisation process is enhanced by a smart contract that provides conditional release of an access token (e.g. when a user performs a payment)

### Architecture Overview


A high-level view of how the system is structured, including visual assets (e.g., images).

In particular, this section should also contain class/sequence diagrams along with the description of the different sub-components involved.

The IAA component is composed of 5 sub-scomponents: Client, Smart contracts, IAA blockchain agent, Authorisation Server, and IoT platform.

#### Client
This this sub-component includes libraries that can be used by an external client application in order to access a platform using the IAA component. 

#### Smart contracts
The IAA component includes two smart contracts, one for handling DIDs, and another that implements the functionality required by OAuth2-based authorisation using blockchains.

#### IAA blockchain agent
This entity is responsible for mediating the communication between the authorisation server (see next) and the smart contracts. It is responsible for translating smart contract events into the appropriate REST API calls to the authorisation server (see below), as well as for implementing a REST API that can be invoked by an authorisation server when it requires functionality provided by the smart contracts.

#### Authorisation server
This entity is an enhanced version of the [OAuth2 php server](https://github.com/bshaffer/oauth2-server-php).


### Relation with SOFIE

Nore information about this compoment and its relation to the SOFIE project can be found in [D2.5 Federation Framework, SOFIE deliverable](https://media.voog.com/0000/0042/0957/files/SOFIE_D2.5-Federation_Framework%2C_2nd_version.pdf)


### Key Technologies

The following table includes the key technologies used for each sub-component

| Sub-component | Technologies |
| ------------- | ------------- |
| Client  | Metamask and compatible browser |
| Smart contracts  | Solidity  |
| IAA blockchain agent  | node.js  |
| Authorisation server  | php compatilbe web server, OAuth2 |


## Usage

If the system offers several features, an example of API and how to use such features might be very insightful and helpful. Furthermore, a description of how the component in the example possibly interacts with other compents is needed. _Each feature would have its own sub-section in this section called with the name of the feature explained, and contains all the needed information in it._

## Installation

### Prerequisites

A list of all the dependencies needed in order to run the system, and how to fetch and install them.

### Configuration (OPTIONAL)

Instruct about any parameters/files that need to be modified (e.g., environment variables, paths) according to specific needs, before executing the environment. Any additional elements that need to be built before execution (e.g., containers, virtual environments, etc...) must be listed.

### Execution

An explanation about how to run the environment, what parameters can be used upon launch, and how such parameters affect the execution (e.g., development vs staging environment).

## Testing

### Prerequisites

A list of all the dependencies needed in order to run the test cases (e.g., a specific testing suite), and how to fetch and install them.

### Running the tests

Explain how to run any automated tests, and what such tests cover, in a high-level manner.

### Evaluating the results

Provide information about where the tests results are saved and in which format. Any additional information needed to properly evaluate the test results must be added.

## Integration

Describe any information that is needed in order to let the project pass through a CI tool. The section should contain information such as the format of the repository (e.g., git, svn, etc.), access control for the repository, i.e., whether it is publicly accessible or it needs to grant permissions to the CI agent (and in that case how such permissions can be obtained), and branches policy (which are the relevant branches, and which one is the designated to be listened to by the CI agent).

## Deployment

Describe what are the additional steps needed in order to deploy the artifact and execute it in production.

## Known/Open Issues

No known issues

## Contact info

Please contact Nikos Fotiou or Dimitris Dimopoulos (AUEB) in case of any questions.

***