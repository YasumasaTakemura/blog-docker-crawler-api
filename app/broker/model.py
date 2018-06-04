# -*- coding: utf-8 -*-

import logging
import os

from app.settings import SETTING
from app.utils.model_utils import get_last_line, create_file, create_offset_file, create_dir

logger = logging.getLogger('DB_Model')
logger.setLevel(logging.DEBUG)


class Topic(object):
    """
    Member props:
        log_file       : file path
        index_file      : pointer of records
        offsets_file    : offsets
        ts_file         : timestamp when /get called
    """

    def __init__(self, topic: str):
        topic_dir = create_dir('log/{}'.format(topic))
        self.log_file = create_file(os.path.join(topic_dir, 'msg.log'))
        self.index_file = create_file(os.path.join(topic_dir, 'index.log'))
        self.offsets_file = create_offset_file(topic_dir)
        self.ts_file = create_file(os.path.join(topic_dir, 'ts.log'))
        self.load()

    def __len__(self):
        self.cache.seek(0, 0)
        length = sum(1 for _ in self.cache)
        return length

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError('expected int but got {}'.format(type(index)))
        if index == -1:
            return get_last_line(self.cache)

        self.cache.seek(0, 0)
        for i, line in enumerate(self.cache):
            if index == i:
                return line.replace('\n', '')

    def load(self):
        """
        Loads data on memory.This cache will be used in each methods.Do not copy or generate list from this cache for memory efficiency
        """
        self.cache = open(self.log_file, 'r')
        logger.info('List of Queue is now dumped and you got pointer of file')

    def check_dup(self, items: list) -> list:
        """ options to applied or not """
        if SETTING.DUPLICATION:
            return items

        cache = self.cache
        lines = list(map(lambda line: line.strip(), cache.readlines()))
        if not lines:
            return items
        lines_no_dup = [item for item in items if item not in set(lines)]
        return lines_no_dup

    def roll_back_commit(self):
        """NotImplementedYet"""
        pass

    def commit(self, msgs: list) -> list:
        # todo : rollback
        # self.roll_back_commit(self.offsets,msg)
        _msgs = map(lambda msg: msg + '\n', self.check_dup(msgs))
        lines = list(_msgs)

        diff = set(msgs) - set(lines)
        if diff:
            logging.error('duplicated messages exist',diff)
        with open(self.log_file, 'a') as f:
            f.writelines(lines)
        return lines

    def get_msg(self, offset):
        """ Get a message """
        self.cache.seek(offset)
        return self.cache.readline()

    def push(self, msgs):
        """ Add line at the end of data """
        if not isinstance(msgs, list):
            raise TypeError('items is required but got {}'.format(type(msgs)))
        lines = self.commit(msgs)
        return ''.join(lines)
