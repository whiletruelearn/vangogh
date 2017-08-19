from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import time

from style_transfer.utils import Utils
from style_transfer.neural_style import StylizeImage

base_dir=os.path.dirname(os.path.abspath(__file__))
template_folder=os.path.join(base_dir, "templates")
static_folder=os.path.join(base_dir, "assets")
process_dir = os.path.join(base_dir,"p_dir")

app = Flask("vangogh", template_folder=template_folder, static_folder=static_folder)

models = Utils.load_models("/home/ks/coding/vangogh/models")
print models.keys()


def stylize_image(content_image, style_image, model, output_path):
    si = StylizeImage(style_image, content_image, models[model], scale=2, output=output_path, cuda = False)
    si.stylize()


@app.route('/assets/<path:path>')
def getStaticFile(path):
    return send_from_directory(static_folder,path, cache_timeout=0)


@app.route("/ping", methods=['GET'])
def ping():
    return jsonify({
        'message': 'pong'
    }), 200


@app.route("/generate", methods=['POST', 'GET'])
def generateArt():
    if request.method == 'GET':
        return render_template("upload.html")

    print request.files
    style_file = request.files['style_file']
    content_file = request.files['content_file']

    style_filename = secure_filename("style_image.jpg")
    content_filename = secure_filename("content_image.jpg")
    style_file.save(os.path.join("/tmp/vangogh", style_filename))
    content_file.save(os.path.join("/tmp/vangogh", content_filename))
    model = style_filename[:-4]

    print model
    output_path = os.path.join(static_folder, "stylized_{}.jpg".format(model))
    stylize_image(os.path.join(process_dir,"content_image.jpg"),
                  os.path.join(process_dir,"style_image.jpg"),
                  model,output_path)


    return jsonify({'image': "/assets/stylized_{}.jpg".format(model)}), 200

app.run(host='0.0.0.0',port=5000)