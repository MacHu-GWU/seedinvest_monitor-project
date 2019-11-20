# -*- coding: utf-8 -*-

from superjson import json
from pathlib_mate import Path
from seedinvest_monitor.devops.config import Config

config = Config()
if config.is_aws_lambda_runtime():
    config.update_from_env_var(prefix="SEEDINVEST_MONITOR_")
else:
    config.update(json.load(Path(config.CONFIG_DIR, "00-config-shared.json").abspath, verbose=False))
    config.update(json.load(Path(config.CONFIG_DIR, "01-config-dev.json").abspath, verbose=False))
    config.dump_python_json_config_file()
    config.dump_cloudformation_json_config_file()


