from setuptools import setup

setup(
    name='PyUpdater-s3-Plugin',
    version='3.0',
    description='Amazon S3 plugin for PyUpdater',
    author='JohnyMoSwag',
    author_email='johnymoswag@gmail.com',
    url='https://github.com/JohnyMoSwag/PyUpdater-s3-Plugin',
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
    packages=['s3_plugin'],
    include_package_data=True,
    namespace_packages = ['pyupdater.plugins'],
    zip_safe=False,
)
