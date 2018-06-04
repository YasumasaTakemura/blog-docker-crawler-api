from google.cloud import storage
from google.api_core.exceptions import Forbidden
import base64
from flask import abort
from google.api_core.exceptions import Conflict
import bz2
import logging
from io import BytesIO
import os
from datetime import datetime

logger = logging.getLogger('Store_model')


class Store(object):
    """singleton"""
    _instance = None

    def __init__(self):
        self.connect()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        try:
            self.client = storage.Client()
        except Exception as e:
            logger.error(str(e))

    def create_bucket(self, bucket_name):
        try:
            bucket = self.client.create_bucket(bucket_name)
            return bucket.name
        except Conflict as e:
            logger.error(e)
            abort(400, '')

    def delete_bucket(self, bucket_name):
        """Deletes a bucket. The bucket must be empty."""
        bucket = self.client.get_bucket(bucket_name)
        bucket.delete()
        logger.error('Bucket {} deleted'.format(bucket.name))
        print('Bucket {} deleted'.format(bucket.name))

    def list_blobs(self, bucket_name):
        """Lists all the blobs in the bucket."""
        # type : (str)=> (list)
        try:
            bucket = self.client.get_bucket(bucket_name)
        except Exception as e:
            logger.error(e)
            raise Exception(str(e))

        blobs = bucket.list_blobs()
        res = []
        for blob in blobs:
            res.append(blob.name)
        return res

    def list_blobs_with_prefix(self, bucket_name, prefix, delimiter='/'):
        """Lists all the blobs in the bucket."""
        # type : (str)=> (list)
        bucket = self.client.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
        res = []
        for blob in blobs:
            res.append(blob.name)
        if delimiter:
            for prefix in blobs.prefixes:
                res.append(prefix)
        return res

    def write(self, bucket_name, filename, data, enc_key=None):
        # Encryption key must be an AES256 key represented as a bytestring with
        # 32 bytes. Since it's passed in as a base64 encoded string, it needs
        # to be decoded.
        try:
            bucket = self.client.get_bucket(bucket_name)
        except Forbidden as e:
            logger.error(e)
            raise Forbidden(str(e))
        blob = storage.Blob(filename, bucket, encryption_key=enc_key)
        data = bz2.compress(data.encode(), 9)
        try:
            blob.upload_from_string(data, content_type='application/gzip')
            return '/{}/{}'.format(bucket_name, filename)
        except Exception as e:
            logger.error(e)

    def get_blob(self, bucket_name, filename, enc_key=None):
        bucket = self.client.get_bucket(bucket_name)
        if enc_key:
            enc_key = base64.b64decode(enc_key)
        return storage.Blob(filename, bucket, encryption_key=enc_key)

    def read(self, bucket_name, filename, enc_key=None):
        """ read file as string """
        blob = self.get_blob(bucket_name, filename, enc_key)
        string_buffer = BytesIO()
        blob.download_to_file(string_buffer)
        try:
            data = string_buffer.getvalue()
            data = bz2.decompress(data).decode()
        except Exception as e:
            logging.error(e)
            raise e
        return data

    def read_as_file(self, bucket_name, filename, enc_key=None):
        """ read and save file """
        data = self.read(bucket_name, filename, enc_key=enc_key)
        self._write_file(data, filename)

    def _write_file(self, data, filename):
        filename += '.html'
        with open(filename, 'w') as f:
            f.write(data)

    def decomp(self, filename):
        with open(filename, 'rb') as f:
            data = f.read()
        return bz2.decompress(data).decode()

    def buck_up(self, dirname: str, filename: str):
        assert os.getenv('BUCKUP_DIR')
        bucket_name = os.getenv('BUCKUP_DIR') + dirname
        with open(filename) as f:
            data = f.read()
        filename += '_' + datetime.now().strftime('%Y-%m-%d')
        self.write(bucket_name, filename, data, enc_key=None)
