import unittest
import main
import os
from app.utils.model_utils import create_file, create_offset_file, create_dir
from app.broker.model import Topic
import shutil


class TestBroker(unittest.TestCase):
    def setUp(self):
        self.topic_name = 'test'
        path = lambda filename: os.path.join(os.getcwd() + '/var/log/{}/{}.log'.format(self.topic_name, filename))
        self.msg = path('msg')
        self.index = path('index')
        self.offsets = path('offsets')
        self.ts = path('ts')

        create_dir('log/{}'.format(self.topic_name))
        create_file('log/{}/msg.log'.format(self.topic_name))
        create_file('log/{}/index.log'.format(self.topic_name))
        # create_file('log/{}/ts.log'.format(self.topic_name))
        create_offset_file('test')

    def tearDown(self):
        for filename in [self.msg, self.index, self.offsets, self.ts]:
            os.remove(filename)

        shutil.rmtree(os.getcwd() + '/var/log/{}'.format(self.topic_name))

    def test_push(self):
        paths = ['path/1', 'path/2', 'path/3']
        topic = Topic('test')
        lines = topic.push(paths)
        self.assertEqual('\n'.join(paths) + '\n', lines)

    def test_is_correct_offsets(self):
        """ is create_offset_file working """
        paths = ['path/1', 'path/2', 'path/3']
        topic = Topic('test')
        # lines = topic.push(paths)
        # self.assertEqual('\n'.join(paths) + '\n', lines)

        with open(self.offsets) as f:
            _offset = f.read()

        self.assertEqual('0', _offset)
