from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=words_file>
        <input type=submit value=Upload>
        </form>
    """