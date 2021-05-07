provider "template" {
  version = "~> 2.1"
}

provider "aws" {
  version = "~> 2.14"
  region  = var.aws_region
}

module "lambda_ami_backup" {
  source       = "./modules"
  schedule_exp_ami_create = var.schedule_exp_ami_create
  schedule_exp_ami_delete = var.schedule_exp_ami_delete
  tag_key      = var.ec2_tag_key_env_var
  tag_value    = var.ec2_tag_value_env_var
  max_images   = var.max_images
}