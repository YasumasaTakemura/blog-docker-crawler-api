import logging
import os
import json
from flask import request, Blueprint, abort, jsonify
from app.store.store import Store

from app.broker.model import Topic
from app.consumer.model import Consumer

logger = logging.getLogger('DB_View')

app = Blueprint('topic', __name__, url_prefix=os.getenv('API_VERSION'))


@app.route('/', methods=['GET', 'POST'])
def working():
    try:
        print(request.json)
    except:
        print(json.loads(request.form))
    else:
        print(request.form)

    return 'working', 200


@app.route('/push', methods=['POST'])
def push():
    paths = request.form.getlist('path')
    logger.info(paths)
    topic = Topic('test')
    lines = topic.push(paths)
    try:
        return lines, 200
    except Exception as e:
        logger.error('could not push urls')
        abort(400, e)


@app.route('/read', methods=['POST'])
def read():
    filename = request.form.get('filename')
    bucket = os.getenv('BUCKET_NAME')
    store = Store()
    try:
        data = store.read_as_file(bucket, filename)
        return data or '', 200
    except Exception as e:
        logger.error('bucket was not created')
        abort(400, e)


@app.route('/create_bucket', methods=['POST'])
def create_bucket():
    bucket_name = request.form.get('bucket_name')
    store = Store()
    bucket_name = store.create_bucket(bucket_name=bucket_name)
    if bucket_name:
        return bucket_name, 200
    logger.error('bucket was not created')
    abort(400, '')
