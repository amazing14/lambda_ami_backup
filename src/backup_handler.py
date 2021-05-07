import os
import itertools
import boto3

from image import Image

class EC2:
    def __init__(self):
        self.tag_key = os.environ.get('TAG_KEY', 'Backup')
        self.tag_value = os.environ.get('TAG_VALUE', 'by_ami_automation')
        self.region = os.environ.get('AWS_REGION', 'us-east-1')
        self.ec2_client = boto3.client('ec2', region_name=self.region)
        self.reservations = None

    def __get_id_and_name(self, instance):
        instance_id = instance['InstanceId']
        instance_name = ''

        for tags in instance.get('Tags', []):
            if tags.get('Key', '') == 'Name':
                instance_name = tags.get('Value', '')

        ec2_details = dict()
        ec2_details['instance_id'] = instance_id
        ec2_details['instance_name'] = instance_name

        return ec2_details

    def get_instance_ids_and_names(self) -> list:
        filters = [{
            'Name': 'tag:' + self.tag_key, 'Values': [self.tag_value]
        }]
        reservations = self.ec2_client.describe_instances(Filters=filters)
        reserves = reservations.get('Reservations', [])
        item = []
        for res in reserves:
            instances = res.get('Instances', [])
            item.append(map(self.__get_id_and_name, instances))

        return list(itertools.chain(*item))


def _ami_backup():
    ec2_obj = EC2()
    ec2_info: list = ec2_obj.get_instance_ids_and_names()
    print("AMIs will be create for the EC2 instances :{}".format(ec2_info))
    image = Image()
    for ec2 in ec2_info:
        name = ec2.get('instance_name')
        ec2_id = ec2.get('instance_id')
        print("Baking AMI for the instance name: {} id: {}".format(name, ec2_id))
        image.bake(ec2_id=ec2_id, name=name)


def lambda_handler(event, context):
    _ami_backup()

    return {
        'statusCode': 200,
        'body': 'Create AMI backup requested.'
    }

# for local testing
# lambda_handler("event", "context")