# Flask app here in the future

from app import data_imports
from app import data_cleaning
from app import summary_stats   
from app import models
from app import visualisations
from flask import Flask, render_template, request,redirect, url_for
import os
import json
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
    n_stats = summary_stats.numeric_statistics(app.config['df'])
    return render_template('summary_statistics.html', n_statistics = n_stats)

@app.route('/visualisation')
def visualisation():
    return render_template('visualisations.html')

@app.route('/regression',methods=['GET','POST'])
def regression():
    return render_template('regression.html',df=app.config['df'])

@app.route('/run_regression', methods=['GET','POST'])
def run_regression():

    model_type = request.form['model_type']
    target = request.form['target_variable']
    features = request.form.getlist('features')
    hyperpar_grid = json.loads(request.form['hyperpar_grid'])
    cv = int(request.form['cv'])
    n_iter = int(request.form['n_iter'])
    test_size = float(request.form['test_size'])
    search_method = request.form['search_method']


    model = models.RegressionModel(model_type,hyperpar_grid=hyperpar_grid, cv=cv, n_iter=n_iter, random_state=42)
    model.split_data(app.config['df'], variables=features, target=target, test_size=test_size)
    model.train(search_method=search_method)

    mse = model.evaluate()

    return render_template('regression_results.html', mse=mse)
if __name__ == '__main__':
    app.run(debug=True)