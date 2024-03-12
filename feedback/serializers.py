from rest_framework.serializers import ModelSerializer, SerializerMethodField, ImageField
from rest_framework import serializers

# ... import models 
from .models import FeedBack


# ... 
class FeedBackSerializer(ModelSerializer): 

    class Meta: 

        model = FeedBack
        fields = "__all__"
        # fields = [
            
        
        # ]