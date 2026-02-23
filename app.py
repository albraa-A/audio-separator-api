from flask import Flask, request, jsonify
import replicate
import os

app = Flask(__name__)

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

@app.route("/separate", methods=["POST"])
def separate():
    try:
        audio_url = request.json["audio_url"]

        client = replicate.Client(api_token=REPLICATE_API_TOKEN)

        output = client.run(
            "cjwbw/demucs",
            input={"audio": audio_url}
        )

        return jsonify({"result": output})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/")
def home():
    return "Audio Separator API is running ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
