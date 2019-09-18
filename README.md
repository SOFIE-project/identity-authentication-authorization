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

#### Client
A web browser should be configured with the [metamsk](https://metamask.io) extension. The Client folder should be stored in a web server so it can be accessed over HTTP(s). 

#### Smart contracts
Smart contracts should be installed in an Ethereum network. 

#### IAA blockchain agent
IAA blockchain agent requires [node.js](https://nodejs.org/en/) and [npm](https://www.npmjs.com). The Agent folder should be stored in a location that can be accessed by node.js and npm, in an IP address that can be accessed by the uthorization server. The agent needs to be connected to an ethereum RPC server that supports the [web3.js - Ethereum JavaScript API](https://web3js.readthedocs.io/en/v1.2.1/). [Geth](https://geth.ethereum.org/install-and-build/Installing-Geth) is the recommended approach.  

#### Authorization server
The Authorization-server fodler should be stored in a web server that supports php, so it can be accessed over HTTP(s) (NOTE accessing the Authorization server is not secure).

### Configuration

#### Client
Edit the js/conf.js and update the following variables:
- contractAddress The address of the Authorization smart contract
- authServerURL The URL of the Authorization server

#### IAA blockchain agent
Edit the IAAgent.js file and update the following variables
- contractAddress The address of the Authorization smart contract
- authServerURL The URL of the Authorization server
- web3Provider The address of the Ethereum RPC server (geth)
- ethAccountAddr The address of the ehtereum account that the agent will use


#### Authorization server
Edit the index.php file and update the following variables
- IAAagent The address of the IAA blockchain agent

### Execution
The sub-components should be executed in the following order

#### IAA blockchain agent
The fist time this subcomponent is executed the appropriate dependencies should be downaloaded and installed. From the Agent folder executes

`npm install`

Before executing the agent the Ethereum RPC server should be up and running. We have found that invoking geth with the following paprametes produces the desired output.

`geth --networkid XXXX  --rpc --rpcaddr X.X.X.X --rpcport XXXX  --rpcapi="db,eth,net,personal,web3" --allow-insecure-unlock`

Make sure that the account that will be used by the Agent is unlocked (e.g., by executing `personal.unlockAccount(web3.eth.accounts[0], "PASSWORD",0)`)

Then the agent can be executed using node.js:

`node IAAagent.js`

#### Client
A web browser should be configured with the [metamsk](https://metamask.io) extension. The Client folder should be stored in a web server so it can be accessed over HTTP(s). 

#### Smart contracts
Smart contracts should be installed in an Ethereum network. 



#### Authorization server
The Authorization-server fodler should be stored in a web server that supports php, so it can be accessed over HTTP(s) (NOTE accessing the Authorization server is not secure).

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