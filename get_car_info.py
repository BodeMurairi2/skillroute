#!/usr/bin/env python3

"""This script handles operation for a Car website"""

import os
from dotenv import load_dotenv
from google import genai

# load env variable
load_dotenv()

def get_request(image_path, userMessage):
    """Get request to Gemini AI"""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    my_file = client.files.upload(file=image_path)  # expects string path

    message = userMessage

    response = client.models.generate_content(
        model=os.getenv("GEMINI_AI_MODEL"),
        contents=[my_file, message]
    )
    return response.json()

if __name__ == "__main__":
    get_request(image_path, userMessage)
