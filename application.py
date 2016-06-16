import os, sys, tempfile

import image_to_midi as im
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/temp_files/uploads"
DOWNLOAD_FOLDER = "static/temp_files/downloads"
ALLOWED_EXTENSIONS = set(["bmp"])




application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@application.route("/", methods=['GET', 'POST'])
def index():
	print request.files, request.method
	if request.method == 'POST':
		# check if the post request has the file part
	    print 'yay'
	    if 'bmp' not in request.files:
	        # flash('No file part')
	        print 'nope'
	        return redirect(request.url)
	    file = request.files['bmp']
	    print file.filename
	    # if user does not select file, browser also
	    # submit a empty part without filename
	    if file.filename == '':
	        # flash('No selected file')
	        print 'no'
	        return redirect(request.url)
	    if file and allowed_file(file.filename):
	    	print 'yay'
	        filename = secure_filename(file.filename)
	        file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
	        return redirect(url_for('generate', filename=filename))
	return render_template('index.html')

@application.route("/generate/<filename>")
def generate(filename):
	tf = tempfile.NamedTemporaryFile(delete=False)
	out_name = tf.name.split('\\')[-1] + '.mid'
	out_path = os.path.join(application.config['DOWNLOAD_FOLDER'], out_name)
	in_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
	im.make_MIDI(in_path, out_path)

	return redirect(url_for('play', filename=out_name))

@application.route("/play/<filename>")
def play(filename):
	filepath = 'temp_files/downloads/' + filename 
	return render_template('play.html', filepath=filepath)

if __name__=="__main__":
	application.run()

