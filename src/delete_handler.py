import os
import boto3
from Image import Image

ec2_client = boto3.client('ec2', 'ap-northeast-2')
ec2_res = boto3.resource('ec2', 'ap-northeast-2')
tag_key = os.environ.get('TAG_KEY', 'Backup')
tag_value = os.environ.get('TAG_VALUE', 'by_ami_automation')


def _ami_delete():
    image = Image().filter()
    image.delete_amis()


def lambda_handler(event, context):
    _ami_delete()

    return {
        'statusCode': 200,
        'body': 'Delete AMI requested.'
    }
