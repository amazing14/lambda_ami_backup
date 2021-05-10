from image import Image


def _ami_delete():
    image = Image()
    image.delete_amis()


def lambda_handler(event, context):
    _ami_delete()

    return {
        'statusCode': 200,
        'body': 'Delete AMI requested.'
    }

# ### local testing
# if __name__ == "__main__":
#     lambda_handler("event", "context")