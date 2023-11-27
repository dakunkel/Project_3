# Imports
import os
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()
import json
from web3 import Web3
from pathlib import Path
import streamlit as st
import hashlib

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

#Load API Key for Image Generator
ai_api_key = os.getenv("DEEPAI")

################################################################################
# Load_Contract Function
################################################################################
@st.cache_resource
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/ai_nft_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

# Load the contract
contract = load_contract()


# Hash Image for block
def hash_image(file_path):
    # Read the content of the image file in binary mode
    with open(file_path, 'rb') as file:
        image_content = file.read()
    # Calculate the SHA-256 hash
    sha256_hash = hashlib.sha256(image_content).hexdigest()
    return sha256_hash

# Make NFT
def make_nft(text_input_for_AI_call):

    # make a call to Image Generator using user input
    response = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': text_input_for_AI_call,
        'grid_size' : "1",
    },
    headers={'api-key': ai_api_key}
    )

    image_url = response.json()['output_url']
    image_name = save_nft(response)
    
    return image_name, image_url
    
# Save NFT to a specified file path
def save_nft(response):
    if response.status_code == 200:
        try:
            # Get the JSON data from the response
            response_json = response.json()

            # Check if the response contains a link to the image
            if 'output_url' in response_json:
                image_url = response_json['output_url']
                image_name = f"{response.json()['id']}.jpg"

                # Download the image from the URL
                image_response = requests.get(image_url)
                image_bytes = BytesIO(image_response.content)

                # Create a folder if it doesn't exist
                folder_path = "generated_images"
                os.makedirs(folder_path, exist_ok=True)

                # Open and save the image to the folder
                image = Image.open(image_bytes)
                image_path = os.path.join(folder_path, image_name)
                image.save(image_path)

                print(f"Image saved successfully at {image_path}")
                return image_name
            else:
                print("Error: The API response does not contain a link to the generated image.")
        except Exception as e:
            print(f"Error processing the API response: {e}")
    else:
            print(f"Error: {response.status_code} - {response.text}")

## Pin the file to IPFS
def pin_nft(imageID, image_url):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(image_url)

    # Build a token metadata file for the artwork
    token_json = {
        "name": imageID,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json

################################################
# Streamlit application headings
st.markdown("# Create your own NFT!")
st.markdown("### Generate an NFT with AI and claim as your own")
st.markdown("#### Each NFT costs 0.10 ETH")
st.markdown("Example prompt: Generate a captivating and vibrant digital artwork featuring a diverse array of birds in a lush, otherworldly aviary.")
st.text(" \n")

################################################
# Streamlit Sidebar Code - Start

st.sidebar.markdown("# Do you want to buy your NFT?")
st.sidebar.markdown("## Enter Your Account Address")
st.sidebar.markdown("Cost: :green[0.10] ETH")

# set purchase address as session var to prevent data from getting cleared
purchaseAddress = st.sidebar.text_input("Account Address")
st.session_state.purchaseAddress = purchaseAddress


################################################
text_input_for_AI_call = st.text_input("What do you want to see in your image?")
if st.button("Make me an NFT"):

    #Initiate Request for Image
    image_name, image_url = make_nft(text_input_for_AI_call)
    
    # Save as session var to prevent data from getting cleared
    if "image_name" not in st.session_state:
        st.session_state.image_name = image_name
    if "image_url" not in st.session_state:
        st.session_state.image_url = image_url

    # Display image to user
    st.write("Your NFT is now available:")
    st.image(f"generated_images/{image_name}", width=800)
    file_path = f"generated_images/{image_name}"
    
    image_hash = hash_image(file_path)
    if "image_hash" not in st.session_state:
        st.session_state.image_hash = image_hash 
    
    # Print image details
    st.write(f"The SHA-256 hash of the image is: {image_hash}")
    st.markdown(f"Image ID: {image_name}")
    st.markdown(f"Image Hash: {image_hash}")

################################################################################
# Purchase new NFT
################################################################################
if st.sidebar.button("Purchase"):
    
    # reload all session variables. only proceed if all are present
    if (st.session_state.image_name 
        and st.session_state.image_url 
        and st.session_state.image_hash
        and st.session_state.purchaseAddress):
        image_name = st.session_state.image_name
        image_url = st.session_state.image_url 
        image_hash = st.session_state.image_hash
        purchaseAddress = st.session_state.purchaseAddress   

        st.write(f"Your NFT was generated with ID: {image_name}")
        st.image(f"generated_images/{image_name}", width=800)

        # # Use the `pin_artwork` helper function to pin the file to IPFS
        nft_ipfs_hash, token_json = pin_nft(image_name, image_url)

        nft_uri = f"ipfs://{nft_ipfs_hash}"
        
        # execute transaction by engagin solidity
        tx_hash = contract.functions.purchaseNFT(
            purchaseAddress, 
            image_name, #imageID 
            100000000000000000, # purchasePrice 
            image_hash,
            nft_uri #tokenURI
        ).transact({"from": purchaseAddress, "gas": 3000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # show proof of transaction
        st.sidebar.write("Transaction receipt mined:")
        st.sidebar.write(dict(receipt))
        st.sidebar.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        st.sidebar.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{nft_ipfs_hash})")
        st.sidebar.markdown(f"[Artwork IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")
    else:
        st.write("You haven't made an NFT yet")

st.markdown("---")