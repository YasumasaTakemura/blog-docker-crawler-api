import unittest
import main
import os
from app.broker.model import Topic
from app.utils.model_utils import create_file, create_offset_file, create_dir
import shutil

class TestConsumerView(unittest.TestCase):
    def setUp(self):
        # todo :
        self.topic_name = 'test'
        self.path = lambda filename :os.path.join(os.getcwd() + '/var/log/{}/{}.log'.format(self.topic_name,filename))
        self.msg = self.path('msg')
        self.index = self.path('index')
        self.offset = self.path('offsets')
        self.ts = self.path('ts')

        create_dir('log/{}'.format(self.topic_name))
        create_file('log/{}/index.log'.format(self.topic_name))
        create_file('log/{}/ts.log'.format(self.topic_name))
        create_offset_file('test')

        self.app = main.app.test_client()
        self.app.post('/v2/push',data=dict(path=['path/1','path/2','path/3']))

    def tearDown(self):
        msg = os.getcwd() + '/var/log/test/msg.log'
        index = os.getcwd() + '/var/log/test/index.log'
        offset = os.getcwd() + '/var/log/test/offsets.log'
        ts = os.getcwd() + '/var/log/test/ts.log'

        # remove files
        for filename in [msg,index,offset,ts] :
            os.remove(filename)

        # remove dirs
        _dir = os.getcwd() + '/var/log/{}'.format(self.topic_name)
        if os.path.isdir(_dir):
            shutil.rmtree(_dir)

    def test_get(self):
        res = self.app.get('/v2/get')
        self.assertEqual(res.data.decode('utf8'),'path/1\n')
