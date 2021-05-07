variable "ec2_tag_key_env_var" {
  description = "The EC2's tag key that lambda looking up."
  default     = "Backup"
}

variable "ec2_tag_value_env_var" {
  description = "The EC2's tag value that lambda looking up."
  default     = "ec2_ami_automation"
}

variable "schedule_exp_ami_create" {
  description = "The cloudwatch event schedule expression to trigger ami create lambda function."
  default     = "cron(0 18 * * ? *)"
}
variable "schedule_exp_ami_delete" {
  description = "The cloudwatch event schedule expression to trigger ami delete lambda function."
  default     = "cron(0 19 * * ? *)"
}

variable "max_images" {
  description = "The maximun count of backup images"
  default     = 1
}

variable "aws_region" {
  description = "AWS region to deploy the ec2 AMI automation stack"
  default     = "us-east-1"
}