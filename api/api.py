from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import sys

from style_transfer.neural_style import StylizeImage

base_dir=os.path.dirname(os.path.abspath(__file__))
template_folder=os.path.join(base_dir, "templates")
static_folder=os.path.join(base_dir, "assets")
app = Flask("vangogh", template_folder=template_folder, static_folder=static_folder)

def stylize_image(content_image,style_image,model):
    si = StylizeImage(style_image, content_image, model, scale=3, output="stylized", cuda = False)
    si.style_image()



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
    model = request.text['model']
    style_filename = secure_filename(style_file.filename)
    content_filename = secure_filename(content_file.filename)
    style_file.save(os.path.join("/tmp/vangog", "style_image"))
    content_file.save(os.path.join("/tmp/vangog", "content_image"))

    stylize_image("content_image","style_image",model)
    return jsonify({}), 200


app.run(port=5000)