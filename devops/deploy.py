# -*- coding: utf-8 -*-

from seedinvest_monitor.cf import template, config
from seedinvest_monitor.boto_ses import boto_ses
from troposphere_mate import StackManager

stack_manager = StackManager(
    boto_ses=boto_ses,
    cft_bucket=config.S3_BUCKET_FOR_DEPLOY.get_value(),
)

config_data = config.to_cloudformation_config_data()
stack_parameters = {
    key: config_data[key]
    for key in template.parameters
}

stack_manager.deploy(
    template,
    stack_name=config.ENVIRONMENT_NAME.get_value(),
    stack_parameters=stack_parameters,
    include_iam=True,
)
