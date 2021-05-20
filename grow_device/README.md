# Grow HAT Mini

Designed as a tiny valet for your plants, Grow HAT mini will monitor the soil moiture for up to 3 plants, water them with tiny pumps, and show you their health on its small but informative screen. Learn more - https://shop.pimoroni.com/products/grow

[![Build Status](https://travis-ci.com/pimoroni/enviroplus-python.svg?branch=master)](https://travis-ci.com/pimoroni/grow-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/grow-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/grow-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/enviroplus.svg)](https://pypi.python.org/pypi/growhat)
[![Python Versions](https://img.shields.io/pypi/pyversions/enviroplus.svg)](https://pypi.python.org/pypi/growhat)

# Installing

You're best using the "One-line" install method.

## One-line (Installs from GitHub)

```
curl -sSL https://get.pimoroni.com/grow | bash
```

**Note** report issues with one-line installer here: https://github.com/pimoroni/get

## Or... Install and configure dependencies from GitHub:

* `git clone https://github.com/pimoroni/grow-python`
* `cd grow-python`
* `sudo ./install.sh`

**Note** Raspbian Lite users may first need to install git: `sudo apt install git`

## Or... Install from PyPi and configure manually:

* Install dependencies:

```
sudo apt install python3-setuptools python3-pip python3-yaml python3-smbus python3-pil python3-spidev python3-rpi.gpio
```

* Run `sudo pip3 install growhat`

**Note** this wont perform any of the required configuration changes on your Pi, you may additionally need to:

* Enable i2c: `sudo raspi-config nonint do_i2c 0`
* Enable SPI: `sudo raspi-config nonint do_spi 0`
* Add the following to `/boot/config.txt`: `dtoverlay=spi0-cs,cs0_pin=14`

# Monitoring Your Plants

The example `monitor.py` monitors the moisture level of your soil and sounds an alarm when it drops below a defined threshold.

It's configured using `settings.yml`. Your settings for monitoring will look something like this:

```yaml
channel1:
        warn_level: 0.2
channel2:
        warn_level: 0.2
channel3:
        warn_level: 0.2
general:
        alarm_enable: True
        alarm_interval: 1.0
```

`monitor.py` includes a main view showing the moisture status of each channel and the level beyond which the alarm will sound.

The controls from the main view are as follows:

* `A` - cycle through the main screen and each channel
* `B` - snooze the alarm
* `X` - configure global settings or the selected channel

The warning moisture level can be configured for each channel, along with the Wet and Dry points that store the frequency expected from the sensor when soil is fully wet/dry.

## Watering

If you've got pumps attached to Grow and want to automatically water your plants, you'll need some extra configuration options.

See [Channel Settings](#channel-settings) and [General Settings](#general-settings) for more information on what these do.

```yaml
channel1:
        water_level: 0.8
        warn_level: 0.2
        pump_speed: 0.7
        pump_time: 0.7
        wet_point: 0.7
        dry_point: 27.6
        auto_water: True
        watering_delay: 60
channel2:
        water_level: 0.8
        warn_level: 0.2
        pump_speed: 0.7
        pump_time: 0.7
        wet_point: 0.7
        dry_point: 27.6
        auto_water: True
        watering_delay: 60
channel3:
        water_level: 0.8
        warn_level: 0.2
        pump_speed: 0.7
        pump_time: 0.7
        wet_point: 0.7
        dry_point: 27.6
        auto_water: True
        watering_delay: 60
general:
        alarm_enable: True
        alarm_interval: 1.0
```

## Channel Settings

Grow has three channels which are separated into the sections `channel1`, `channel2` and `channel3`, each of these sections has the following configuration options:

* `water_level` - The level at which auto-watering should be triggered (soil saturation from 0.0 to 1.0)
* `warn_level` - The level at which the alarm should be triggered (soil saturation from 0.0 to 1.0)
* `pump_speed` - The speed at which the pump should be run (from 0.0 low speed to 1.0 full speed)
* `pump_time` - The time that the pump should run for (in seconds)
* `auto_water` - Whether to run the attached pump (True to auto-water, False for manual watering)
* `wet_point` - Value for the sensor in saturated soil (in Hz)
* `dry_point` - Value for the sensor in totally dry soil (in Hz)
* `watering_delay` - Delay between waterings (in seconds)

## General Settings

An additional `general` section can be used for global settings:

* `alarm_enable` - Whether to enable the alarm
* `alarm_interval` - The interval at which the alarm should beep (in seconds)

## Help & Support

* GPIO Pinout - https://pinout.xyz/pinout/grow_hat_mini
* Support forums - http://forums.pimoroni.com/c/support
* Discord - https://discord.gg/hr93ByC
