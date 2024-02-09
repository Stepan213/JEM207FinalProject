# Flask app here in the future

from app import data_imports
from app import data_cleaning
from app import summary_stats   
from app import models
from app import visualisations
from flask import Flask, render_template, request,redirect, url_for
import os
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['df'] = None

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

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    file.save(file_path)

    app.config['df'] =  data_imports.read_file(file_path=file_path)

    return redirect(url_for('menu'))

@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/view_dataframe')
def view_dataframe():
    return render_template('view_dataframe.html',df=app.config['df'])

@app.route('/clean_dataframe', methods=['GET', 'POST'])
def clean_dataframe():
    return render_template('clean_dataframe.html')

@app.route('/clean_dataframeresult', methods=['GET', 'POST'])
def clean_dataframeresult():
    strategy = request.form['strategy']
    remove_dup = request.form['remove_duplicates']
    data_cleaner = data_cleaning.DataCleaner(app.config['df'])
    app.config['df'] = data_cleaner.na_handling(na_strategy=strategy)

    if remove_dup == 'yes':
        app.config['df'] = data_cleaner.remove_duplicates()
    
    return render_template('view_dataframe.html',df=app.config['df'])

@app.route('/summary_statistics')
def summary_statistics():
    return render_template('summary_statistics.html')

@app.route('/summary_statisticsresult')
def summary_statisticsresult():
    target_variable = request.form['variables']
    df = app.config['df']
    if target_variable == 'all':
        summary_stats.numeric_statistics(df)
        summary_stats.categorical_statistics(df)
    else:
        print(summary_stats.numeric_statistics(df))
        print(summary_stats.categorical_statistics(df))

    return render_template('summary_statisticsresult.html')

@app.route('/visualisation')
def visualisation():
    return render_template('visualisations.html')

@app.route('/regression')
def regression():
    return render_template('regression.html')

if __name__ == '__main__':
    app.run(debug=True)