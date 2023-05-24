from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from rest_framework.authentication import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.views import TokenObtainPairView

#// serializers 
from .serializers import (SignupSerializer, 
                          AccountSerializer, 
                          AccountUpdateSerializer,
                          SigninTokenObtainPairSerializer,)

# // models 
from .models import AccountProfile

# ... Register/Login with google 
class GoogleRegisterLoginAPIView(APIView):
    
    #.. set permissions 
    permission_classes = [AllowAny] 
        
    #.. 
    def post(self, request, *args, **kwargs):
        
        # .. declare payload 
        payload = dict()
        
        #// first name 
        fName = request.data.get("f_name")
        SName = request.data.get("s_name")
        Email = request.data.get("email")
        Password = request.data.get("password")
        
        # .. verify 
        _type = type(None)
        if(isinstance(fName, _type) or isinstance(SName, _type) or
           isinstance(Email, _type) or isinstance(Password, _type)):
            
            # ... set payload 
            payload["msg"] = "first name, last name, email and password cannot be null"             
            # ... response 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        # ... verify that customer exist or not Account Exists 
        cAccount = get_user_model()\
                    .objects\
                    .filter(email = Email)\
                    .first()
                    
        # ... check type
        if(isinstance(cAccount, get_user_model())):
           
        
            # .. generate token 
            refreshT = RefreshToken.for_user(cAccount)

            # .. add extra fields 
            refreshT["f_name"] = cAccount.f_name
            refreshT["s_name"] = cAccount.s_name
            refreshT["driver"] = cAccount.driver
            refreshT["is_staff"] = cAccount.is_staff

            # .. set payload 
            payload["msg"] = "Signed In"
            payload["refresh"] = str(refreshT),
            payload["access"] = str(refreshT.access_token)
            
            # ... return response 
            return Response(payload, status=status.HTTP_200_OK)
            
        # .. otherwise everything is fine
        signup_serializer = SignupSerializer(data=request.data)
        if(signup_serializer.is_valid(raise_exception=True)):
            
            # ... new google account 
            nAccount = signup_serializer.save()
            
            # ... double check that all is fine
            if(isinstance(nAccount, get_user_model())):
                
               
                # .. generate token 
                refreshT = RefreshToken.for_user(nAccount)
            
                # .. add extra fields 
                refreshT["f_name"] = nAccount.f_name
                refreshT["s_name"] = nAccount.s_name
                refreshT["driver"] = nAccount.driver
                refreshT["is_staff"] = nAccount.is_staff
                
                # .. set payload 
                payload["msg"] = "Google Account Created"
                payload["refresh"] = str(refreshT),
                payload["access"] = str(refreshT.access_token)
                
                # ... return response
                return Response(payload, status=status.HTTP_200_OK)
        
        # .. otherwise error 
        return Response(signup_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
     
# .. create new account/register/signup 
class AccountCreateAPIVIEW(APIView):
    
    #... set permissions 
    permission_classes = [AllowAny]
    
    #... post 
    def post(self, request, *args, **kwargs):
        
        #... payload 
        payload = dict()
        
        #... serializer
        signup_serializer = SignupSerializer(data=request.data)
        if(signup_serializer.is_valid(raise_exception=True)):
            # ... new account 
            nAccount = signup_serializer.save()
            if(nAccount):
                #... set payload 
                payload["msg"] = "successfully registered with XCrossing Lines"
                payload["email"] = nAccount.email
                #... respond 
                return Response(payload, status=status.HTTP_201_CREATED)
        # ... otherwise error 
        return Response(signup_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
# Read the 
class AccountGetAPIVIEW(APIView): 
    
    #... permissions 
    permission_classes = [IsAuthenticated,]
    
    #... get method 
    def get(self, request, *args, **kwargs):
        
        #... acccount model 
        acccount = get_object_or_404(get_user_model(), pk = request.user.pk)
        
        # seralize cAccount = customer_account
        cAccount = AccountSerializer(acccount, many = False)
        return Response(cAccount.data, status = status.HTTP_200_OK)

# update 
class AccountUpdateAPIVIEW(APIView):
    
    #set permissions 
    permission_classes = [IsAuthenticated,]
    
    # .. update
    def put(self, request, *args, **kwargs):
        
        #.. first set payload 
        payload = dict()
        
        # retrieve logged in 
        account = request.user
        
        # //check 
        if isinstance(account, get_user_model()):
            # .. get update account = uAccount
            uAccount = get_object_or_404(get_user_model(), pk = account.pk)
            uAccountSerializer = AccountUpdateSerializer(uAccount, data = request.data)
            
            # .. check if valid 
            if uAccountSerializer.is_valid(raise_exception=True):
                uAccountSerializer.save()
                return Response(uAccountSerializer.data, status=status.HTTP_200_OK)
            return Response(uAccountSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #...
        payload["msg"] = "UNAUTHORIZED"
        return Response(payload, status=status.HTTP_401_UNAUTHORIZED)
         
    
# ... delete user account 
class DeleteAccountAPIVIEW(APIView):
    
    # set permissions
    permission_classes = [IsAuthenticated,]
    
    # ... override delete 
    def delete(self, request, *args, **kwargs):
        
        # ... 
        if request.user.is_authenticated:
            #.. retrieve account dAccount = delete Account 
            dAccount = get_object_or_404(get_user_model(), id = request.user.id) 
            dAccount.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)

# ... signin access_token and refesh_token
class SignInTokenObtainPairView(TokenObtainPairView):
     # set permissions
    permission_classes = [AllowAny,]
    
    # .. 
    serializer_class = SigninTokenObtainPairSerializer

# .. signout
class SignOutAPIVIEW(APIView):
    
    #.. enter permissions 
    permission_classes = [IsAuthenticated]
    
    # .. post to blacklist
    def post(self, request, *args, **kwargs):
        
        # payload 
        payload = dict()
        
        # account 
        account = request.user
        
        #try to blacklist 
        try:
            
            #retrieve outstanfing tokens
            tokens = OutstandingToken\
                        .objects\
                        .filter(user_id = account.id)
                        
            # loop 
            for token in tokens:
                t, _ = BlacklistedToken\
                        .objects\
                        .get_or_create(token = token)
                        
           
            payload["msg"] = "successfully logged out"
            # when done return
            return Response(payload, status=status.HTTP_200_OK)
        
        # raise exception
        except  Exception as e:
            
            # .. set payload 
            payload["msg"] = str(e)
            
            #... respond 
            return Response(payload, status = status.HTTP_400_BAD_REQUEST)
        
