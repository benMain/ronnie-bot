import boto3
import os
from datetime import datetime


class S3Client(object):
    """s3 Client for checking timestamp!"""

    def __init__(self):
        super(S3Client, self).__init__()
        self.client = boto3.client('s3', 'us-west-2')
        self.format = "%Y-%m-%dT%H:%M:%S"
        self.bucket = 'ronnie-bot-config'
        self.key = 'LastPostTimestamp.txt'
        self.file_name = '/tmp/{}'.format(self.key)
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        self.file = open(self.file_name, 'w')

    def get_last_post(self):
        timeFile = self.client.get_object(Bucket=self.bucket,
                                          Key=self.key)
        return datetime.strptime(timeFile['Body'].read(), self.format)

    def write_last_post(self, timestamp):
        time_string = timestamp.strftime(self.format)
        self.file.write(time_string)
        self.file.close()
        self.client.upload_file(
            self.file_name, self.bucket, self.key)
