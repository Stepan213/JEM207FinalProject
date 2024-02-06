function browseFile() {
    document.getElementById('fileInput').click();
}

function updateFileName() {
    var filePath = document.getElementById('fileInput').value;
    document.getElementById('filePath').value = filePath;
}
