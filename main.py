from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

FILE_PATH = "data.txt"

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Отсутствует поле 'text'"}), 400
        text = data['text'].strip()
        if not text:
            return jsonify({"error": "Текст не может быть пустым"}), 400
        with open(FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"{text}\n")
        return jsonify({"status": "ok", "message": "Данные успешно сохранены"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data", methods=["GET"])
def get_data():
    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                content = f.read()
            if not content.strip():
                return jsonify({"status": "ok", "content": "Файл существует, но пуст"}), 200

            return jsonify({"status": "ok", "content": content}), 200
        else:
            return jsonify({"status": "ok", "content": "Файл data.txt ещё не создан"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    if not os.path.exists(FILE_PATH):
        open(FILE_PATH, "w", encoding="utf-8").close()
    app.run(host="127.0.0.1", port=5000)