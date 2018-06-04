import unittest
import main
import os
import shutil

from app.broker.model import Topic
from app.utils.model_utils import  create_offset_file,create_file,create_dir
from app.utils.common import islocal
from os.path import expanduser
HOME = os.getcwd()

"""
Check var/log_test exist
remove dir if exist

create dir
create files
"""


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.topic_name = 'test'

    def tearDown(self):
        _dir = os.getcwd() + '/var/log_test'
        if os.path.isdir(_dir):
            shutil.rmtree(_dir)


    def test_create_file(self):
        _dir = create_dir('log_test/test')
        create_file(_dir + '/index.log')
        create_file(_dir + '/msg.log')
        create_file(_dir + '/ts.log')
        index_log = os.getcwd() + '/var/log_test/{}/index.log'.format(self.topic_name)
        msg_log = os.getcwd() + '/var/log_test/{}/msg.log'.format(self.topic_name)
        ts_log = os.getcwd() + '/var/log_test/{}/ts.log'.format(self.topic_name)

        self.assertTrue(os.path.isfile(index_log))
        self.assertTrue(os.path.isfile(msg_log))
        self.assertTrue(os.path.isfile(ts_log))