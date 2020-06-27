from .models import Control
from rest_framework import serializers


class ControlSerializer(serializers.HyperlinkedModelSerializer):
	id = serializers.ReadOnlyField()
	control_name = serializers.CharField(required=False, read_only=True)
	room = serializers.StringRelatedField()

	class Meta:
		model = Control
		fields = ['id', 'control_name', 'current_state', 'room']

	def update(self, instance, validated_data):
		instance.set_state(validated_data.get('current_state'))
		return instance
