import os
from flask import Blueprint, request, jsonify
import requests


ai_bp = Blueprint("ai", __name__)


@ai_bp.post("/generate-topics")
def generate_topics():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY not configured"}), 500

    url = (
        "https://generativelanguage.googleapis.com/v1/models/"
        "gemini-2.5-pro:generateContent?key=" + api_key
    )
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 6000,
        },
    }

    try:
        resp = requests.post(url, json=payload, timeout=60)
    except requests.RequestException as e:
        return jsonify({"error": "Upstream request failed", "details": str(e)}), 502

    if not resp.ok:
        try:
            err = resp.json()
        except ValueError:
            err = {"error": resp.text}
        return jsonify({"error": err.get("error", "Gemini API error")}), resp.status_code

    try:
        return jsonify(resp.json())
    except ValueError:
        return jsonify({"error": "Invalid JSON from Gemini"}), 502


