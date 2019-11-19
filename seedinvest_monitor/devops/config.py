# -*- coding: utf-8 -*-

from pathlib_mate import Path
from configirl import ConfigClass, Constant, Derivable


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

    AWS_PROFILE = Constant()
    AWS_PROFILE_FOR_PYTHON = Derivable()

    @AWS_PROFILE_FOR_PYTHON.getter
    def get_AWS_PROFILE_FOR_PYTHON(self):
        if self.is_aws_lambda_runtime():
            return None
        else:
            return self.AWS_PROFILE.get_value()

    S3_BUCKET_FOR_DEPLOY = Constant()

    DYNAMODB_TABLE_STARTUP = Derivable()

    @DYNAMODB_TABLE_STARTUP.getter
    def get_DYNAMODB_TABLE_STARTUP(self):
        return "{}-startup".format(self.ENVIRONMENT_NAME.get_value())



