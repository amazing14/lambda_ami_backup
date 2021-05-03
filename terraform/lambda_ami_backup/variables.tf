variable "ec2_tag_key_env_var" {
  description = "The EC2's tag key that lambda looking up."
  default     = "Backup"
}

variable "ec2_tag_value_env_var" {
  description = "The EC2's tag value that lambda looking up."
  default     = "by_ami_automation"
}

variable "schedule_exp" {
  description = "The cloudwatch event schedule expression."
  default     = "rate(15 minutes)"
  //    default = "cron(0 18 * * ? *)"
}

variable "max_images" {
  description = "The maximun count of backup images"
  default     = 1
}