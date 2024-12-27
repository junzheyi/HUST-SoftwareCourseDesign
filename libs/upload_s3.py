# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 15:28
# @Author  : Junzhe Yi
# @File    : upload_s3.py
# @Software: PyCharm

import boto3
from botocore.exceptions import ClientError
from os.path import basename
from libs.read_config import ReadConfig


def upload_file(filename):
    try:
        my_config = ReadConfig("config/config.ini")
        session = boto3.Session(profile_name=my_config.aws_profile_name)
        s3_client = session.client("s3")
        response = s3_client.upload_fileobj(filename, Bucket=my_config.s3_bucket,
                                            Key=filename.name
                                            )
        return True
    except ClientError as e:
        print(e)
        return False


if __name__ == '__main__':
    upload_file(r"libs/flush_all_milvus_collection.py")
