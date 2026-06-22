from flask import Flask,jsonify,request,send_from_directory

import os

STORAGE_FOLDER = 'storage'
os.makedirs('storage', exist_ok=True)

app = Flask(__name__)

@app.route('/')
def home():
    return "Cloud Storage Explorer"

@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file.save(os.path.join('storage', file.filename))

    return jsonify({'message': 'File uploaded successfully',
                    'filename' : file.filename})

@app.route('/files',methods=['GET'])
def listfiles():
    files=os.listdir(STORAGE_FOLDER)
    return jsonify ({'files' : files})

@app.route('/download/<filename>',methods=['GET'])
def download_file(filename):
    return send_from_directory(STORAGE_FOLDER,filename,as_attachment=True)

@app.route('/delete/<filename>',methods=['DELETE'])
def delete_file(filename):
    file_path=os.path.join(STORAGE_FOLDER,filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'})

    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True,port=5003)               