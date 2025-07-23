#!/usr/bin/env python3

"""Main logic"""

import os
import shutil
from flask import Flask, request, redirect, render_template, url_for
from store_userphoto import upload_user_image
from get_car_info import get_request
from werkzeug.utils import secure_filename

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    """Home page"""
    if request.method == "POST":
        file = request.files["car_photo"]
        question_message = request.form.get("message")
        if file:
            # Save uploaded file temporarily
            filename = secure_filename(file.filename)
            temp_path = os.path.join(UPLOAD_DIR, filename)
            file.save(temp_path)

            # upload to R2 Cloudflare
            upload_user_image(image_path=temp_path, file_name=filename)

            # upload to gemini
            get_request(image_path=temp_path, userMessage=question_message)

            # remove temp folder
            shutil.rmtree(UPLOAD_DIR)

        return redirect(url_for('get_infos'))
    return render_template("index.html")

@app.route("/get-car-info/get-infos", methods=["GET"])
def get_infos():
    """get infos"""
    return render_template("carInfo.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
