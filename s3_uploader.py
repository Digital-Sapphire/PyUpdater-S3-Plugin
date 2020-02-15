# ------------------------------------------------------------------------------
# Copyright (c) 2015-2019 Digital Sapphire
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------


import logging
import os
import sys
import threading

from boto3.session import Session

try:
    from pyupdater.core.uploader import BaseUploader
except ImportError:  # PyUpdater <3.0
    from pyupdater.uploader import BaseUploader

from pyupdater.utils.exceptions import UploaderError

log = logging.getLogger(__name__)


class S3Uploader(BaseUploader):

    name = 'S3'
    author = 'Digital Sapphire'

    def init_config(self, config):
        self.access_key = os.environ.get(u'PYU_AWS_ID')
        if self.access_key is None:
            raise UploaderError('Missing PYU_AWS_ID',
                                expected=True)

        self.secret_key = os.environ.get(u'PYU_AWS_SECRET')
        if self.secret_key is None:
            raise UploaderError(u'Missing PYU_AWS_SECRET',
                                expected=True)

        self.session_token = os.environ.get(u'PYU_AWS_SESSION_TOKEN')

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

        # Try to get bucket key from env var
        self.bucket_key = os.environ.get(u'PYU_AWS_BUCKET_KEY')
        bucket_key = config.get(u'bucket_key')

        # If there is a bucket key in the repo config we
        # override the env var
        if bucket_key is not None:
            self.bucket_key = bucket_key

        # If nothing is set default to bucket root
        if self.bucket_key is None:
            self.bucket_key = ''

        # Strip slashes for sanity
        self.bucket_key = self.bucket_key.rstrip('/\\').lstrip('/\\')

        # Try to get bucket region
        self.bucket_region = os.environ.get(u'PYU_AWS_BUCKET_REGION')
        bucket_region = config.get(u'bucket_region')

        # If there is a bucket key in the repo config we
        # override the env var
        if bucket_region is not None:
            self.bucket_region = bucket_region

        # If nothing is set default to bucket root
        if self.bucket_region is None:
            self.bucket_region = 'us-west-2'

        self._connect()

    def _connect(self):
        session = Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.session_token,
            region_name=self.bucket_region
        )
        self.s3 = session.client('s3')

    def set_config(self, config):
        bucket_name = config.get('bucket_name')
        bucket_name = self.get_answer(
            'Please enter a bucket name',
            default=bucket_name
        )
        config['bucket_name'] = bucket_name

        bucket_key = config.get('bucket_key')
        bucket_key = self.get_answer(
            'Please enter a bucket key',
            default=bucket_key
        )
        config['bucket_key'] = bucket_key

        bucket_region = config.get('bucket_region')
        bucket_region = self.get_answer(
            'Please enter a bucket region',
            default=bucket_region
        )
        config['bucket_region'] = bucket_region

    def upload_file(self, filename):
        """Uploads a single file to S3

        Args:
            filename (str): Name of file to upload.

        Returns:
            (bool) Meanings::

                True - Upload Successful

                False - Upload Failed
        """
        if self.bucket_key is None:
            key = os.path.basename(filename)
        else:
            key = self.bucket_key + '/' + os.path.basename(filename)
        try:
            self.s3.upload_file(
                filename,
                self.bucket_name,
                key,
                ExtraArgs={'ACL': 'public-read'},
                Callback=ProgressPercentage(filename)
            )

            log.debug('Uploaded {}'.format(filename))

            return True

        except Exception as err:
            log.error('Failed to upload file')
            log.debug(err, exc_info=True)

            self._connect()

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
