from flask import Flask, request, jsonify
import replicate
import os

app = Flask(__name__)

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
                "cjwbw/demucs",
                input={"audio": audio_file}
            )

        return jsonify({"result": output})

    except Exception as e:
        return jsonify({"error": str(e)})
