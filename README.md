[![PyPI version](https://badge.fury.io/py/PyUpdater-S3-Plugin.svg)](https://badge.fury.io/py/PyUpdater-S3-Plugin)

# PyUpdater S3 plugin

PyUpdater upload plugin for AWS S3

## Installing

    $ pip install PyUpdater-S3-plugin


## Configuration

System environmental variables

Optional - If set will be used globally. Will be overwritten when you add S3 settings during pyupdater init

| Env Var              | Meaning                                 |
| --------------------- |---------------------------------------- |
| PYU_AWS_ID            | Your amazon api id                      |
| PYU_AWS_SECRET        | You amazon api secret                   |
| PYU_AWS_SESSION_TOKEN | You amazon api session token (optional) |
| PYU_AWS_BUCKET        | Bucket name (optional)                  |
| PYU_AWS_BUCKET_REGION | AWS Bucket Region (optional)            |
| PYU_AWS_BUCKET_KEY    | AWS Bucket Key (optional)               |
| PYU_AWS_ENDPOINT_URL  | AWS Endpoint URL (optional)             |
