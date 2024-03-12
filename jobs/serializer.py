from rest_framework.serializers import ModelSerializer, SerializerMethodField, ImageField
from rest_framework import serializers

# ... models 
from rest_framework.authentication import get_user_model
from .models import Route, Job
from accounts.models import AccountProfile, Account

# ... external serializers 
from accounts.serializers import AccountProfileSerializer, AccountSerializer



# rotues serializer 
class RouteSerializer(ModelSerializer):

    class Meta:
        model = Route
        fields = "__all__"

# .. serializers 
class JobsGetCustomerSerializer(ModelSerializer):
    
    # .. customer 
    customer = serializers.SerializerMethodField(read_only = True)
    driver = serializers.SerializerMethodField(read_only = True)
    # routes = serializers.SerializerMethodField(read_only = True)
    routes = RouteSerializer(read_only = True,  many = True)

    # meta 
    class Meta: 
        model = Job
        # fields = "__all__"
        fields = [
            "id",
            "customer",
            "driver",
            "job_canceled",
            "job_completed",
            "job_invoice_sent",
            "job_cancellation_feedback_sent",
            "helpers",
            "floors",
            "shuttle",
            "referal_discount",
            "referal_code",
            "hear_about_us",
            "vehicle_size",
            "payment_option",
            "driver_note",
            "price_adjustment_justification",
            "base_fee",
            "mid_discount",
            "return_customer_discount",
            "distance",
            "routes",
            "job_date",
            "job_time",
            "created_at",
            "updated_at",
            "amount_due",
            "give_extra_discount",
            "set_price_adjustment",
            "extra_discount",
            "price_adjustment",
        ]
        
    # ... we need to get full customer profile 
    def get_customer(self, obj):
        
        # check booking instance 
        if(isinstance(obj.customer, get_user_model())):
            
            # ... lets find the profile 
            aProfile = AccountProfile\
                        .objects.get(
                        account = obj.customer)
            
            # ... seralize this 
            sAccountProfile = AccountProfileSerializer(aProfile, many = False)
            sAccount = AccountSerializer(obj.customer, many = False)
            
            # // 
            sAccountJson = sAccount.data
            sAccountJson["account-profile"] = sAccountProfile.data
            
            #//
            return sAccountJson 
        
        return None
    
    # ... we need to get full customer profile 
    def get_driver(self, obj):

        # check booking instance 
        if(isinstance(obj.driver, get_user_model())):
            
            # ... lets find the profile 
            aProfile = AccountProfile\
                        .objects.get(
                        account = obj.customer)
            
            # ... seralize this 
            sAccountProfile = AccountProfileSerializer(aProfile, many = False)
            sAccount = AccountSerializer(obj.customer, many = False)
            
            # // 
            sAccountJson = sAccount.data
            sAccountJson["account-profile"] = sAccountProfile.data
            
            #//
            return sAccountJson 
        
        return None
    
    # get routes 
    # def get_routes(self, obj):
        
    #     # ---simplified version
    #     return [{
    #              "id": a.id,
    #              "lat": a.lat, 
    #              "lng": a.lng, 
    #              "description": a.description,
    #              "route_name": a.route_name} 
    #                         for a in obj.routes.all()]
        

# ... create Serializer 
class JobCreateSerializer(ModelSerializer):
    
    class Meta: 
        model = Job
        fields = (
            "customer",
            "helpers",
            "floors",
            "shuttle",
            "vehicle_size",
            "payment_option",
            "driver_note",
            "base_fee",
            "referal_code",
            "hear_about_us",
            "referal_discount",
            "mid_discount",
            "return_customer_discount",
            "distance",
            "job_canceled",
            "job_invoice_sent",
            "job_date",
            "job_time",
            )
        

class GenenerateQuoteSerializer(ModelSerializer):
    pass
        
        
# ... Update Serializer 
class JobUpdateSerializer(ModelSerializer):
    
    class Meta: 
        model = Job
        fields = (
            "customer",
            "helpers",
            "floors",
            "shuttle",
            "vehicle_size",
            "payment_option",
            "driver_note",
            "base_fee",
            "mid_discount",
            "return_customer_discount",
            "job_cancellation_feedback_sent",
            "distance",
            "job_canceled",
            "job_invoice_sent",
            "job_date",
            "job_time",
     
        )