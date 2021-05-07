variable "schedule_exp_ami_create" {}
variable "schedule_exp_ami_delete" {}

resource "aws_cloudwatch_event_rule" "ec2_ami_automation_create_rule" {
  name        = "ec2_ami_automation_create"
  description = "Triggers the lambda which will create automatic AMIs by tag"
  schedule_expression = var.schedule_exp_ami_create
  depends_on = [aws_iam_role.iam_for_lambda]
}

resource "aws_cloudwatch_event_rule" "ec2_ami_automation_delete_rule" {
  name        = "ec2_ami_automation_delete"
  description = "Triggers the lambda which will delete the old AMIs by tag & max count"
  schedule_expression = var.schedule_exp_ami_delete
  depends_on = [aws_iam_role.iam_for_lambda]
}

resource "aws_cloudwatch_event_target" "target_ami_backup_lambda" {
  rule      = aws_cloudwatch_event_rule.ec2_ami_automation_create_rule.name
  arn       = aws_lambda_function.ami_backup_lambda.arn
}

resource "aws_cloudwatch_event_target" "target_ami_delete_lambda" {
  rule      = aws_cloudwatch_event_rule.ec2_ami_automation_delete_rule.name
  arn       = aws_lambda_function.ami_delete_lambda.arn
}
