"""
Load config file and optional .env (which may contain secrets that should not go in config)

"""

from . import parser as cp
from . import loader as cl
from .. import logger as pml


def load_configuration(config_file, dotenv_file=None, include_os_env=True):
    """
    Read configuration files and return dict of settings

    :param config_file: str
    :param dotenv_file: str | None
    :param include_os_env: bool
    :return:

    """
    config = cp.parse_config(config_file, dotenv_file, include_os_env)
    logger = configure_logger(config)
    monitors = cl.load_monitors(config)
    actions = cl.load_actions(config)

    config['monitors'] = monitors
    config['actions'] = actions
    config = configure_listeners(config)

    return config


def configure_listeners(config):
    """
    Attach listeners (actions) to monitors

    :param config:
    :return:
    """
    listeners = config.get('listeners', {})
    monitors = config.get('monitors', {})
    actions = config.get('actions', {})
    logger = pml.get_logger()

    if not listeners:
        raise ValueError("no listeners found in configuration")

    for listener_name, listener_info in listeners.items():
        monitor_name = listener_info['monitor']
        action_name = listener_info['action']

        if monitor_name not in monitors:
            raise ValueError("monitor {} not found "
                             "(for listener {})".format(monitor_name, listener_name))

        if action_name not in actions:
            raise ValueError("action {} not found "
                             "(for listener {})".format(action_name, listener_name))

        monitor = monitors[monitor_name]
        action = actions[action_name]

        monitor.add_listener(listener_name, action)
        logger.debug(f"adding action {action} to monitor {monitor}")

    return config


def configure_logger(config: dict):
    """
    Set up application-wide logger

    """
    general = config.get("general")
    log_level = general.get("log_level", "ERROR")
    log_file = general.get("log_file", None)
    logger = pml.set_logger(log_level, log_file)

    return logger



