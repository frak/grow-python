#!/usr/bin/env python3
import logging
import sys

import ltr559
import RPi.GPIO as GPIO
import ST7735

from PIL import Image

from channel import Channel
from config import Config
from views import *

FPS = 20
BUTTONS = [5, 6, 16, 24]
LABELS = ["A", "B", "X", "Y"]
DISPLAY_WIDTH = 160
DISPLAY_HEIGHT = 80


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('grow.ui')

    logger.info(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Set up the ST7735 SPI Display')
    display = ST7735.ST7735(
        port=0, cs=1, dc=9, backlight=12, rotation=270, spi_speed_hz=80000000
    )
    display.begin()

    logger.info(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Set up light sensor')
    light = ltr559.LTR559()

    logger.info(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Set up our canvas and prepare for drawing')
    image = Image.new("RGBA", (DISPLAY_WIDTH, DISPLAY_HEIGHT), color=(255, 255, 255))

    logger.info(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Loading config')
    config = Config()
    config_file = sys.argv[1]
    config.load(config_file)

    channels = []
    for i in range(1, 4):
        channels.append(Channel.channel_from_config(i, config.get_channel(i), logger))

    alarm = Alarm(image)
    alarm.update_from_yml(config.get_general())

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def handle_button(pin):
        index = BUTTONS.index(pin)
        label = LABELS[index]

        if label == "A":  # Select View
            view_controller.button_a()

        if label == "B":  # Sleep Alarm
            if not view_controller.button_b():
                if view_controller.home:
                    if alarm.sleeping():
                        alarm.cancel_sleep()
                    else:
                        alarm.sleep()

        if label == "X":
            view_controller.button_x()

        if label == "Y":
            view_controller.button_y()

    for pin in BUTTONS:
        GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=200)

    main_options = [
        {
            "title": "Alarm Interval",
            "prop": "interval",
            "inc": 1,
            "min": 1,
            "max": 60,
            "format": lambda value: f"{value:02.0f}sec",
            "object": alarm,
            "help": "Time between alarm beeps.",
        },
        {
            "title": "Alarm Enable",
            "prop": "enabled",
            "mode": "bool",
            "format": lambda value: "Yes" if value else "No",
            "object": alarm,
            "help": "Enable the piezo alarm beep.",
        },
    ]

    view_controller = ViewController([
        (MainView(image, channels=channels, alarm=alarm), SettingsView(image, options=main_options)),
        (DetailView(image, channel=channels[0]), ChannelEditView(image, channel=channels[0])),
        (DetailView(image, channel=channels[1]), ChannelEditView(image, channel=channels[1])),
        (DetailView(image, channel=channels[2]), ChannelEditView(image, channel=channels[2])),
    ])

    while True:
        for channel in channels:
            channel.update_from_yml(config.get_channel(channel.channel))
            if channel.alarm:
                alarm.trigger()

        alarm.update(light.get_lux() < 4.0)

        view_controller.update()
        view_controller.render()
        display.display(image.convert("RGB"))

        config.set_general({"alarm_enable": alarm.enabled, "alarm_interval": alarm.interval})
        config.save(config_file)

        time.sleep(1.0 / FPS)


if __name__ == "__main__":
    main()
