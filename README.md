# FinTech Capstone Project - NFT Creator by *Team Ripples*

## Summary

	Over the last few years, two groundbreaking concepts have emerged as pinnacles of innovation. Non-Fungible Tokens, or NFTs have taken the world by storm, revolutionizing ownership and authenticity in the digital space. These unique cryptographic tokens, built on blockchain technology allow for the creation of one-of-a-kind verifiable digital assets. Simultaneously, humans are just scraping the surface of what’s possible with Artificial Intelligence, or AI. Machine learning algorithms, natural language processing, and other forms of Artificial Intelligence have the opportunity to transform industries in years to come. This project serves to marry the two concepts into one cohesive use case. 
 
 We’ve created a platform where users can effortlessly generate tokens of personalized artwork. By simply typing in their preferences, users can harness the power of Artificial Intelligence to craft and mint distinct NFT images on the blockchain. To do this, we created a  smart contact using a mixture of Python and Solidity, while utilizing Streamlit as the user’s frontend interface. 
 
 The marrying of NFTs and AI within our platform represents the forward thinking application of these concepts in fintech. Both concepts have already begun to disturb the industry. As time goes on we’ll continue to see the convergence of NFTs and AI in FinTech. 
	

## Technologies

[Libraries, APIs, Languages]
- Python3
- Solidity
- Web3: A decentralized and blockchain-based technology that enables secure, transparent and user-centric interactions
- Ganache: Personal blockchain development environment
- MetaMask: Extension that serves as a cryptocurrency wallet and gateway, enabling users to interact with decentralized applications on the Ethereum blockchain
- Piñata Cloud: Cloud-based service that allows customizable access to the entire IPFS network
- [DeepAI AI Image Generator](https://deepai.org/machine-learning-model/text2img): AI powered tool that generates images based on user text input
- [Remix IDE](https://remix.ethereum.org): Web-based IDE designed for smart contract development on the Ethereum blockchain

## Libraries
Preloaded with Python: OS, Requests

- Web3
- PythonIO
- JSON
- Dotenv
- Pillow (PIL)
- Hashlib
- User Interface/Frontend: Streamlit
- Custom Libraries Used: Pinata & OpenZeppelin (ERC721Full)

## Application Capabilities

Smart Contracts
- `NFTCreator`: Ethereum smart contract that extends the ERC721 standard, allowing the creation and purchase of NFTs. It includes a `purchaseNFT` function for minting new tokens, associating them with metadata, and recording details such as image ID, purchase price, and image hash in a mapping called `nftCollection`.

APIs
- `makeNFT()`: Uses DeepAI’s Image Generator API to create an NFT based on the users input.
- `purchaseNFT()`: Allows a user to purchase the generated NFT using Ethereum. This API lives in the `NFTCreator` Solidity Smart Contract.

InterPlanetary File System (IPFS) protocol 
- Image Asset hosted on local github repository, accessible through generated URIs.

Trusted Data Encryption
- Digital NFT asset stored on localnet Blockchain for further heightened security of purchased goods using unique Transaction Hash using SHA256.

Payable & Transactable
- Wallet Addresses must be valid payable Ethereum wallets to purchase user / AI generated images; No purchase needed to generate "free" NFT artwork.

## Usage & Installation
*Requirements, running the application:*

This application is hosted locally through Streamlit (UI) and is based in Python3 and Solidity. In order to launch this application locally, you’ll need to follow the steps below.

## Prerequisites

Install [required libraries]()

```
pip install os requests web3 python-io json dotenv pillow hashlib streamlit
```
Download Ganache and set up a workspace 
Install Metamask and connect to your Ganache workspace
An `.env` with the following API keys
`DEEPAI` : key for DeepAI’s Image Generator
`WEB3_PROVIDER_URI`: Ganache RPC server address (generally https://127.0.0.1:7545)
`PINATA_API_KEY`
`PINATA_SECRET_API_KEY`

Preparing the Smart Contract
Import `AI_NFT.sol` into Remix IDE
Compile the contract using Solidity compiler version 0.5.5+
`Deploy` the contract with the following configurations
Environment: Injected Provider - MetaMask
Account: <Ganache account connected to MetaMask>
Gas Limit: 3000000
Contract: NFTCreator
	The deployed contract should look something like: 
![](screenshot of deployed contract)
Copy the deployed contract address and add it to your `.env` file using alias `SMART_CONTRACT_ADDRESS`

Running the Streamlit Application

Download/import `pinata.py` and `project_file.py` 
In the same directory as `project_file.py`, run the following command
```
Streamlit run ./project_file.py
```

The output will look like:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.5.3:8501
```

Access the UI using http://192.168.5.3:8501 or http://localhost:8501 to start generating and purchasing NFTs!



## Future Improvements Roadmap:

- Validity functionality to verify if a digital asset is indeed specific, verified artwork based on instance-generated Transaction Hash.
- Create a decentralized marketplace to view and purchase other AI / User generated NFTs stored on ‘mainnet’ Ethereum network.
- Provide a more robust, dynamic “Dashboard experience” on Streamlit that provides actual banking information.
- Integrate other Web3.0 social platforms and dApps like OpenSea.io, UniSwap, etc.
  
# COMING SOON!! - 11/29/23
