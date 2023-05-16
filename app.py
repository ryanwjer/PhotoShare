import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/ryan/photosapp/photos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mkv', 'mov', 'webm'}

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 16 MB upload limit
app.secret_key = 'jD4b!9$Fm@3dP&7hR*1uYw'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Allowed file types are png, jpg, jpeg, gif')
                return redirect(request.url)

        return redirect(url_for('upload_success'))

    return render_template('index.html')

@app.route('/success')
def upload_success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
