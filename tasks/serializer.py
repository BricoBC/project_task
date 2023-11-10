from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        #Se indica cuales campos se quiere mandar al front.
        # fields = ('id', 'title', 'description', 'done')
        fields = '__all__'