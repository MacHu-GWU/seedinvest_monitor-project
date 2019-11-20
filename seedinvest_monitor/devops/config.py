# -*- coding: utf-8 -*-

from configirl import ConfigClass, Constant, Derivable
from pathlib_mate import Path


class Config(ConfigClass):
    CONFIG_DIR = Path(__file__).parent.parent.parent.append_parts("config")

    METADATA = Constant(default=dict())

    PROJECT_NAME = Constant()
    PROJECT_NAME_SLUG = Derivable()

    @PROJECT_NAME_SLUG.getter
    def get_project_name_slug(self):
        return self.PROJECT_NAME.get_value().replace("_", "-")

    STAGE = Constant()  # example dev / test / prod

    ENVIRONMENT_NAME = Derivable()

    @ENVIRONMENT_NAME.getter
    def get_ENVIRONMENT_NAME(self):
        return "{}-{}".format(self.PROJECT_NAME_SLUG.get_value(self), self.STAGE.get_value())

    AWS_PROFILE_FOR_DEPLOY = Constant()
    AWS_PROFILE_FOR_PYTHON = Derivable()

    @AWS_PROFILE_FOR_PYTHON.getter
    def get_AWS_PROFILE_FOR_PYTHON(self):
        if self.is_aws_lambda_runtime():
            return None
        else:
            return self.AWS_PROFILE_FOR_DEPLOY.get_value()

    AWS_ACCOUNT_ID = Constant()
    AWS_REGION = Constant()

    S3_BUCKET_FOR_DEPLOY = Constant()

    DYNAMODB_TABLE_STARTUP = Derivable()

    @DYNAMODB_TABLE_STARTUP.getter
    def get_DYNAMODB_TABLE_STARTUP(self):
        return "{}-startup".format(self.ENVIRONMENT_NAME.get_value())

    SQS_QUEUE_URL = Derivable()

    @SQS_QUEUE_URL.getter
    def get_SQS_QUEUE_URL(self):
        return f"https://sqs.{self.AWS_REGION.get_value()}.amazonaws.com/{self.AWS_ACCOUNT_ID.get_value()}/{self.ENVIRONMENT_NAME.get_value()}-download-job"

    LAMBDA_CODE_S3_KEY = Derivable()

    @LAMBDA_CODE_S3_KEY.getter
    def get_LAMBDA_CODE_S3_KEY(self):
        from seedinvest_monitor._version import __version__
        return f"lambda/MacHu-GWU/seedinvest_monitor-project/{__version__}/source.zip"

    LAMBDA_LAYER_VERSION = Constant()
    LAMBDA_LAYERS = Derivable()

    @LAMBDA_LAYERS.getter
    def get_LAMBDA_LAYERS(self):
        return [
            f"arn:aws:lambda:us-east-1:110330507156:layer:seedinvest_monitor:{self.LAMBDA_LAYER_VERSION.get_value()}"
        ]

    UPDATE_NEW_PROJECT_RATE = Constant()

    HTML_UPDATE_INTERVAL_IN_SECONDS = Constant()

    START_CRAWLER_RATE = Constant()
