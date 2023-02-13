from rest_framework import serializers
from .models import SimpleRandom

class SimpleRandomSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleRandom
        fields = '__all__'