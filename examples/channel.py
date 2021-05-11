import math
import time
from pathlib import Path
from os.path import exists, getmtime

from moisture import Moisture
from pump import Pump


class Channel:
    colors = [
        (31, 137, 251),
        (99, 255, 124),
        (254, 219, 82),
        (247, 0, 63)
    ]

    def __init__(
            self,
            display_channel,
            sensor_channel,
            pump_channel,
            logger,
            title=None,
            water_level=0.5,
            warn_level=0.5,
            pump_speed=0.5,
            pump_time=0.2,
            watering_delay=60,
            wet_point=0.7,
            dry_point=26.7,
            icon=None,
            auto_water=False,
            enabled=False,
    ):
        self._run_file = f"/var/run/grow-{display_channel}-{sensor_channel}-{pump_channel}"

        self.channel = display_channel
        self.sensor = Moisture(sensor_channel, False)
        self.pump = Pump(pump_channel)
        self.logger = logger
        self.water_level = water_level
        self.warn_level = warn_level
        self.auto_water = auto_water
        self.pump_speed = pump_speed
        self.pump_time = pump_time
        self.watering_delay = watering_delay
        self._wet_point = wet_point
        self._dry_point = dry_point
        self.icon = icon
        self._enabled = enabled
        self.alarm = False
        self.title = f"Channel {display_channel}" if title is None else title


        self.sensor.set_wet_point(wet_point)
        self.sensor.set_dry_point(dry_point)

    @classmethod
    def channel_from_config(cls, number, config, logger):
        out = Channel(number, number, number, logger)
        out.update_from_yml(config)
        return out

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        self._enabled = enabled

    @property
    def wet_point(self):
        return self._wet_point

    @property
    def dry_point(self):
        return self._dry_point

    @property
    def last_dose(self):
        if not exists(self._run_file):
            self.set_last_dose()
        return getmtime(self._run_file)

    def set_last_dose(self):
        Path(self._run_file).touch()

    @wet_point.setter
    def wet_point(self, wet_point):
        self._wet_point = wet_point
        self.sensor.set_wet_point(wet_point)

    @dry_point.setter
    def dry_point(self, dry_point):
        self._dry_point = dry_point
        self.sensor.set_dry_point(dry_point)

    def indicator_color(self, value):
        value = 1.0 - value

        if value == 1.0:
            return self.colors[-1]
        if value == 0.0:
            return self.colors[0]

        value *= len(self.colors) - 1
        a = int(math.floor(value))
        b = a + 1
        blend = float(value - a)

        r, g, b = [int(((self.colors[b][i] - self.colors[a][i]) * blend) + self.colors[a][i]) for i in range(3)]

        return r, g, b

    def update_from_yml(self, config):
        if config is not None:
            self.pump_speed = config.get("pump_speed", self.pump_speed)
            self.pump_time = config.get("pump_time", self.pump_time)
            self.warn_level = config.get("warn_level", self.warn_level)
            self.water_level = config.get("water_level", self.water_level)
            self.watering_delay = config.get("watering_delay", self.watering_delay)
            self.auto_water = config.get("auto_water", self.auto_water)
            self.enabled = config.get("enabled", self.enabled)
            self.wet_point = config.get("wet_point", self.wet_point)
            self.dry_point = config.get("dry_point", self.dry_point)

        pass

    def __str__(self):
        return """Channel: {channel}
Enabled: {enabled}
Alarm level: {warn_level}
Auto water: {auto_water}
Water level: {water_level}
Pump speed: {pump_speed}
Pump time: {pump_time}
Delay: {watering_delay}
Wet point: {wet_point}
Dry point: {dry_point}
""".format(
            channel=self.channel,
            enabled=self.enabled,
            warn_level=self.warn_level,
            auto_water=self.auto_water,
            water_level=self.water_level,
            pump_speed=self.pump_speed,
            pump_time=self.pump_time,
            watering_delay=self.watering_delay,
            wet_point=self.wet_point,
            dry_point=self.dry_point,
        )

    def water(self):
        if not self.auto_water:
            return False
        if time.time() - self.last_dose > self.watering_delay:
            self.pump.dose(self.pump_speed, self.pump_time, blocking=False)
            self.set_last_dose()
            return True
        return False

    def render(self, image, font):
        pass

    def update(self):
        if not self.enabled:
            self.logger.info(
                f"Channel {self.channel} is disabled"
            )
            return
        # sat = self.sensor.saturation
        sat = self.sensor.get_reading()
        if sat < self.water_level:
            if self.water():
                self.logger.info(
                    "Watering Channel: {} - rate {:.2f} for {:.2f}sec".format(
                        self.channel, self.pump_speed, self.pump_time
                    )
                )
        else:
            self.logger.info(
                f"Channel {self.channel} does not need watering, saturation {sat} water level {self.water_level}"
            )
        if sat < self.warn_level:
            if not self.alarm:
                self.logger.warning(
                    "Alarm on Channel: {} - saturation is {:.2f}% (warn level {:.2f}%)".format(
                        self.channel, sat * 100, self.warn_level * 100
                    )
                )
            self.alarm = True
        else:
            self.alarm = False
