# Flask app here in the future

from app import data_imports
from app import data_cleaning
from app import summary_stats   
from app import models
from app import visualisations
from app import relationship_detection
from flask import Flask, render_template, request
import os
from markupsafe import escape

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']

    if file.filename == '':
        return "No selected file"
    if file.filename.endswith('.csv') == False + file.filename.endswith('.xlsx') == False:
        return "Invalid file format. Only CSV and XLSX files are supported."

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    file.save(file_path) 

    df = data_imports.read_file(file_path)
    cleaner = data_cleaning.DataCleaner(df)
    cleaner.clean()
    return df.to_html()

if __name__ == '__main__':
    app.run(debug=True)