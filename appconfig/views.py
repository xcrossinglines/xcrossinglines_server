from rest_framework.authentication import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# .... models 
from rest_framework.authentication import get_user_model
from accounts.models import AccountProfile


# .. verify complete profile 
class VerifyCompleteProfileView(APIView): 


    def verifyCustomer(self, cUser):

        # define payload 
        payload = dict()

        print(isinstance(cUser, get_user_model()), "CHECL")

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

        # ... cUser 
        cUser = request.user
        # ... 
        payload = self.verifyCustomer(cUser)
        # ... return 
        return Response(payload, status=status.HTTP_200_OK)







