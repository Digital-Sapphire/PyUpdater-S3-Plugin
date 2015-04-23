# The MIT License (MIT)
#
# Copyright (c) 2014 JohnyMoSwag <johnymoswag@gmail.com>
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

# Really Ugly Imports
# Suggestions welcome
import logging
import os
import sys

try:
    from boto3.s3.connection import S3Connection
except ImportError:
    boto3 = None
    try:
        from boto.s3.connection import S3Connection
        from boto.s3.key import Key
    except ImportError:
        boto = None
from jms_utils.paths import ChDir

from pyupdater.uploader import BaseUploader
from pyupdater.utils.exceptions import UploaderError

log = logging.getLogger(__name__)


# TODO: figure out how to upload files
# deeper then just the root directory
class S3Uploader(BaseUploader):

    def __init__(self):
        super(S3Uploader, self).__init__()

    def init(self, **kwargs):
        self.file_list = kwargs.get(u'files', [])
        a_key = os.environ.get(u'PYU_AWS_ID')
        if a_key is None:
            raise UploaderError('Missing PYU_AWS_ID')
        self.access_key = a_key
        s_key = os.environ.get(u'PYU_AWS_SECRET')
        if s_key is None:
            raise UploaderError(u'Missing PYU_AWS_SECRET')
        self.secret_key = s_key
        self.bucket_name = os.environ.get(u'PYU_AWS_BUCKET')
        bucket_name = kwargs.get(u'object_bucket')
        if bucket_name is not None:
            self.bucket_name = bucket_name
        if self.bucket_name is None:
            raise UploaderError(u'Bucket name is not set')
        self._connect()

    # ToDo: Remove in v2.0
    def _connect(self):
        self.connect()
    # End ToDo

    def connect(self):
        """Connects client attribute to S3"""
        self.s3 = S3Connection(aws_access_key_id=self.access_key,
                               aws_secret_access_key=self.secret_key,
                               debug=False)
        bucket = self.s3.get_bucket(self.bucket_name)
        self.client = Key(bucket)

    # ToDo: Remove in v2.0
    def _upload_file(self, filename):
        self.upload_file(self, filename)
    # End ToDo

    def upload_file(self, filename):
        """Uploads a single file to S3

        Args:
            filename (str): Name of file to upload.

        Returns:
            (bool) Meanings::

                True - Upload Successful

                False - Upload Failed
        """
        with ChDir(self.deploy_dir):
            self.client.key = filename
            try:
                self.client.set_contents_from_filename(filename,
                                                       cb=self.s3_progress)
                self.client.make_public()
                log.debug('Uploaded {}'.format(filename))
                os.remove(filename)
                return True
            except Exception as e:
                log.error(str(e), exc_info=True)
                self._connect()
                return False

    def s3_progress(self, current, total):
        percent = float(current) / total * 100
        sys.stdout.write('\r%.1f' % percent)
        sys.stdout.flush()
