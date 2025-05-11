from flask import Flask, request, jsonify, send_file
import requests
import base64

app = Flask(__name__)

# === НАСТРОЙКИ ===
GITHUB_TOKEN = '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'  # Вставь сюда свой GitHub Personal Access Token
REPO = 'akvalongist/site-landing'
FILE_PATH = 'docs/index.html'
BRANCH = 'main'

@app.route('/openapi.json', methods=['GET'])
def openapi():
    return send_file('openapi.json')

def get_file_info():
    url = f'https://api.github.com/repos/{REPO}/contents/{FILE_PATH}'
    headers = {'Authorization': f'Bearer {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.json()

@app.route('/update', methods=['POST'])
def update_file():
    data = request.json
    new_content = data.get('content')
    commit_message = data.get('message', 'auto update via bot')

    file_info = get_file_info()
    sha = file_info.get('sha')

    if not sha:
        return jsonify({"error": "Не удалось получить SHA"}), 400

    content_encoded = base64.b64encode(new_content.encode()).decode()

    update_data = {
        "message": commit_message,
        "content": content_encoded,
        "branch": BRANCH,
        "sha": sha
    }

    url = f'https://api.github.com/repos/{REPO}/contents/{FILE_PATH}'
    headers = {'Authorization': f'Bearer {GITHUB_TOKEN}'}
    response = requests.put(url, headers=headers, json=update_data)

    if response.status_code in (200, 201):
        return jsonify({"status": "Файл обновлён"})
    else:
        return jsonify({"error": response.json()}), 500

if __name__ == '__main__':
    app.run(debug=True)
