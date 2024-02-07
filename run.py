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
from werkzeug.utils import secure_filename

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

    #file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    #os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    df = data_imports.import_data(data_source="file", file_path=file_path)
 

    return redirect(url_for('menu'))
@app.route('/menu')
def menu():
    return render_template('menu.html')

# Add more routes for each menu option
@app.route('/view_dataframe')
def view_dataframe():
    return render_template('view_dataframe.html', df=data_processor_instance.get_dataframe())

@app.route('/clean_dataframe')
def clean_dataframe():
    cleaner = data_cleaning.DataCleaner(df)
    cleaned_df = data_cleaning.clean_data(data_processor_instance.get_dataframe())
    print(cleaner.get_log())
    return render_template('clean_dataframe.html', cleaned_df=cleaned_df)

@app.route('/view_statistics')
def view_statistics():
    stats = summary_stats.generate_summary_stats(data_processor_instance.get_dataframe())
    return render_template('view_statistics.html', stats=stats)

@app.route('/use_regression_models')
def use_regression_models():
    regression_model = models.train_regression_model(data_processor_instance.get_dataframe())
    return render_template('use_regression_models.html', regression_model=regression_model)

@app.route('/view_visualisations')
def view_visualisations():
    visualisations_data = visualisations.generate_visualisations(data_processor_instance.get_dataframe())
    return render_template('view_visualisations.html', visualisations_data=visualisations_data)

@app.route('/relationship_detection')
def relationship_detection_page():
    relationships = relationship_detection.detect_relationships(data_processor_instance.get_dataframe())
    return render_template('relationship_detection.html', relationships=relationships)


if __name__ == '__main__':
    app.run(debug=True)