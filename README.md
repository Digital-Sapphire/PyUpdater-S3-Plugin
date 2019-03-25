[![PyPI version](https://badge.fury.io/py/PyUpdater-S3-Plugin.svg)](http://badge.fury.io/py/PyUpdater-S3-Plugin)

# PyUpdater S3 plugin

PyUpdater upload plugin for AWS S3

## Installing

    $ pip install PyUpdater-S3-plugin


## Configuration

System environmental variables

Optional - If set will be used globally. Will be overwritten when you add scp settings during pyupdater init

| Variable              | Meaning                                 |
| --------------------- |---------------------------------------- |
| PYIU_AWS_ID           | Your amazon api id                      |
| PYIU_AWS_SECRET       | You amazon api secret                   |
| PYU_AWS_SESSION_TOKEN | You amazon api session token (optional) |
| PYIU_AWS_BUCKET       | Bucket name (optional)                  |


## Changes

* v1.1

    - Updated

        Compat with PyUpdater 0.19+