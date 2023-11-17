pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract NFTCreator is ERC721Full {
    constructor() public ERC721Full("NFTToken", "NFT") {}
    struct NFT {
        string imageID;
        uint256 purchasePrice;
        string imageHash;
    }

    mapping(uint256 => NFT) public nftCollection;

    function purchaseNFT(
        address owner, 
        string memory imageID, 
        uint256 purchasePrice,
        string memory imageHash,
        string memory tokenURI
        ) public returns (uint256) {
            uint256 tokenId = totalSupply();

            _mint(owner, tokenId);
            _setTokenURI(tokenId, tokenURI);

            nftCollection[tokenId] = NFT(imageID, purchasePrice, imageHash);
            return tokenId;
        }
}