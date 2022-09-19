## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 0.15.0, < 2.0.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 3.9.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 3.9.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_event_rule.commit](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.deploy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_log_group.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_subscription_filter.error_parser_logfilter](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_subscription_filter) | resource |
| [aws_cloudwatch_metric_alarm.lambda_error](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_lambda_function.error_parser](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda_sync](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_permission.allow_cloudwatch_for_error_parser](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [aws_lambda_permission.with_sns](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [aws_sns_topic.lambda_error](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic) | resource |
| [aws_sns_topic.sync](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic) | resource |
| [aws_sns_topic_policy.container_status_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic_policy) | resource |
| [aws_sns_topic_policy.lambda_error_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic_policy) | resource |
| [aws_sns_topic_subscription.send_container_status](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic_subscription) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.sns_lambda_error_access_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sns_topic_access_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allow"></a> [allow](#input\_allow) | list of repo to be converted if empty all are permitted | `string` | n/a | yes |
| <a name="input_conversions"></a> [conversions](#input\_conversions) | dictionary with special repo conversions in json | `string` | n/a | yes |
| <a name="input_deny"></a> [deny](#input\_deny) | list of repos to not be converted | `string` | n/a | yes |
| <a name="input_deploy_environment"></a> [deploy\_environment](#input\_deploy\_environment) | is environment test or prod | `string` | n/a | yes |
| <a name="input_prefix"></a> [prefix](#input\_prefix) | some to differentiate, usually project 'fdh' or 'dpl' | `string` | n/a | yes |
| <a name="input_prefix_destination"></a> [prefix\_destination](#input\_prefix\_destination) | incoming prefix for codecommit | `string` | n/a | yes |
| <a name="input_prefix_source"></a> [prefix\_source](#input\_prefix\_source) | outcoming prefix for codecommit | `string` | n/a | yes |
| <a name="input_repo_path"></a> [repo\_path](#input\_repo\_path) | something in the form 'git-codecommit.eu-west-1.amazonaws.com/v1/repos' | `string` | n/a | yes |
| <a name="input_retention_in_days"></a> [retention\_in\_days](#input\_retention\_in\_days) | how many days wait before deleting logs | `number` | `30` | no |
| <a name="input_role_arn"></a> [role\_arn](#input\_role\_arn) | assumed to create infrastructure in enviroment where .hcl is ran | `string` | n/a | yes |
| <a name="input_role_arn_lambda_name"></a> [role\_arn\_lambda\_name](#input\_role\_arn\_lambda\_name) | role used by lambda | `string` | n/a | yes |
| <a name="input_role_arn_lambda_sync_name"></a> [role\_arn\_lambda\_sync\_name](#input\_role\_arn\_lambda\_sync\_name) | role used by lambda | `string` | n/a | yes |
| <a name="input_tag"></a> [tag](#input\_tag) | tag to be added | `map(any)` | `{}` | no |
| <a name="input_timeout"></a> [timeout](#input\_timeout) | how many seconds before quitting lambda | `number` | `15` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_role_arn"></a> [role\_arn](#output\_role\_arn) | default role |
| <a name="output_role_arn_lambda"></a> [role\_arn\_lambda](#output\_role\_arn\_lambda) | default role |
