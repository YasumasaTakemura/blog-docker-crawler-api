import logging
import os
from flask import request, Blueprint

from app.broker.model import Topic
from app.consumer.model import Consumer

logger = logging.getLogger('ConsumerView')
app = Blueprint('consumer', __name__, url_prefix=os.getenv('API_VERSION'))


@app.route('/get', methods=['GET'])
def get():
    index = request.args.get('index')
    topic = Topic('test')
    consumer = Consumer(topic)
    msg = consumer.get_msg()
    consumer.commit(msg)
    return msg or '', 200


@app.route('/flush', methods=['GET'])
def flush():
    topic = Topic('test')
    consumer = Consumer(topic)
    offsets = consumer.flush()
    return str(offsets) or '', 200


@app.route('/get_offsets', methods=['GET'])
def get_offsets():
    topic = Topic('test')
    consumer = Consumer(topic)
    return '{}'.format(consumer.offsets) or '', 200
