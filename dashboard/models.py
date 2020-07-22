from django.db import models
from django_mysql.models import ListCharField
import requests


# Create your models here.
class Room(models.Model):
	room_name = models.CharField(max_length=50)
	min_room_temp = models.FloatField(null=True, blank=True)
	max_room_temp = models.FloatField(null=True, blank=True)
	current_temp = models.FloatField(null=True, blank=True)
	current_temp_timestamp = models.DateTimeField(null=True, blank=True)
	enabled = models.BooleanField(default=False, blank=True)

	def __repr__(self):
		return self.room_name

	def __str__(self):
		return self.room_name


class Control(models.Model):
	control_name = models.CharField(max_length=50)
	url = models.CharField(max_length=200)
	current_state = models.CharField(max_length=10, null=True, blank=True)
	room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
	states = ListCharField(
		base_field=models.CharField(max_length=10),
		size=5,
		max_length=(5 * 11),  # 6 * 10 character nominals, plus commas
		null=True,
		blank=True
	)
	state_values = ListCharField(
		base_field=models.IntegerField(),
		size=5,
		max_length=30,
		null=True,
		blank=True
	)

	def __str__(self):
		return self.control_name

	def set_state(self, state):
		if state == self.current_state:
			return
		try:
			index = self.states.index(state)
		except ValueError:
			raise ValueError('Invalid State')
		target_value = self.state_values[index]
		command_string = 'position=' + str(target_value)
		response = requests.get(url=self.url + '?' + command_string, timeout=5)
		if not str(target_value) in response.text:
			raise ConnectionError('Value not set')
		self.current_state = state
		# todo: add state change time
		self.save()


class Sensor(models.Model):
	TEMP = 'temp'
	HUM = 'hum'
	TYPES = [
		(TEMP, 'Temperature'),
		(HUM, 'Humidity')
	]

	sensor_name = models.CharField(max_length=50)
	url = models.CharField(max_length=200)
	units = models.CharField(max_length=10)
	room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
	type = models.CharField(max_length=20, choices=TYPES, default=TEMP)

	def __str__(self):
		return self.sensor_name

	def get_value(self):
		try:
			value = None
			for _ in range(3):
				value = requests.get(url=self.url, timeout=5).text
			return value
		except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
			return None
