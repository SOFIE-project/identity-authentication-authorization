pragma solidity ^0.5.0;

import "./ERC721Token.sol";

contract ERC721Metadata is ERC721Token {

    string internal tokenName;
    string internal tokenSymbol;
    address private contractOwner;

    //mapping from token id to metadata uri
    mapping (uint256 => string) internal idToUri;

    constructor (string memory name, string memory symbol) public {
        tokenName = name;
        tokenSymbol = symbol;
        contractOwner = msg.sender;
        supportedInterfaces[0x5b5e139f] = true; //ERC721Metadata Interface
    }

    function getName() external view returns (string memory) {
       return tokenName;
    }

    function getSymbol() external view returns (string memory ) {
        return tokenSymbol;
    }

    function setTokenUri (uint256 _tokenId, string memory _uri) internal validToken(_tokenId) {
        idToUri[_tokenId] = _uri;
    }

    function getTokenURI(uint256 _tokenId) external view validToken(_tokenId) returns (string memory) {
        return idToUri[_tokenId];
    }

    function burn (uint256 _tokenId) internal {
        super.burn(_tokenId);
        if (bytes(idToUri[_tokenId]).length !=0) {
            delete idToUri[_tokenId];
        }
    }
	
	function burn1 (uint256 _tokenId) external {
        require(msg.sender == contractOwner);
        burn(_tokenId);
    }
    
    function mint (address _to, uint256 _tokenId, string memory uri) public  {
        require(msg.sender == contractOwner);
        super.mint(_to, _tokenId);
        setTokenUri(_tokenId, uri);
    }
}
