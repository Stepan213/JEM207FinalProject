function browseFile() {
    document.getElementById('fileInput').click();
}

function updateFileName() {
    var filePath = document.getElementById('fileInput').value;
    document.getElementById('filePath').value = filePath;
}
function selectAllNumericalVariables() {
    var numericalVariables = document.getElementsByName('numerical_variables');
    for (var i = 0; i < numericalVariables.length; i++) {
        numericalVariables[i].checked = true;
    }
}

function toggleFields() {
    var searchMethod = document.getElementById('search_method');
    var cvLabel = document.getElementById('cv_label');
    var cvInput = document.getElementById('cv');
    var nIterLabel = document.getElementById('n_iter_label');
    var nIterInput = document.getElementById('n_iter');
    var hyperparamGridFields = document.getElementById('hyperparam_grid_fields');

    if (searchMethod.value === 'grid_search' || searchMethod.value === 'random_search' || searchMethod.value === 'bayesian_optimization') {
        hyperparamGridFields.style.display = 'block';
    } else {
        hyperparamGridFields.style.display = 'none';
    }

    if (searchMethod.value === 'none') {
        cvLabel.style.display = 'none';
        cvInput.style.display = 'none';
        nIterLabel.style.display = 'none';
        nIterInput.style.display = 'none';
    } else {
        cvLabel.style.display = 'block';
        cvInput.style.display = 'block';
        nIterLabel.style.display = 'block';
        nIterInput.style.display = 'block';
    }
    populateHyperparamGrid();
}
function populateHyperparamGrid() {
    var modelSelect = document.getElementById('model_type');
    var hyperparamGridTextarea = document.getElementById('hyperpar_grid');
    var selectedModel = modelSelect.value;
    var hyperparamOptions = getHyperparamOptions(selectedModel);

    hyperparamGridTextarea.value = JSON.stringify(hyperparamOptions, null, 4);
}

function getHyperparamOptions(model_type) {
    switch (model_type) {
        case 'linear_regression':
            return {
                'fit_intercept': [true, false],
                'normalize': [true, false],
                'copy_X': [true, false],
            };

        case 'lasso':
            return {
                'alpha': [0.001, 0.01, 0.1, 1.0],
                'fit_intercept': [true, false],
                'normalize': [true, false],
                'max_iter': [100, 200, 300, 400, 500],
                'tol': [1e-4, 1e-3, 1e-2, 1e-1],
            };

        case 'ridge':
            return {
                'alpha': [0.001, 0.01, 0.1, 1.0],
                'fit_intercept': [true, false],
                'normalize': [true, false],
                'copy_X': [true, false],
                'max_iter': [100, 200, 300, 400, 500],
                'tol': [1e-4, 1e-3, 1e-2, 1e-1],
                'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga'],
            };

        case 'random_forest':
            return {
                'n_estimators': [10, 50, 100, 200],
                'max_depth': [null, 10, 20, 30], 
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'bootstrap': [true, false],
                };

        default:
            return {};
    }
}
