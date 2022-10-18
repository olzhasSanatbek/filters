from flask import Flask, render_template, send_from_directory, url_for, request
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
import os
from Filters import Filters
import cv2


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
UPLOADED_PHOTOS_DEST = 'uploads'
DOWNLOAD_FOLDER = 'filtering'

app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOADED_PHOTOS_DEST'] = UPLOADED_PHOTOS_DEST
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

photos = UploadSet('photos', IMAGES)

configure_uploads( app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators = [
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )

class FilteringForm(FlaskForm):
    submit = SubmitField('Filtering')

@app.route('/filtering/<filename>')
def get_filtering_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

def filtering(checkbox, filename):
        PATH = os.path.join(UPLOADED_PHOTOS_DEST, filename)
        match checkbox:
            case 'Box Filter':
                filtering = Filters.box_filter(PATH)
            case 'Bilateral Filter':
                filtering = Filters.bilateral_filter(PATH)
            case 'Median Blur Filter':
                filtering = Filters.median_blur_filter(PATH)
            case 'Laplacian Derivatives':
                filtering = Filters.laplacian(PATH)
        
        cv2.imwrite(os.path.join(DOWNLOAD_FOLDER, filename), filtering)

@app.route('/', methods = ['GET', 'POST'])
def upload_img():
    upload_form = UploadForm()
    filtering_form = FilteringForm()
    
    if filtering_form.validate_on_submit():
        filename = photos.save(upload_form.photo.data)
        filtering(request.form.get('filters'), filename)
        filtering_file_url = url_for('get_filtering_file', filename=filename)
    else:
        filtering_file_url = None
    return render_template('index.html', upload_form = upload_form, 
                                        filtering_form = filtering_form,
                                        filtering_file_url = filtering_file_url)


if __name__ == '__main__':
   app.run(debug=True)