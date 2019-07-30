from flask import Flask, flash, request, redirect, url_for, render_template, make_response
import os
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
import urllib.request

app = Flask(__name__)
app.secret_key = "khuta"

api = Api(app)

UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','BED'])


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class folderUpload(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),headers)
    def post(self):
        if 'fileList' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['fileList']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

class view(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),headers)

api.add_resource(folderUpload,"/")
api.add_resource(view, "/view")