from rest_framework import serializers

from .models import Members,all_users_data

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Members
        fields = ("name", "host","cpu_usage")

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = all_users_data
        fields = '__all__'