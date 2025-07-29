#!/usr/bin/env python3

"""This script handles operation for a Car website"""

import os
from dotenv import load_dotenv
from google import genai

# load env variable
load_dotenv()

def get_request(image_path, uploaded_url):
    """Get request to Gemini AI"""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    my_file = client.files.upload(file=image_path)

    user_message = (
        f"The uploaded image is available at this URL: {uploaded_url}. "
        "About this image: First, tell me if it's a car or not. "
        "If it is a car, return a JSON object with the following consistent structure: "
        "{ "
            "\"is_car\": true, "
            f"\"user_uploaded_image_url\": \"{uploaded_url}\", "
            "\"car_details\": { "
                "\"brand\": string, "
                "\"model\": string, "
                "\"approximate_year\": string, "
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
        "If the image is NOT a car, return this JSON object instead: "
        "{ "
            "\"is_car\": false, "
            f"\"user_uploaded_image_url\": \"{uploaded_url}\", "
            "\"image_url_info\": string (describe what the image shows or why it’s not a car) "
        "}. "
        "Important rules: "
        "- Always return the field `user_uploaded_image_url`. "
        "- Always use the exact field names and JSON structure shown above — no missing keys. "
        "- Only return the raw JSON object. No explanations. No preamble."
    )

    response = client.models.generate_content(
        model=os.getenv("GEMINI_AI_MODEL"),
        contents=[my_file, user_message]
    )
    return response.text

if __name__ == "__main__":
    get_request(image_path)
