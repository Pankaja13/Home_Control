from .models import Room, Sensor, Control
from functools import reduce
import logging
logger = logging.getLogger('django')


def regulate_temperature():
	for room in Room.objects.all():
		# Temperature Regulation
		sensors = Sensor.objects.filter(room__room_name=room.room_name, type=Sensor.TEMP)
		temperature_list = list(map(lambda sensor: float(sensor.get_value()), sensors))
		temperature = reduce(lambda total, value: total + value, temperature_list) / len(temperature_list)
		print(temperature_list, temperature)
		control = Control.objects.get(control_name="Main HVAC Control")
		if temperature > room.max_room_temp:
			control.set_state('Cool')
			logger.info("Cooling")
		elif temperature < room.min_room_temp:
			control.set_state('Off')
			logger.info("Turning Off")
		else:
			logger.info("Doing nothing!")
