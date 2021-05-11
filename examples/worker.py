#!/usr/bin/env python3
import logging
import sys
import time

from channel import Channel
from config import Config


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('grow.worker')
    logger.info(f'Starting run at {time.strftime("%Y-%m-%d %H:%M:%S")}')
    config = Config()
    config.load(sys.argv[1])
    for i in range(1, 4):
        channel = Channel.channel_from_config(i, config.get_channel(i), logger)
        channel.update()
    logger.info(f'Finished run at {time.strftime("%Y-%m-%d %H:%M:%S")}')


if __name__ == "__main__":
    main()
