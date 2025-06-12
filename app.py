from flask import Flask, request, jsonify
import io
import base64
from PIL import Image
from main import main 

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing 'query' in request"}), 400

    result = main(query)
    if "error" in result:
        return jsonify(result), 400

    chart = result.get("chart")
    if isinstance(chart, Image.Image):
        img_io = io.BytesIO()
        chart.save(img_io, format='PNG')
        img_io.seek(0)
        image_base64 = base64.b64encode(img_io.read()).decode('utf-8')
    else:
        image_base64 = None

    return jsonify({
        "analysis": result.get("analysis"),
        "news": result.get("news"),
        "image_base64": image_base64
    })

