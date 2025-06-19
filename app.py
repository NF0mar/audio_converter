from flask import Flask, request, send_file
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return 'Tacab Audio Converter is running!'

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return {'error': 'No file uploaded'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No file selected'}, 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    wav_filename = os.path.splitext(filename)[0] + '.wav'
    output_path = os.path.join(CONVERTED_FOLDER, wav_filename)

    try:
        subprocess.run(['ffmpeg', '-y', '-i', input_path, output_path], check=True)
        return send_file(output_path, as_attachment=True)
    except subprocess.CalledProcessError as e:
        return {'error': f'FFmpeg failed: {e}'}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
