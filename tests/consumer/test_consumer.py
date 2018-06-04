import unittest
import main
import os
from app.consumer.model import Consumer
from app.broker.model import Topic
from app.utils.model_utils import create_file, create_offset_file, create_dir
import shutil


class TestConsumer(unittest.TestCase):
    def setUp(self):
        """ create dir and files """
        self.topic_name = 'test'
        path = lambda filename: os.path.join(os.getcwd() + '/var/log/{}/{}.log'.format(self.topic_name, filename))
        self.msg = path('msg')
        self.index = path('index')
        self.offsets = path('offsets')
        self.ts = path('ts')

        create_dir('log/{}'.format(self.topic_name))
        create_file('log/{}/index.log'.format(self.topic_name))
        create_file('log/{}/ts.log'.format(self.topic_name))
        create_offset_file('test')


    def tearDown(self):
        """ remove dir and files """
        for filename in [self.index, self.offsets, self.ts]:
            os.remove(filename)

        shutil.rmtree(os.getcwd() + '/var/log/{}'.format(self.topic_name))

    def test_is_correct_offsets(self):
        """ is create_offset_file working """

        print('====LIST=====')
        print(os.listdir('/Users/yasumasatakemura/projects/teit/docker-crawler-api/var/log/test'))
        cwd = os.getcwd() + '/var/log/{}'.format(self.topic_name)

        if not os.path.isdir(cwd):
            create_dir('/log/{}'.format(self.topic_name))

        with open(self.offsets) as f:
            _offset = f.read()

        self.assertEqual('0', _offset)

    def test_get(self):
        """ is /get working properly """
        topic = Topic(self.topic_name)
        consumer = Consumer(topic)
        msg = consumer.get_msg()
        consumer.commit(msg)
        with open(self.offsets) as f:
            _offset = f.read()
        self.assertEquals("0", _offset)

    def test_is_correct_offset(self):
        """ is correct offsets """
        topic = Topic(self.topic_name)
        paths = ['path/1', 'path/2', 'path/3']
        lines = topic.push(paths)
        self.assertEqual('\n'.join(paths) + '\n', lines)

        consumer = Consumer(topic)
        msg = consumer.get_msg()
        consumer.commit(msg)
        with open(self.offsets) as f:
            _offset = f.read()
        self.assertEqual("7", _offset)

    def test_is_correct_index(self):
        """ is correct index """
        topic = Topic(self.topic_name)
        paths = ['path/1']
        topic.push(paths)

        consumer = Consumer(topic)
        msg = consumer.get_msg()
        consumer.commit(msg)

        with open(self.index) as f:
            _index = f.read()
        self.assertEqual("0\t7\n", _index)
