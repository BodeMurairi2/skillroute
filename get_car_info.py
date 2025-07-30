#!/usr/bin/env python3

"""This script handles operation for a Car website"""

import os
from dotenv import load_dotenv
from google import genai

# load env variable
load_dotenv('auth.env')

def get_request(image_path):
    """Get request to Gemini AI"""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    my_file = client.files.upload(file=image_path)  # expects string path
    user_message = (
    "About this image: First, tell me if it's a car or not. "
    "If it is a car, return a JSON object with the following consistent structure: "
    "{ "
        "\"is_car\": true, "
        "\"car_details\": { "
            "\"brand\": string, "
            "\"model\": string, "
            "\"approximate_year\": string,"
            "\"body_style\": string, "
            "\"exterior_design\": string, "
            "\"interior_design\": string, "
            "\"color\": string, "
            "\"lights\": string, "
            "\"wheels\": string, "
            "\"technology\": string, "
            "\"price_range\": string, "
            "\"where_to_buy\": string (include a valid link if possible), "
            "\"car_features\": [string, string, ...], "
            "\"engine_type\": string, "
            "\"performance_specifications\": { "
                "\"horsepower\": string, "
                "\"torque\": string, "
                "\"0_60_mph\": string, "
                "\"top_speed\": string "
            "}, "
            "\"safety_features\": [string, string, ...], "
            "\"image_url_info\": string, "
            "\"special_features_modifications\": string "
        "} "
    "}. "
    "Include detailed and accurate values under each field. Use best realistic estimates if not fully visible. "
    "Do not include markdown formatting like ```json. "
    "Always return the exact same structure for all car images — no missing fields — so that I can reliably use it on my website. "
    "If the image is NOT a car, return this JSON object instead: "
    "{ "
        "\"is_car\": false, "
        "\"image_url_info\": string (explain why it’s not a car or what the image shows) "
    "}. "
    "Again, always return the exact same structure for non-car responses. "
    "Only return the raw JSON object — no explanation, no headers, no extra text."
)

    message = user_message

    response = client.models.generate_content(
        model=os.getenv("GEMINI_AI_MODEL"),
        contents=[my_file, message]
    )
    return response.text

if __name__ == "__main__":
    get_request(image_path)
