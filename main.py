from flask import Flask, url_for, render_template, request
from PIL import Image
import easyocr
import os

app = Flask(__name__)

@app.route("/", methods=["get", "post"])
def home():
    if request.method == "POST":
        file = request.files["image"]

        if "png" in file.filename or "jpg" in file.filename:
            img = Image.open(file.stream)
            img = img.save("image.png")

        reader = easyocr.Reader(['fr', 'en'], gpu=True)  # this needs to run only once to load the model into memory
        result = reader.readtext("image.png")

        os.remove("image.png")

        calcul = result[0][1]

        if "x" in calcul:
            calcul = calcul.replace("x", "*")
        elif ":" in calcul:
            calcul = calcul.replace(":", "/")

        resultCalculations = eval(calcul)

        return render_template("result.html", result=resultCalculations)
    else:
        return render_template("home.html")