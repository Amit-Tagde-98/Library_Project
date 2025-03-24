from rest_framework import serializers
from book.models import *
from datetime import datetime, timezone, timedelta


class UserAuthSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        fields = '__all__'

class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'