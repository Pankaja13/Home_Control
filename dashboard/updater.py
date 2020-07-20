from .models import Room, Sensor, Control
from functools import reduce
from django_cron import CronJobBase, Schedule
import logging
logger = logging.getLogger('dashboard')


class Regulate(CronJobBase):
	schedule = Schedule(run_every_mins=1)
	code = 'dashboard.Regulate'

	@staticmethod
	def do():
		for room in Room.objects.all():
			# Temperature Regulation
			sensors = Sensor.objects.filter(room__room_name=room.room_name, type=Sensor.TEMP)
			temperature_list = [float(x) for x in map(lambda sensor: sensor.get_value(), sensors) if x is not None]
			temperature = reduce(lambda total, value: total + value, temperature_list) / len(temperature_list)
			logger.info(room.room_name + str(temperature_list))
			control = Control.objects.get(control_name="Main HVAC Control")
			if temperature > room.max_room_temp:
				control.set_state('Cool')
				logger.info("Cooling")
			elif temperature < room.min_room_temp:
				control.set_state('Off')
				logger.info("Turning Off")
			else:
				logger.info("Doing nothing!")
