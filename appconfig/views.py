from rest_framework.authentication import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# .... models 
from rest_framework.authentication import get_user_model
from accounts.models import AccountProfile
from .models import AppConfigModel
from .serializers import AppConfigModelSerializer


# .. verify complete profile 
class VerifyCompleteProfileView(APIView): 

    permission_classes = [AllowAny,]  
 
    def verifyCustomer(self, cUser, shutdown_website):

        # define payload 
        payload = dict()

        # ..payload["shutdown_website"] = shutdown_website
        payload["shutdown_website"] = shutdown_website

        # .. check if cUser is type Usermodel 
        if(isinstance(cUser, get_user_model())):
            # .. retrieve 
            firstName = cUser.f_name
            surname = cUser.s_name
            mobileNumber = cUser.m_number

            #.. compaire
            _noneType = type(None)
            if(isinstance(firstName, _noneType) or 
                isinstance(surname, _noneType) or 
                    isinstance(mobileNumber, _noneType)):
                
                # .. define payload 
                payload["isLoggedIn"] = True
                payload["pComplete"] = False
                payload["msg"] = "Your profile is incomplete, please complete your profile."
                
                # return 
                return payload
            
            #.. otherwise 
            if(len(firstName) <= 0 or 
                    len(surname)<=0 or 
                        len(mobileNumber)<=0):
                
                # .. define payload 
                payload["isLoggedIn"] = True
                payload["pComplete"] = False
                payload["msg"] = "Your profile is incomplete, please complete your profile."
                #// return 
                return payload 
            
            #.. otherwise 
            payload["isLoggedIn"] = True
            payload["pComplete"] = True
            payload["msg"] = "Awesome! your profile is complete."

            # ..return 
            return payload

        # .. otherwise customer if not logged in 
        payload["isLoggedIn"] = False 
        payload["pComplete"] = False 
        payload["msg"] = "Your profile is incomplete, please complete your profile." 

        #.. return 
        return payload

    def get(self, request, *args, **kwargs):

        # // shutdown website 
        shutdown_website = False
        # ... fetch object 
        obj = AppConfigModel\
                .objects\
                .all()\
                .order_by("-created_at")\
                .first()
        
        if(isinstance(obj, AppConfigModel)):
            shutdown_website = obj.shutdown_website

        # ... 
        payload = self.verifyCustomer(request.user, shutdown_website)
        # ... return 
        return Response(payload, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):

        # ... payload 
        payload = dict()

        super_user = request.data.get("super_user")
        command = request.data.get("shutdown_website")
        # first 
        if(super_user is None or command is None):
            # // response 
            payload["msg"] = "customer id command cannot be null"
            return Response(payload, status=status.HTTP_401_UNAUTHORIZED)
            
        # .. get object or 404
        c_obj = get_object_or_404(get_user_model(), pk = super_user)
     
        # .. verify 
        if(isinstance(c_obj, get_user_model())):

            # .. check if staff 
            if(c_obj.is_superuser):
                # ... 
                appSerializer = AppConfigModelSerializer(data=request.data)
                if(appSerializer.is_valid(raise_exception=True)):
                    appSerializer.save()
                    return Response({"msg": "successfully created"}, status= status.HTTP_200_OK)
                return Response(appSerializer.errors, status = status.HTTP_400_BAD_REQUEST)
            # .. respod
            return Response({"msg": "Unauthorized"}, status=401)

        # .. respod
        return Response({"msg": "Error no objs found"}, status=400)









