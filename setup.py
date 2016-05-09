from setuptools import setup

setup(
    name='PyUpdater-s3-Plugin',
    version='3.0.4',
    description='Amazon S3 plugin for PyUpdater',
    author='Digital Sapphire',
    author_email='info@digitalsapphire.io',
    url='https://github.com/JMSwag/PyUpdater-s3-Plugin',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2.7',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],
    platforms=['Any'],
    install_requires=[
        'boto3',
        'jms-utils >= 1.0.1',
        ],
    provides=['pyupdater.plugins',],
    entry_points={
        'pyupdater.plugins': [
            's3 = s3_uploader:S3Uploader',
        ],
    },
    py_modules=['s3_uploader'],
    include_package_data=True,
    zip_safe=False,
)
