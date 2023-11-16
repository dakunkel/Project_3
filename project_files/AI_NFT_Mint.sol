pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";

contract NFT is ERC20, ERC20Detailed {
    address payable owner;

    modifier onlyOwner {
        require(owner == msg.sender, "You are not allowed to mint!");
        _;
    }

    constructor(uint initialSupply) ERC20Detailed("MintedNFT", "NFT", 18) public {
        owner = msg.sender;
        _mint(owner, initialSupply);
    }

    function mint(address recipient, uint amount) public onlyOwner {
        _mint(recipient, amount);
    }

}