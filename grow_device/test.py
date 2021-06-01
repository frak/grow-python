#!/usr/bin/env python3
import logging
import sys
from time import sleep

from moisture import Moisture
from pump import Pump


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('grow.test')

    if len(sys.argv) < 4:
        logger.error('Usage: ./test.py {sensor_channel} {pump_channel} {power}')
        exit(1)

    sensor_channel = int(sys.argv[1])
    pump_channel = int(sys.argv[2])
    pump_power = float(sys.argv[3])
    moisture = Moisture(sensor_channel)
    pump = Pump(pump_channel)
    while True:
        logger.info(f"Moisture: {moisture.get_reading()}")
        pump.dose(pump_power, 10, True)
        sleep(10)


if __name__ == "__main__":
    main()
