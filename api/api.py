from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import time
import uuid

from style_transfer.utils import Utils
from style_transfer.neural_style import StylizeImage

base_dir=os.path.dirname(os.path.abspath(__file__))
template_folder=os.path.join(base_dir, "templates")
static_folder=os.path.join(base_dir, "assets")
process_dir = os.path.join(base_dir,"p_dir")

app = Flask("vangogh", template_folder=template_folder, static_folder=static_folder)

models = Utils.load_models(os.path.join(base_dir, "../models"))
print models.keys()


def stylize_image(content_image, style_image, model, output_path):
    si = StylizeImage(style_image, content_image, models[model], scale=2, output=output_path, cuda = False)
    si.stylize()


@app.route('/assets/<path:path>')
def getStaticFile(path):
    return send_from_directory(static_folder,path, cache_timeout=0)



@app.route('/getStyleImgs', methods=['GET'])
def getStyleImgs():
    return jsonify(models.keys()), 200


@app.route("/ping", methods=['GET'])
def ping():
    return jsonify({
        'message': 'pong'
    }), 200


def getStyleFile(key):
    return os.path.join(static_folder, "style_images", "{}.jpg".format(key))

@app.route("/generate", methods=['POST', 'GET'])
def generateArt():
    style_file_params = request.args.get("stylefile")

    if request.method == 'GET':
        return render_template("upload.html")


    style_file = request.files['style_file'] if style_file_params == None else None
    content_file = request.files['content_file']

    style_filename = secure_filename(style_file.filename) if style_file_params == None else style_file_params+".jpg"

    print "style_filename"
    print style_filename

    content_filename = secure_filename(content_file.filename)

    style_file.save(os.path.join(process_dir, "style_image.jpg")) if style_file_params == None else None
    content_file.save(os.path.join(process_dir, "content_image.jpg"))
    model = style_filename[:-4]

    uid = uuid.uuid4()
    output_path = os.path.join(static_folder, "stylized_{}.jpg".format(uid))
    content_img = os.path.join(process_dir,"content_image.jpg")
    style_img = os.path.join(process_dir,"style_image.jpg") if style_file_params == None else getStyleFile(style_file_params)
    stylize_image(content_img, style_img, model,output_path)


    return jsonify({'image': "/assets/stylized_{}.jpg".format(uid)}), 200

app.run(host='0.0.0.0',port=5000)