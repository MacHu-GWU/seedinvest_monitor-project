# -*- coding: utf-8 -*-

import boto3
from seedinvest_monitor.devops.config_init import config

boto_ses = boto3.Session(profile_name=config.AWS_PROFILE_FOR_PYTHON.get_value())
