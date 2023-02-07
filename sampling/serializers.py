from rest_framework import serializers
from .models import State, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

    #def to_representation(self, instance):
    #    representation = super().to_representation(instance)
    #    representation['options'] = OptionSerializer(instance.options.all(), many=True).data
    #    return representation