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
from setuptools import setup

import versioneer


with open('README.md', 'r') as f:
    readme = f.read()


setup(
    name='PyUpdater-S3-Plugin',
    version=versioneer.get_version(),
    description='Amazon S3 plugin for PyUpdater',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Digital Sapphire',
    author_email='info@digitalsapphire.io',
    url='https://github.com/DigitalSapphire/PyUpdater-s3-Plugin',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Environment :: Console'
                 ],
    platforms=['Any'],
    install_requires=['boto3>=1.9.0'],
    entry_points={
        'pyupdater.plugins.upload': [
            's3 = s3_uploader:S3Uploader',
        ],
    },
    py_modules=['s3_uploader'],
    include_package_data=True,
    zip_safe=False,
)
