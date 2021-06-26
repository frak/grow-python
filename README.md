# Grow Hat Fleet

This code is for managing any number of Raspberry Pi Zeros running the [Pimoroni Grow Kit](https://shop.pimoroni.com/products/grow) 
Hat with both moisture sensors and the [optional pump](https://shop.pimoroni.com/products/mini-pump) and
[piping](https://shop.pimoroni.com/products/8mm-silicone-tube-1m). At it's simplest you can 
manually set the dry and wet points for each of your sensors through the built-in screen with 
buttons. Most of the coded for this is lightly adapted from the example 
[code given by Pimoroni](https://github.com/pimoroni/grow-python).

For more than one unit, or simply to have remote control there is an optional admin 
server module which can provide each device with fresh configuration each time the sensors 
are checked. This server will also accept events pushed from the devices and certain actions 
can be triggered.

## Device

### Installation

Provisioning of devices is managed through a simple Ansible playbook. This text assumes you 
have a [working Ansible installation](https://docs.ansible.com/ansible/latest/installation_guide/index.html)
a [valid SSH keypair](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-2) 
set-up on your workstation and a freshly written [Raspberry Pi OS Lite image](https://www.raspberrypi.org/documentation/installation/installing-images/).

Enable SSH for the image and copy Wi-Fi configuration for first boot (default values for 
env vars shown here):

    $ WPA_CONF=~/Documents/wpa_supplicant.conf BOOT_PART=/Volumes/boot ansible-playbook provision/headless-boot.yaml -i localhost, --connection=local

Unmount the SD card and insert it into the Pi, then power up the device. Once it has booted,
secure the installation:

    $ ssh-copy-id pi@raspberrypi.local
    $ HOST_NAME=growpi ansible-playbook provision/harden-device.yaml -i raspberrypi.local, -u pi

The device will reboot. Now provision the Grow Pi software itself:

    $ ansible-playbook provision/device-provision.yaml -i growpi.local, -u pi

The device will reboot.

### Configuration via the built-in UI

The controls from the main view are as follows:

* `A` - cycle through the main screen and detailed view of each channel
* `B` - snooze the alarm
* `X` - configure either the global settings, or the settings for the selected channel

The full list of values that can be configured for each channel:

* `water_level` - The level at which auto-watering should be triggered (soil saturation from 0.0 to 1.0)
* `warn_level` - The level at which the alarm should be triggered (soil saturation from 0.0 to 1.0)
* `pump_speed` - The speed at which the pump should be run (from 0.0 low speed to 1.0 full speed)
* `pump_time` - The time that the pump should run for (in seconds)
* `auto_water` - Whether to run the attached pump (True to auto-water, False for manual watering)
* `wet_point` - Value for the sensor in saturated soil (in Hz)
* `dry_point` - Value for the sensor in totally dry soil (in Hz)

The list of global settings that can be changed:

* `alarm_enable` - Whether to enable the alarm
* `alarm_interval` - The interval at which the alarm should beep (in seconds)
* `watering_delay` - Delay between runs of the worker (in minutes)

