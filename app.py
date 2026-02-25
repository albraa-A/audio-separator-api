from flask import Flask, request, jsonify
from flask_cors import CORS
import replicate
import os

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

@app.route("/")
def home():
    return "Audio Separator API is running ✅"

@app.route("/separate", methods=["POST"])
def separate():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"})

        file = request.files["file"]

        # حفظ الملف مؤقتاً
        filepath = f"/tmp/{file.filename}"
        file.save(filepath)

        client = replicate.Client(api_token=REPLICATE_API_TOKEN)

        with open(filepath, "rb") as audio_file:
            output = client.run(
                "cjwbw/demucs:25a173108cff36ef9f80f854c162d01df9e6528be175794b81158fa03836d953",
                input={"audio": audio_file}
            )

        return jsonify({"result": output})

    except Exception as e:
        return jsonify({"error": str(e)})
