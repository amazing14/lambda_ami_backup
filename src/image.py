import operator
import os
from datetime import datetime

import boto3


class Image:
    def __init__(self):
        self.tag_key = os.environ.get('TAG_KEY', 'Backup')
        self.tag_value = os.environ.get('TAG_VALUE', 'ec2_ami_automation')
        self.region = os.environ.get('AWS_REGION', 'us-east-1')
        self.max_reserved_count = int(os.environ.get('MAX_RESERVED_COUNT', 5))

        self.ec2_client = boto3.client('ec2', region_name=self.region)
        self.ec2_res = boto3.resource('ec2', region_name=self.region)
        self.amis: list = []
        self.amis_to_delete: dict = {}

    def bake(self, ec2_id: str, name: str) -> None:
        now = datetime.now().strftime("%Y-%m-%dT%H-%M")
        image_name = f'ec2_ami_auto_backup_{name}_{now}'

        ami: dict = self.ec2_client.create_image(
            NoReboot=True,
            Name=image_name,
            Description=f'Instance {name} - automated daily AMI backup by ec2 ami automation.',
            InstanceId=ec2_id
        )

        image = self.ec2_res.Image(ami.get('ImageId', ''))

        if image:
            image.create_tags(
                Tags=[
                    {'Key': 'Name', 'Value': image_name},
                    {'Key': self.tag_key, 'Value': self.tag_value},
                    {'Key': 'Image_group', 'Value': name},
                ]
            )

        print('AMI:{} created from Instace: {}'.format(ami.get("ImageId", ""), ec2_id))

    def filter_images(self):
        filters = [
            {
                'Name': f'tag:{self.tag_key}', 'Values': [self.tag_value]
            }
        ]
        filtered_amis = self.ec2_client.describe_images(Filters=filters)
        self.amis = filtered_amis.get('Images', '')

    def delete_amis(self):
        self.filter_images()
        self.__get_ami_group_by_tag_name()

        for group_name, images in self.amis_to_delete.items():
            if (len(images)) > self.max_reserved_count:
                images.sort(key=operator.itemgetter('CreationDate'), reverse=True)
                images_to_delete = images[self.max_reserved_count:]
                print("AMIs to be deregistered: {}".format(images_to_delete))
                self.__delete_amis(images_to_delete)

    # Get snapshots associated with the images
    def __get_snapshot_ids(self, image_id):
        ImageDetails = self.ec2_client.describe_images(DryRun=False, ImageIds=[image_id])
        DeviceMappings = ImageDetails['Images'][0]['BlockDeviceMappings']
        SnapshotIds = []
        for device in DeviceMappings:
            if "Ebs" not in device:  # Skip if the device is not an EBS volume
                continue
            SnapshotIds.append(device['Ebs']['SnapshotId'])
        return SnapshotIds

    # Delete snapshots associated with the images
    def __delete_snapshots(self, image_id, snapshot_ids):
        for SnapshotId in snapshot_ids:
            self.ec2_client.delete_snapshot(DryRun=False, SnapshotId=SnapshotId)
            print("Snapshot with id : {} of the ami: {} is DELETED".format(SnapshotId, image_id))

    def __delete_amis(self, images_to_delete):
        for img in images_to_delete:
            image_id = img['ImageId']
            snapshot_ids = self.__get_snapshot_ids(image_id=image_id)
            self.ec2_client.deregister_image(ImageId=image_id)
            print('AMI: {} is deregistered. Deleting the snapshots...'.format(image_id))
            self.__delete_snapshots(image_id=image_id, snapshot_ids=snapshot_ids)

    def __get_ami_group_by_tag_name(self):
        for img in self.amis:
            group_name = self.__get_tag_value_with_key(img['Tags'], 'Image_group')

            if group_name not in self.amis_to_delete:
                self.amis_to_delete[group_name] = []

            self.amis_to_delete[group_name].append({
                'ImageId': img['ImageId'],
                'CreationDate': img['CreationDate']
            })

    def __get_tag_value_with_key(self, tags, key):
        for key_value in tags:
            if key in key_value.get('Key', ''):
                return key_value.get('Value', '')
