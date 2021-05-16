import time
import RPi.GPIO as GPIO
from history import History

MOISTURE_1_PIN = 23
MOISTURE_2_PIN = 8
MOISTURE_3_PIN = 25
MOISTURE_INT_PIN = 4


class Moisture(object):
    """Grow moisture sensor driver."""

    def __init__(self, channel=1):
        """Create a new moisture sensor.

        Uses an interrupt to count pulses on the GPIO pin corresponding to the selected channel.

        The moisture reading is given as pulses per second.

        :param channel: One of 1, 2 or 3. 4 can optionally be used to set up a sensor on the Int pin (BCM4)

        """
        self._gpio_pin = [MOISTURE_1_PIN, MOISTURE_2_PIN, MOISTURE_3_PIN, MOISTURE_INT_PIN][channel - 1]
        self._history = History(f"/var/lib/grow-monitor/channel-{channel}.yml")

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._gpio_pin, GPIO.IN)

        self._count = 0
        self._reading = 0
        self._last_pulse = time.time()
        self._wet_point = 0.7
        self._dry_point = 27.6
        self._time_last_reading = time.time()
        self._readings = []

        self._time_start = time.time()

    def get_reading(self):
        self._readings = []
        self._get_readings()
        self._reading = self._average_readings()
        self._history.add_reading(self._reading)
        return max(0.0, min(1.0, self.saturation))

    def _event_handler(self, pin):
        self._count += 1
        self._last_pulse = time.time()
        if self._time_elapsed >= 1.0:
            self._readings.append(self._count / self._time_elapsed)
            self._count = 0
            self._time_last_reading = time.time()

    def _get_readings(self):
        try:
            GPIO.add_event_detect(self._gpio_pin, GPIO.RISING, callback=self._event_handler, bouncetime=1)
            time.sleep(3.1)
            GPIO.remove_event_detect(self._gpio_pin)
        except RuntimeError as e:
            if self._gpio_pin == 8:
                raise RuntimeError("""Unable to set up edge detection on BCM8.

Please ensure you add the following to /boot/config.txt and reboot:

dtoverlay=spi0-cs,cs0_pin=14 # Re-assign CS0 from BCM 8 so that Grow can use it

""")
            else:
                raise e

    def _average_readings(self):
        return sum(self._readings) / len(self._readings)

    @property
    def history(self):
        history = []

        for moisture in self._history.get_readings():
            saturation = float(moisture - self._dry_point) / self.range
            saturation = round(saturation, 3)
            history.append(max(0.0, min(1.0, saturation)))

        return history

    @property
    def _time_elapsed(self):
        return time.time() - self._time_last_reading

    def set_wet_point(self, value=None):
        """Set the sensor wet point.

        This is the watered, wet state of your soil.

        It should be set shortly after watering. Leave ~5 mins for moisture to permeate.

        :param value: Wet point value to set in pulses/sec, leave as None to set the last sensor reading.

        """
        self._wet_point = value if value is not None else self._reading

    def set_dry_point(self, value=None):
        """Set the sensor dry point.

        This is the unwatered, dry state of your soil.

        It should be set when the soil is dry to the touch.

        :param value: Dry point value to set in pulses/sec, leave as None to set the last sensor reading.

        """
        self._dry_point = value if value is not None else self._reading

    @property
    def moisture(self):
        """Return the raw moisture level.

        The value returned is the pulses/sec read from the soil moisture sensor.

        This value is inversely proportional to the amount of moisture.

        Full immersion in water is approximately 50 pulses/sec.

        Fully dry (in air) is approximately 900 pulses/sec.

        """
        return self._reading

    @property
    def range(self):
        """Return the range sensor range (wet - dry points)."""
        return self._wet_point - self._dry_point

    @property
    def saturation(self):
        """Return saturation as a float from 0.0 to 1.0.

        This value is calculated using the wet and dry points.

        """
        saturation = float(self.moisture - self._dry_point) / self.range
        saturation = round(saturation, 3)
        return max(0.0, min(1.0, saturation))
