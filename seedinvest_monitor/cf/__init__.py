# -*- coding: utf-8 -*-

"""
Cloudformation Template Generation
"""

from troposphere_mate import (
    Template, Ref,
    sqs, iam, dynamodb, awslambda, events,
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
    QueueName=helper_fn_sub("{}-download-job", param_env_name),
    VisibilityTimeout=30,
)

#--- Lambda Function
aws_lambda_func_code = awslambda.Code(
    S3Bucket=config.S3_BUCKET_FOR_DEPLOY.get_value(),
    S3Key=config.LAMBDA_CODE_S3_KEY.get_value()
)
aws_lambda_layers = config.LAMBDA_LAYERS.get_value()
aws_lambda_environment = awslambda.Environment(
    Variables={
        k: v
        for k, v in config.to_dict(prefix="SEEDINVEST_MONITOR_").items()
        if isinstance(v, str)
    },
)

lbd_func_update_new_project = awslambda.Function(
    "LbdFuncUpdateNewProject",
    template=template,
    FunctionName=helper_fn_sub("{}-update-new-project", param_env_name),
    Code=aws_lambda_func_code,
    Layers=aws_lambda_layers,
    Handler="seedinvest_monitor.handlers.update_new_project.handler",
    MemorySize=128,
    Timeout=120,
    Runtime="python3.6",
    Environment=aws_lambda_environment,
    Role=iam_role_for_lbd_func.iam_role_arn,
)

event_rule_update_new_project = events.Rule(
    "EventRuleUpdateNewProject",
    template=template,
    State="ENABLED",
    ScheduleExpression=config.UPDATE_NEW_PROJECT_RATE.get_value(),
    Targets=[
        events.Target(
            Id="EventRuleUpdateNewProject",
            Arn=lbd_func_update_new_project.lbd_func_arn,
        )
    ],
    DependsOn=[
        lbd_func_update_new_project,
    ]
)

lbd_permission_event_rule_update_new_project = awslambda.Permission(
    "LbdPermissionEventRuleUpdateNewProject",
    template=template,
    Action="lambda:InvokeFunction",
    FunctionName=lbd_func_update_new_project.lbd_func_arn,
    Principal="events.amazonaws.com",
    SourceArn=event_rule_update_new_project.event_rule_arn,
    DependsOn=[
        event_rule_update_new_project,
        lbd_func_update_new_project,
    ]
)


lbd_func_start_crawler = awslambda.Function(
    "LbdFuncStartCrawler",
    template=template,
    FunctionName=helper_fn_sub("{}-start-crawler", param_env_name),
    Code=aws_lambda_func_code,
    Layers=aws_lambda_layers,
    Handler="seedinvest_monitor.handlers.start_crawler.handler",
    MemorySize=128,
    Timeout=120,
    Runtime="python3.6",
    Environment=aws_lambda_environment,
    Role=iam_role_for_lbd_func.iam_role_arn,
)

event_rule_start_crawler = events.Rule(
    "EventRuleStartCrawler",
    template=template,
    State="ENABLED",
    ScheduleExpression=config.START_CRAWLER_RATE.get_value(),
    Targets=[
        events.Target(
            Id="EventRuleStartCrawler",
            Arn=lbd_func_start_crawler.lbd_func_arn,
        )
    ],
    DependsOn=[
        lbd_func_start_crawler,
    ]
)

lbd_permission_event_rule_start_crawler = awslambda.Permission(
    "LbdPermissionEventRuleStartCrawler",
    template=template,
    Action="lambda:InvokeFunction",
    FunctionName=lbd_func_start_crawler.lbd_func_arn,
    Principal="events.amazonaws.com",
    SourceArn=event_rule_start_crawler.event_rule_arn,
    DependsOn=[
        event_rule_start_crawler,
        lbd_func_start_crawler,
    ]
)


lbd_func_worker = awslambda.Function(
    "LbdFuncWorker",
    template=template,
    FunctionName=helper_fn_sub("{}-worker", param_env_name),
    Code=aws_lambda_func_code,
    Layers=aws_lambda_layers,
    Handler="seedinvest_monitor.handlers.worker.handler",
    MemorySize=128,
    Timeout=120,
    Runtime="python3.6",
    Environment=aws_lambda_environment,
    Role=iam_role_for_lbd_func.iam_role_arn,
)


sqs_event_source_mapping = awslambda.EventSourceMapping(
    "DownloaderLambdaEventMapping",
    template=template,
    BatchSize=10,
    Enabled=True,
    EventSourceArn=sqs_queue.sqs_queue_arn,
    FunctionName=Ref(lbd_func_worker),
    DependsOn=[
        sqs_queue,
        lbd_func_worker,
    ]
)


# --- post process ---
common_tags = {
    "ProjectName": config.PROJECT_NAME_SLUG.get_value(),
    "Stage": config.STAGE.get_value(),
    "EnvironmentName": config.ENVIRONMENT_NAME.get_value(),
}
template.create_resource_type_label()
template.update_tags(common_tags)
