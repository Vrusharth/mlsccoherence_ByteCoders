from rest_framework import serializers
from instagram.models import Userprofile

from .models import *

class UserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = '__all__'