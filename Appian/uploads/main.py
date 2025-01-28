import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from pipeline_utils import process_document

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'documents'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    if file.filename.rsplit('.', 1)[1].lower() != 'pdf':
        return jsonify({"error": "Invalid file type"}), 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(file_path)
    result = process_document(file_path)
    return jsonify(result), 200

@app.route('/search', methods=['GET', 'POST'])
def search_document():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)