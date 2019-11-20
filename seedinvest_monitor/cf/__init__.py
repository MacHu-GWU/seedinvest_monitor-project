# -*- coding: utf-8 -*-

"""
Cloudformation Template Generation
"""

from troposphere_mate import (
    Template, GetAtt,
    sqs, events, iam, dynamodb,
    canned,
    helper_fn_sub,
)

from seedinvest_monitor.devops.config_init import config

template = Template()

param_env_name = canned.parameter.param_env_name
template.add_parameter(param_env_name)

# -- declare aws resoure
iam_role_for_lbd_func = iam.Role(
    "IamRoleForLbdFunc",
    template=template,
    RoleName=helper_fn_sub("{}-lbd-execution", param_env_name),
    AssumeRolePolicyDocument=canned.iam.create_assume_role_policy_document([
        canned.iam.AWSServiceName.aws_Lambda,
    ]),
    ManagedPolicyArns=[
        canned.iam.AWSManagedPolicyArn.awsLambdaBasicExecutionRole,
        canned.iam.AWSManagedPolicyArn.amazonSQSFullAccess,
        canned.iam.AWSManagedPolicyArn.amazonDynamoDBFullAccess,
        canned.iam.AWSManagedPolicyArn.amazonS3FullAccess,
    ]
)

dynamodb_table_startup = dynamodb.Table(
    "DynamoDBTableStartup",
    template=template,
    TableName=helper_fn_sub("{}-startup", param_env_name),
    KeySchema=[
        dynamodb.KeySchema(
            AttributeName="id",
            KeyType="HASH",
        ),
    ],
    BillingMode="PAY_PER_REQUEST",
    AttributeDefinitions=[
        dynamodb.AttributeDefinition(
            AttributeName="id",
            AttributeType="S",
        ),
    ]
)

sqs_queue = sqs.Queue(
    "SQSQueueScheduler",
    template=template,
    QueueName=config.DYNAMODB_TABLE_STARTUP.get_value(),
    VisibilityTimeout=30,
)

# event_rule = events.Rule(
#     "EventRule",
#     State="ENABLED",
#     ScheduleExpression=expression,
#     Targets=[
#         events.Target(
#             Id="EventRuleStartCrawlerGitHubDataTrigger",
#             Arn=GetAtt(self.lbd_func_aws_object, "Arn"),
#         )
#     ],
#     DependsOn=[
#         self.lbd_func_aws_object,
#     ]
# )

# --- post process ---
common_tags = {
    "ProjectName": config.PROJECT_NAME_SLUG.get_value(),
    "Stage": config.STAGE.get_value(),
    "EnvironmentName": config.ENVIRONMENT_NAME.get_value(),
}
template.create_resource_type_label()
template.update_tags(common_tags)
