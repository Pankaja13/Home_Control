from django.http import HttpResponse
from .models import Control
from .serializers import ControlSerializer
from rest_framework import generics


def index(request):
	return HttpResponse("Hello, world.")


class ControlList(generics.ListAPIView):
	queryset = Control.objects.all()
	serializer_class = ControlSerializer


class ControlDetail(generics.RetrieveUpdateAPIView):
	queryset = Control.objects.all()
	serializer_class = ControlSerializer
