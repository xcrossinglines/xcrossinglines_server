
# .. 3rd party packages
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ImageField
from rest_framework import serializers
from rest_framework.authentication import get_user_model

#.. models 
from .models import Account, AccountProfile

#... 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# serializers 
class SignupSerializer(ModelSerializer):
    
    #// create meta class 
    class Meta: 
        model= Account
        fields = ('email', 
                'f_name', 
                's_name',
                'm_number', 
                'password', 
                'customer', 
                'driver', 
                'is_staff',
                'is_corperate',)
        extra_kwargs = {'password': {'write_only': True}}
        
    #// create password 
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

    
# new account serializer 
class AccountSerializer(ModelSerializer):

    #// serializers
    profile = SerializerMethodField(read_only = True)

    # // meta
    class Meta: 
        model = Account
        fields = [
            "id",
            "profile",
            "email",
            "f_name",
            "s_name",
            "m_number",
            "is_active",
            "is_staff",
            "is_superuser",
            "customer",
            "is_corperate",
            "register_method",
            "driver",
            "verified",
            "d_joined",
            "d_updated",
            "did_accept_ts_cs",
            "groups",
            "user_permissions",
            "last_login",
       
        ]

    #//get full profile 
    def get_profile(self, obj):
        getProfile = AccountProfile.objects.get(account = obj)
        sProfile = AccountProfileSerializer(getProfile)
        return sProfile.data
    
        
        
class AccountUpdateSerializer(ModelSerializer):
    
    class Meta:
        model = Account
        fields = ['f_name', 's_name', 'm_number',]

    # ... 
class AccountProfileSerializer(ModelSerializer):
    
    class Meta:
        model = AccountProfile
        fields = "__all__"  

        
#// custom JWT TOKEN SERIALIZER
class SigninTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, account):
        # ...
        token = super().get_token(account)
        _type = type(None)
        # ///
        aProfile = AccountProfile\
                        .objects\
                        .get(account = account)
                        
        #.. retrieve refferal code 
        referal_code = "None"
        if(isinstance(aProfile, AccountProfile)):
            referal_code = aProfile.referal_code
            
        #// here we add 
        token["f_name"] = account.f_name
        token["s_name"] = account.s_name
        token["referal_code"] = referal_code
        token["driver"] = account.driver
        token["is_staff"] = account.is_staff
        token["customer"] = account.customer
        token["is_corperate"] = account.is_corperate
        # token['image'] = aProfile.image.url
    
        return token 
            

    
