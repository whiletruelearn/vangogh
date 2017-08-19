from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import sys

from style_transfer.utils import Utils
from style_transfer.neural_style import StylizeImage

base_dir=os.path.dirname(os.path.abspath(__file__))
template_folder=os.path.join(base_dir, "templates")
static_folder=os.path.join(base_dir, "assets")
app = Flask("vangogh", template_folder=template_folder, static_folder=static_folder)

models = Utils.load_models("/home/ks/coding/vangogh/models")
print models.keys()
output_path = os.path.join(static_folder,"stylized.jpg")

def stylize_image(content_image, style_image, model):
    si = StylizeImage(style_image, content_image, models[model], scale=1, output=output_path, cuda = False)
    si.stylize()



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

    style_filename = secure_filename(style_file.filename)
    content_filename = secure_filename(content_file.filename)
    style_file.save(os.path.join("/tmp/vangogh", "style_image.jpg"))
    content_file.save(os.path.join("/tmp/vangogh", "content_image.jpg"))
    model = style_filename[:-4]



    stylize_image('/tmp/vangogh/content_image.jpg','/tmp/vangogh/style_image.jpg',model)
    return jsonify({'image': output_path}), 200


app.run(port=5000)