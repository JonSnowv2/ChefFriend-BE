from flask import request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
from config import db, app

from models.image import Img

@app.route('/api/upload_pic')
@cross_origin(origin="*")
def upload():
    pic = request.files['pic']

    if not pic:
        return 'No pic uploaded', 400
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype

    img = Img(img=pic.read(), mimetype=mimetype, name=filename)

    db.session.add(img)
    db.session.commit()

    return 'Image has been uploaded', 200

@app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()

    if not img:
        return 'Image not found', 404
    
    respone = {'image': img, 'mimetype': img.mimetype}
    return jsonify(respone), 200

