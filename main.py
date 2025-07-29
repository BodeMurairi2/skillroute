#!/usr/bin/env python3

"""Main logic"""

import os
import re
import json
from flask import Flask, request, redirect, render_template, url_for, session
from flask_session import Session
from store_userphoto import upload_user_image
from get_car_info import get_request
from werkzeug.utils import secure_filename

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("temp_session", exist_ok=True)

# Initialize Flask app
app = Flask(__name__)

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.abspath("temp_session")
app.config['SESSION_PERMANENT'] = False

Session(app)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["car_photo"]
        if file:
            filename = secure_filename(file.filename)
            temp_path = os.path.join(UPLOAD_DIR, filename)
            file.save(temp_path)

            uploaded_image = upload_user_image(image_path=temp_path, file_name=filename)
            response_json = get_request(image_path=temp_path)

            session['response_json'] = response_json
            session['uploaded_image'] = uploaded_image

            os.remove(temp_path)

        return redirect(url_for('get_infos'))
    return render_template("index.html")


@app.route("/get-car-info/get-infos", methods=["GET"])
def get_infos():
    json_response = session.get('response_json', None)
    user_image = session.get('uploaded_image', None)

    data = json.loads(json_response) if json_response else {}
    is_car = data.get("is_car", False)

    if is_car:
        car_details = data.get("car_details", {})
        car_primary_info = {
            "car_name": car_details["brand"],
            "car_model": car_details["model"],
            "car_year": car_details["approximate_year"],
            "body_style": car_details["body_style"],
            "exterior_design": car_details["exterior_design"],
            "interior_design": car_details["interior_design"],
            "color": car_details["color"],
            "lights": car_details["lights"],
            "wheels": car_details["wheels"],
            "technology": car_details["technology"],
            "price": car_details["price_range"],
            "where_to_buy": re.findall(r'https?://[^\s,"]+|www\.[^\s,")]+', car_details["where_to_buy"]),
            "engine_type": car_details["engine_type"],
            "image_url": car_details["image_url_info"],
            "special_features_modifications": car_details["special_features_modifications"],
            "user_uploaded_image_url": user_image
        }
        car_features = car_details.get("car_features", [])
        car_safety_features = car_details.get("safety_features", [])
        car_performance_specs = car_details.get("performance_specifications", {})
        print(user_image)
    else:
        car_primary_info = {
            "image_url": data.get("image_url_info", ""),
            "message": "The uploaded image does not appear to be a car.",
            "user_uploaded_image_url": user_image
        }
        car_features = []
        car_safety_features = []
        car_performance_specs = {}

    return render_template(
        "try.html",
        is_car=is_car,
        car_primary_info=car_primary_info,
        car_features=car_features,
        car_safety_features=car_safety_features,
        car_performance_specs=car_performance_specs
    )

if __name__ == "__main__":
    app.run(debug=True, port=8000)
