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

# Define Functions
# ----------
# Make NFT Function
def make_nft(text_input_for_AI_call):
    response = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': text_input_for_AI_call,
        'grid_size' : "1",
    },
    headers={'api-key': ai_api_key}
    )
    image_name = save_nft(response)
    return image_name
    
# Save NFT Function
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



# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

#Load API Key
ai_api_key = os.getenv("DEEPAI")

################################################
# Streamlit application headings
st.markdown("# Create your own NFT!")
st.markdown("### Generate an NFT with AI and claim as your own")
st.markdown("#### Each NFT costs 0.10 ETH")
st.markdown("Example prompt: Generate a captivating and vibrant digital artwork featuring a diverse array of birds in a lush, otherworldly aviary. Envision a kaleidoscope of feathery hues, with meticulously detailed plumage showcasing a range of colors from iridescent blues and greens to warm sunset oranges. The scene is set against a surreal backdrop that seamlessly blends elements of nature and fantasy – imagine towering, ethereal trees with branches that intertwine to create natural perches for the birds, and cascading waterfalls that form crystal-clear pools reflecting the avian splendor. The birds themselves should vary in species, size, and pose, capturing moments of graceful flight, playful interaction, and serene repose. The play of light and shadow should add depth to the composition, creating a visually stunning and immersive experience that celebrates the beauty and diversity of our feathered friends.")
st.text(" \n")

################################################
# Streamlit Sidebar Code - Start

st.sidebar.markdown("# Do you want to buy your NFT?")
st.sidebar.markdown("## Enter Your Account Address")
st.sidebar.text_input("Account Address")
st.sidebar.markdown("Cost: :green[0.10] ETH")
st.sidebar.button("Purchase")

seller_address = ""
recipient_address = ""
cost = 100000000000000000

################################################
#Test Streamlit
text_input_for_AI_call = st.text_input("What do you want to see in your image?")
if st.button("Make me an NFT"):
    #Initiate Request for Image
    image_name = make_nft(text_input_for_AI_call)
    st.write("Your NFT is now available:")
    st.image(f"generated_images/{image_name}", width=800)
