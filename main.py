import os

from flask import Flask, render_template, request, send_file, flash, redirect
from functions.pressure import create_json
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import json
import zlib
import hashlib

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'json'}


@app.route("/")
def index():
    md5_hash = calculate_md5()
    return render_template('main.html', md5_hash=md5_hash)

def calculate_md5():
    md5 = hashlib.md5()
    for root, dirs, files in os.walk(app.root_path):
        dirs[:] = [d for d in dirs if d not in "files"]
        for file in files:
            if file == '.env':
                continue
            with open(os.path.join(root, file), "rb") as f:
                md5.update(f.read())
    return md5.hexdigest()


@app.route("/files/<file>")
def getfile(file):
    return send_file('files/' + file + ".json", as_attachment=True)


@app.route("/pressure", methods=["GET"])
def pressure_get():
    return render_template("pressure.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/pressure_in", methods=["POST", 'GET'])
def pressure_in():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("files", filename))
            f = open(os.path.join("files", filename))
            data = json.load(f)
            json_object = json.dumps(data, indent=4)
            crc32_value = zlib.crc32(json_object.encode())
            if crc32_value != int(request.form.get("crc")):
                return render_template("pressure_in.html", error="wrong crc")
            data = json.loads(data)
            return render_template("pressure_in.html", values=data)
    return render_template("pressure_in.html")


@app.route("/pressure", methods=["POST"])
def pressure_create():
    values = {}
    values["status"] = request.form.get("observation_status")
    values["subject_id"] = request.form.get("subject_reference")
    values["subject_name"] = request.form.get("subject_display")
    values["efective_date"] = request.form.get("effective_date")
    values["issued_date"] = request.form.get("issued_date")
    values["performer_reference"] = request.form.get("performer_reference")
    values["performer_display"] = request.form.get("performer_display")
    values["value"] = request.form.get("value")
    values["interpretation_code"] = request.form.get("interpretation_code")
    values["interpretation_display"] = request.form.get("interpretation_display")
    values["text_field"] = request.form.get("text_field")
    json_string = create_json(values)
    json_object = json.dumps(json_string, indent=4)
    crc32_value = zlib.crc32(json_object.encode())
    filepath = "files/pressure.json"
    with open(filepath, "w") as outfile:
        outfile.write(json_object)
    return render_template("pressure.html", data="pressure", crc=crc32_value)


if __name__ == '__main__':
    load_dotenv()
    stored_md5_hash = os.getenv("MD5_HASH")
    current_md5_hash = calculate_md5()
    if current_md5_hash != stored_md5_hash:
        print("Chyba: MD5 hash se neshoduje!")
    else:
        app.run()
