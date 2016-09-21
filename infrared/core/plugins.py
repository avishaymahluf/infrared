from ConfigParser import ConfigParser

import os

from infrared.core.utils import logger

LOG = logger.LOG


class InfraredPlugin(object):
    def __init__(self, name, root_dir, config):
        self.config = config
        self.root_dir = root_dir
        self.name = name

    @property
    def folders_config(self):
        return self.config['folders']

    @property
    def playbooks_config(self):
        return self.config['playbooks']

    def settings_folders(self):
        return [os.path.join(self.root_dir, sf)
                for sf in self.folders_config['settings'].split(os.pathsep)]

    @property
    def cleanup_playbook(self):
        return os.path.join(
            self.folders_config['playbooks'],
            self.playbooks_config['cleanup'])

    @property
    def main_playbook(self):
        return os.path.join(
            self.folders_config['playbooks'],
            self.playbooks_config['main'])

    @property
    def modules_dir(self):
        return self.folders_config['modules']

    @classmethod
    def from_config_file(cls, root_dir, config_file_name):
        """
        Creates plugins from the settings dict.
        """

        config_full_path = os.path.join(root_dir, config_file_name)
        config = ConfigParser()

        with open(config_full_path) as fd:
            config.readfp(fd)

        name = config.get('defaults', 'name')
        folders_config = dict(
            settings=_get_option(config, 'folders', 'settings', 'settings'),
            modules=_get_option(config, 'folders', 'modules', 'library'),
            roles=_get_option(config, 'folders', 'roles', 'roles'),
            playbooks=_get_option(config, 'folders', 'playbooks', 'playbooks')
        )

        playbooks_config = dict(
            main=_get_option(config, 'playbooks', 'main', name+".yml"),
            cleanup=_get_option(config, 'playbooks', 'cleanup', "cleanup.yml")
        )

        plugin_config = dict(
            folders=folders_config,
            playbooks=playbooks_config
        )

        return InfraredPlugin(name, root_dir, plugin_config)

    def subcommand_settings_files(self, subcommand_name, extension='.yml'):
        result = []
        for sf in self.settings_folders():
            settings_file = os.path.join(
                sf, subcommand_name, subcommand_name + extension)

        if os.path.exists(settings_file):
            result.append(settings_file)

        return result

    def __repr__(self):
        return repr(dict(
            name=self.name,
            root_dir=self.root_dir,
            config=self.config))


class PluginsInspector(object):
    PLUGINS_FOLDER = './plugins'
    CONFIG_FILE_NAME = 'infrared.cfg'

    @classmethod
    def get_plugin(cls, name):
        return next(
            (plg for plg in cls.iter_plugins() if plg.name == name), None)

    @classmethod
    def iter_plugins(cls):
        for dirpath, _, _ in os.walk(cls.PLUGINS_FOLDER):
            LOG.debug("Trying to load plugin from: '%s'", dirpath)
            config_path = os.path.join(dirpath, cls.CONFIG_FILE_NAME)
            if os.path.isfile(config_path):
                try:
                    yield InfraredPlugin.from_config_file(
                        dirpath, cls.CONFIG_FILE_NAME)
                except Exception as ex:
                    LOG.warn(
                        "Error loading plugin '%s': %s", dirpath, ex.message)


def _get_option(config, section, option, default):
    if config.has_option(section, option):
        value = config.get(section, option)
    else:
        value = default
    return value