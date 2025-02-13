# Daily EC2 AMI Backup by lambda
This project using `Terraform` to help you deploy a AWS `Lambda` function with `IAM Role` and `Cloudwatch Event`.  

![simple darchitecture](./img/simple-architecture.png)

If your EC2 has a tag key `Backup` and value `ec2_ami_automation`, then it'll be backup AMI by lambda.

**EC2 Tag Example**
![example](./img/ec2_capture.png)

## Prerequisites
* terraform installed (version >= 0.12.1)
* python3 (version >= 3.7) (if you want to test on your local)

## Deployment guide
```bash
# Archive your python code.
$ ./build.sh


$ cd terraform/lambda_ami_backup

$ terraform init
$ terraform plan
$ terraform apply 
```

## Configuration
If you want to customize, see `terraform/lambda_ami_backup/variables.tf` file.

```text
variable "ec2_tag_key_env_var" {
  description = "The EC2's tag key that lambda looking up."
  default     = "Backup"
}

variable "ec2_tag_value_env_var" {
  description = "The EC2's tag value that lambda looking up."
  default     = "ec2_ami_automation"
}

variable "schedule_exp_ami_create" {
  description = "The cloudwatch event schedule expression to trigger ami create lambda function at 6PM daily"
  default     = "cron(0 18 * * ? *)"
}
variable "schedule_exp_ami_delete" {
  description = "The cloudwatch event schedule expression to trigger ami delete lambda function at 7PM daily"
  default     = "cron(0 19 * * ? *)"
}

variable "max_images" {
  description = "The maximun count of backup images"
  default     = 5
}

variable "aws_region" {
  description = "AWS region to deploy the ec2 AMI automation stack"
  default     = "us-east-1"
}
```

cron details: https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html

corn schedule generator: http://www.cronmaker.com/
