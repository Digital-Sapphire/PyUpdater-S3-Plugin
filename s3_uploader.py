# The MIT License (MIT)
#
# Copyright (c) 2016 Digital Sapphire
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import logging
import os
import sys
import threading

from boto3.session import Session

from pyupdater.uploader import BaseUploader
from pyupdater.utils.exceptions import UploaderError

log = logging.getLogger(__name__)


class S3Uploader(BaseUploader):

    name = 'S3'
    author = 'Digital Sapphire'

    def init_config(self, config):
        access_key = os.environ.get(u'PYU_AWS_ID')
        if access_key is None:
            raise UploaderError('Missing PYU_AWS_ID',
                                expected=True)
        secret_key = os.environ.get(u'PYU_AWS_SECRET')
        if secret_key is None:
            raise UploaderError(u'Missing PYU_AWS_SECRET',
                                expected=True)
        # Try to get bucket from env var
        self.bucket_name = os.environ.get(u'PYU_AWS_BUCKET')
        bucket_name = config.get(u'bucket_name')
        # If there is a bucket name in the repo config we
        # override the env var
        if bucket_name is not None:
            self.bucket_name = bucket_name
        # If nothing is set throw an error
        if self.bucket_name is None:
            raise UploaderError(u'Bucket name is not set',
                                expected=True)

        session = Session(aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name='us-west-2')

        self.s3 = session.client('s3')

    def set_config(self, config):
        bucket_name = config.get('bucket_name')
        bucket_name = self.get_answer('Please enter a bucket name',
                                      default=bucket_name)
        config['bucket_name'] = bucket_name

    def upload_file(self, filename):
        """Uploads a single file to S3

        Args:
            filename (str): Name of file to upload.

        Returns:
            (bool) Meanings::

                True - Upload Successful

                False - Upload Failed
        """
        try:
            self.s3.upload_file(filename, self.bucket_name, filename,
                                ExtraArgs={'ACL': 'public-read'},
                                Callback=ProgressPercentage(filename))
            log.debug('Uploaded {}'.format(filename))
            return True
        except Exception as e:
            log.error('Failed to upload file')
            log.debug(str(e), exc_info=True)
            return False


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s / %s  (%.2f%%)" % (self._seen_so_far,
                                         self._size, percentage))
            sys.stdout.flush()
