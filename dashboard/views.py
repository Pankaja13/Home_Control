from django.http import HttpResponse, Http404
from django.shortcuts import render
from functools import reduce
from .models import Control, Room, Sensor
from .serializers import ControlSerializer
from rest_framework import generics


def index(request):
	return HttpResponse("Hello, world.")


def room_detail(request, room_name):
	try:
		room = Room.objects.filter(room_name=room_name).first()
		sensors = Sensor.objects.filter(room__room_name=room.room_name, type=Sensor.TEMP)
		sensor_data = {}
		for sensor in sensors:
			sensor_val = sensor.get_value()
			if sensor_val:
				sensor_data[sensor.sensor_name] = sensor.get_value()
		temperature_list = [float(sensor_data[x]) for x in sensor_data if x is not None]
		average_temperature = reduce(lambda total, value: total + value, temperature_list) / len(temperature_list)
	except Room.DoesNotExist:
		raise Http404("Poll does not exist")
	return render(request, 'dashboard/room_detail.html', {
		'room': room,
		'temperature_list': temperature_list,
		'average_temperature': average_temperature,
		'sensors': sensor_data
	})


class ControlList(generics.ListAPIView):
	queryset = Control.objects.all()
	serializer_class = ControlSerializer


class ControlDetail(generics.RetrieveUpdateAPIView):
	queryset = Control.objects.all()
	serializer_class = ControlSerializer
