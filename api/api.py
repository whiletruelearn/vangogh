from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import sys

from style_transfer.neural_style import StylizeImage

app = Flask("vangogh")

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
        return '''
                <html>
                    <form method=post enctype=multipart/form-data>
                        <input type="file" name="style_file" />
                        <input type="file" name="content_file" />
                        <input type="text" name ="model" />
                        <input type="submit" value="Submit"/>
                    </form>
                </html>
            '''

    print request.files
    style_file = request.files['style_file']
    content_file = request.files['content_file']
    model = request.text['model']
    style_filename = secure_filename(style_file.filename)
    content_filename = secure_filename(content_file.filename)
    style_file.save(os.path.join("/tmp/vangog", "style_image"))
    content_file.save(os.path.join("/tmp/vangog", "content_image"))

    stylize_image("content_image","style_image",model)
    return "ok"


app.run(port=5000)