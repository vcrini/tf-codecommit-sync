data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

variable "deploy_environment" {
  description = "is environment test or prod"
  type        = string
}
variable "prefix" {
  description = "some to differentiate, usually project 'fdh' or 'dpl'"
  type        = string
}
variable "prefix_destination" {
  description = "incoming prefix for codecommit"
  type        = string
}
variable "prefix_source" {
  description = "outcoming prefix for codecommit"
  type        = string
}
variable "repo_path" {
  description = "something in the form 'git-codecommit.eu-west-1.amazonaws.com/v1/repos'"
  type        = string
}
variable "conversions" {
  description = "dictionary with special repo conversions in json"
  type        = string
}
variable "deny" {
  description = "list of repos to not be converted"
  type        = string
}
variable "allow" {
  description = "list of repo to be converted if empty all are permitted"
  type        = string
}
variable "retention_in_days" {
  default     = 30
  description = "how many days wait before deleting logs"
  type        = number
}
variable "role_arn" {
  description = "assumed to create infrastructure in enviroment where .hcl is ran"
  type        = string
}
variable "role_arn_lambda_name" {
  description = "role used by lambda"
  type        = string
}
variable "role_arn_lambda_sync_name" {
  description = "role used by lambda"
  type        = string
}
variable "tag" {
  default = {
  }
  description = "tag to be added"
  type        = map(any)
}
variable "timeout" {
  default     = 15
  description = "how many seconds before quitting lambda"
  type        = number
}
locals {
  region               = data.aws_region.current.name
  account_id           = data.aws_caller_identity.current.account_id
  role_prefix          = "arn:aws:iam::${local.account_id}:role/"
  role_arn_lambda      = "${local.role_prefix}${var.role_arn_lambda_name}"
  role_arn_lambda_sync = "${local.role_prefix}${var.role_arn_lambda_sync_name}"
}
