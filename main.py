#!/usr/bin/env python3

"""This script handles operation for a Car website"""

import os
from dotenv import load_dotenv
from google import genai


# load env variable
load_dotenv()

# take an image path
image_path="/home/bode-murairi/Desktop/LEAD.jpg"


# setup gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

my_file = client.files.upload(file=image_path)

message = "Can you describe this car on the image?"

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[my_file, message]
)

print(response.text)
