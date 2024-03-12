from rest_framework.serializers import ModelSerializer


# // models 
from .models import AppConfigModel


class AppConfigModelSerializer(ModelSerializer):

        class Meta: 
            model = AppConfigModel
            fields = "__all__"

            