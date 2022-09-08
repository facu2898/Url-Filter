import os
from flask import Flask, flash, request, redirect, url_for,send_from_directory, after_this_request,render_template
from werkzeug.utils import secure_filename
from functions import process_urls, urls_to_dict

UPLOAD_FOLDER = 'resources'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/', methods=['GET', 'POST'])
def upload_file():
    url_filename = ""
    products_filename = ""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'urls' not in request.files or 'products' not in request.files:
            flash('No file part')
            return redirect(request.url)
        urls = request.files['urls']
        products = request.files['products']
        tolerance = int(request.form["tolerance"])

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if urls.filename == '' or products.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if urls and allowed_file(urls.filename) and products and allowed_file(products.filename):
            url_filename = secure_filename(urls.filename)
            products_filename = secure_filename(products.filename)
            urls.save(os.path.join(app.config['UPLOAD_FOLDER'], url_filename))
            products.save(os.path.join(app.config['UPLOAD_FOLDER'], products_filename))
            process_urls(url_filename, products_filename, tolerance)
            # Appending app path to upload folder path within app root folder
            uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
            # Returning file from appended path

            return send_from_directory(directory=uploads, path=url_filename)
    return render_template("index.html")


if __name__ == "__main__":
    app.run()

