import unittest
import main
import os
import shutil
from app.broker.model import Topic

class TestBroker(unittest.TestCase):
    def setUp(self):
        self.app = main.app.test_client()
        self.topic_name = 'test'

    def tearDown(self):
        msg = os.getcwd() + '/var/log/test/msg.log'
        index = os.getcwd() + '/var/log/test/index.log'
        offset = os.getcwd() + '/var/log/test/offsets.log'
        ts = os.getcwd() + '/var/log/test/ts.log'

        for filename in [msg,index,offset,ts] :
            os.remove(filename)

        shutil.rmtree(os.getcwd() + '/var/log/{}'.format(self.topic_name))

    def test_push(self):
        res = self.app.post('/v2/push',data=dict(path=['path/1','path/2','path/3']))
        expected =  '\n'.join(['path/1', 'path/2','path/3']) + '\n'
        self.assertEqual(res.data.decode('utf8'),expected)
