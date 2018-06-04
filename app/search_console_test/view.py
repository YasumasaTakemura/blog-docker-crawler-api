from flask import Blueprint, render_template

app = Blueprint('test', __name__)


@app.route('/google50e8617c83703829.html', methods=['GET'])
def testing():
    return render_template('google50e8617c83703829.html')