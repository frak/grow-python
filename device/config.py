import pathlib
import yaml


class Config:
    def __init__(self):
        self.config = None
        self._last_save = ""

        self.channel_settings = [
            "enabled",
            "alarm",
            "warn_level",
            "wet_point",
            "dry_point",
            "auto_water",
            "pump_time",
            "pump_speed",
            "water_level",
        ]

        self.general_settings = [
            "alarm_enable",
            "alarm_interval",
            "watering_delay",
        ]

    def load(self, settings_file):
        settings_file = pathlib.Path(settings_file)

        if settings_file.is_file():
            try:
                self.config = yaml.safe_load(open(settings_file))
            except yaml.parser.ParserError as e:
                raise yaml.parser.ParserError(
                    "Error parsing settings file: {} ({})".format(settings_file, e)
                )

    def save(self, settings_file):
        settings_file = pathlib.Path(settings_file)

        dump = yaml.dump(self.config)

        if dump == self._last_save:
            return

        if settings_file.is_file():
            with open(settings_file, "w") as file:
                file.write(dump)

        self._last_save = dump

    def get_channel(self, channel_id):
        return self.config.get("channel{}".format(channel_id), {})

    def set(self, section, settings):
        if isinstance(settings, dict):
            self.config[section].update(settings)
        else:
            for key in self.channel_settings:
                value = getattr(settings, key, None)
                if value is not None:
                    self.config[section].update({key: value})

    def set_channel(self, channel):
        self.set("channel{}".format(channel.channel), channel)

    def get_general(self):
        return self.config.get("general", {})

    def set_general(self, settings):
        self.set("general", settings)

