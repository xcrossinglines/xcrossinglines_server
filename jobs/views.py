from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from decouple import config
# ... models
from rest_framework.authentication import get_user_model

# ..views 
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

# ... pagination class 
from .pagination import JobsPaginator

# ... import models 
from .models import Job, Route
# from referals.models import Referal
# from accounts.models import AccountProfile

# ... utils 
from .g_quote import GenerateQuote

# ... import serializers 
from .serializer import (JobsGetCustomerSerializer, 
                         JobCreateSerializer, 
                         JobUpdateSerializer)

# ... google 
import googlemaps



# ... retrieve/Get ALL Customer Jobs 
class JobsGETALLCustomerListAPIVIEW(generics.ListAPIView):
    
    # ...  
    queryset = Job.objects\
                .all().order_by("-created_at")
    serializer_class = JobsGetCustomerSerializer
    pagination_class = JobsPaginator
    

 # ... retrieve one Job 
class GetJobAPIView(APIView):
    
    # ... init 
    queryset = Job\
                .objects\
                .all()
                
    lookup_field = 'pk'           
    serializer_class = JobsGetCustomerSerializer
    permission_classes = [IsAuthenticated,]
    
    # .. get 
    def get(self, request, *args, **kwargs):    
        # .. setpayload 
        payload = dict()
        # ... job pk 
        job_pk = self.kwargs.get("pk")
        # .. chec
        if(isinstance(job_pk, type(None))):
            # .. set payliad 
            payload["msg"] = "job invoice pk cannot be null"
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        #.... 
        try:
            # ... check instance 
            if(isinstance(request.user, get_user_model())):
                # .. fetch job 
                cJob = Job\
                        .objects\
                        .filter(pk = job_pk)\
                        .first()
                # .. check if we was able to find it 
                if(isinstance(cJob, type(None))):
                    # // this means we didnt find it 
                    payload["msg"] = "No job with given pk"
                    # ..return 
                    return Response(payload, status=status.HTTP_204_NO_CONTENT)
                # .. else means it was found 
                # .. check if the customer requesting the job is the same customer who made the job
                if(cJob.customer == request.user):
                    # ... return 
                    serialized_job = JobsGetCustomerSerializer(cJob, many=False)
                    return Response(serialized_job.data, status=status.HTTP_200_OK)
                
                # .. otherwise
                payload["msg"] = "you are unathorized to access the this job, bad request"
                # .. return
                return Response(payload, status = status.HTTP_400_BAD_REQUEST)
                # ...
        except Job.DoesNotExist:
            # set payload 
            payload["msg"] = "Job doesnt exists"
            #.. return 
            return Response(payload, status=status.HTTP_204_NO_CONTENT)
    
# ... get custom customer jobs 
class JobsGETCustomerListAPIVIEW(generics.ListAPIView):
    
    # ...  
    queryset = Job.objects\
                .all()\
                .order_by("-created_at")
                
    serializer_class = JobsGetCustomerSerializer
    # pagination_class = JobsPaginator
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,]
    
    # ... override get method 
    def get(self, request, *args, **kwargs):
        
        # ... declare payload 
        payload = dict()
        # ... procaution 
        try:
            
            # // verify that user is logged in 
            if(isinstance(request.user, get_user_model())):
                # fetch customer jobs 
                customer_jobs = Job.objects\
                                .filter(customer = request.user)\
                                .order_by('-created_at')
                
                # ... paginator     
                paginator = JobsPaginator()
                cJobs = paginator\
                        .paginate_queryset(customer_jobs, request= request)  #// customer bookings 
                        
                sJobs = JobsGetCustomerSerializer(cJobs, many = True)
                
                #  ... 
                return paginator.get_paginated_response(sJobs.data)
            
            # here we catch the error 
            #// 
            payload["msg"] = "You are not Authenticated please login" 
            
            # we serialize the data 
            return Response(payload, status=status.HTTP_401_UNAUTHORIZED) 
        
            # .... 
        except Job.DoesNotExist:
            # here we catch the error 
            #// 
            payload["msg"] = "Jobs dont exists" 
            
            # we serialize the data 
            return Response(payload, status=status.HTTP_204_NO_CONTENT) 

# ... create Job
class JobCustomerCreateAPIVIEW(generics.CreateAPIView):
    
    queryset = Job.objects.all() #// 
    serializer_class = JobCreateSerializer
    permission_classes = [IsAuthenticated,]
    
    # ...register all routes 
    def register_routes(self, routes):
        
        # ... jRoute = Job Routes
        # ... create and store in list 
        jRoutes = [Route
                    .objects
                    .create(
                        route_name = a["route_name"], 
                        lat = a["lat"], 
                        lng = a["lng"]) 
                        # /// forloop 
                        for a in routes]
        # ... return List 
        return jRoutes
    
    # ... override the post 
    def post(self, request, *args, **kwargs):
        
        # payload 
        payload = {}
        
        # ... get params 
        customer = request.user # ... logged in customer
        helpers = request.data.get("helpers")  # int 
        floors = request.data.get("floors") # int 
        vehicle_size = request.data.get("vehicle_size") # float 
        payment_option = request.data.get("payment_option")  # string 
        driver_note = request.data.get("driver_note")  # String 
                                
        distance = request.data.get("distance") # float 
        routes = request.data.get("routes")  # list[string, float, float]
        # job_canceled = request.data.get("job_canceled") # boolean 
        
        # dates 
        job_date = request.data.get("job_date")  # string 
        job_time = request.data.get("job_time")  # string 
        
        # ... for the refferals 
        # referal_code = request.data.get("referal_code")
        hear_about_us = request.data.get("hear_about_us")

        # # ... check which is null 
        # print("helpers: ", helpers)
        # print("floors: ", floors)
        # print("vehicle_size: ", vehicle_size)
        # print("payment_option: ", payment_option)
        # print("driver_note: ", driver_note)
        # print("distance: ", distance)
        # print("routes: ", routes)
        # print("job_date: ", job_date)
        # print("job_time: ", job_time)
        # print("referal_code: ", referal_code)
        
        # ... verify that all is not none 
        if(helpers is None or floors is None 
                or vehicle_size is None or payment_option is None 
                        or driver_note is None or distance is None or routes is None 
                                or job_date is None or job_time is None or hear_about_us is None):
 
            # ... set the payload 
            payload["msg"] = "Params cannot be null! Bad request 400."
            # .. respond 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
                
        # ... save and return routes
        jRoutes = self.register_routes(routes)
        
        # .. check if routes exist
        if(len(list(jRoutes)) < 2):
            #// 
            # cannot have zero routes 
            payload['msg'] = 'invalid routes len, please check your routes'
            
            # return response 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # .. remove and add customer name to the dictionary
        # request.data.pop("routes")
        request.data["customer"] = customer.id
        # ..serialize the data 
        jSerializer = JobCreateSerializer(data=request.data, many = False)
        if(jSerializer.is_valid(raise_exception=True)):
            
            # //create job 
            createdJob = jSerializer.save()
            #// add routes 
            createdJob.routes.add(*jRoutes)

            #// set payload
            payload["msg"] = "Created Successfully."

            #// respond    
            return Response(payload, status=status.HTTP_200_OK)
        
        # catch errors and respond 
        return Response(jSerializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

    
# // update job 
class JobCustomerUpdateAPIVIEW(generics.UpdateAPIView):
    
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = JobUpdateSerializer
    lookup_field = 'pk' # ... perfect
    
    # update routes 
    def update_routes(self, routes):
        
        #// verify that item is not none 
        if(isinstance(routes, type(None))):
            return False, []
        
        # ... jRoutes = Job Routes 
        jRoutes = [Route
                    .objects
                    .create(
                        route_name = a["route_name"], 
                        lat = a["lat"], 
                        lng = a["lng"]) 
                            for a in routes]
        # .. return 
        return True, jRoutes

        
    # update 
    def update(self, request, *args, **kwargs):
        
        # payload 
        payload = {}
        # .. update Job
        uJob = self.get_object()
        
        # .. verify that customer and job customer are the same people 
        if(uJob.customer.id != request.user.id):
            # warning 
            payload["msg"] = "Opps!. you are UNAUTHORIZED to complete this action."
            # response 
            return Response(payload, status=status.HTTP_401_UNAUTHORIZED) 
        
        # .. check 
        routes = request.data.get("routes")
        
        # .. retrieve new routes 
        sUpdate, jRoutes = self.update_routes(routes) # .. should update routes, job routes respectively
        
        # init serializer 
        jSerializer = JobUpdateSerializer(uJob,  data = request.data, 
                                         partial = True, many = False)
        if(jSerializer.is_valid(raise_exception=True)):
            
            #// 
            updated_job = jSerializer.save() # .. save 
            
            # .. tells me if I should update the routes also 
            if(sUpdate):
                
                # .. delete 
                for route in updated_job.routes.all():
                    route.delete() # .. delete route from memory
                    
                # .. wen done add the new ones 
                updated_job.routes.add(*jRoutes)
                
            # set payload 
            payload["msg"] = "Yey update success"
            payload["job"] = jSerializer.data
            
            # .. repond
            return Response(payload, status=status.HTTP_200_OK)
        # .. 
        return Response(jSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ... generate Quote 
class GenerateQuoteAPIVIEW(APIView):
    
    # .. add permissionis
    permission_classes = [AllowAny,]


    # .. create function generate what we want 
    def getUserType(self, cUser):

        # payload 
        payload = dict()
        
        # ... check if cUserExists 
        if(isinstance(cUser, get_user_model())):

            # .. set correct payload
            payload["loggedin"] = True
            payload["is_staff"] = cUser.is_staff

            # .. return 
            return payload
            
        # ... set default 
        payload["loggedin"] = False 
        payload["is_staff"] = False 

        # return payload 
        return payload 
    
    #... apply return customer discount if customer is logged in 
    def return_customer_discount(self, cUser, quote):

        # ... zero discount
        zero_discount = 0.0

        # ... verify that customer is logged in 
        if(isinstance(cUser, get_user_model())):

            # ... verify that customer is cooperate 
            if(cUser.is_corperate):
                # .. continue 
                customerJobs = Job.\
                                objects.\
                                    filter(customer = cUser)\
                                        .order_by('-created_at')
                
                # ... customer job count 
                customerJobCount = len(customerJobs)

                # .. verify job count size
                if(customerJobCount >= 1): return quote*(5/100.0)

                # ... else 
                return zero_discount
            # ... else
            return zero_discount
        # ... else 
        return zero_discount

    # override post method 
    def post(self, request, *args, **kwargs):
        
        # .. define payload 
        payload = dict()

        # ... Noneable fields 
        cUser = request.user

        # .. 
        floors = request.data.get("floors") # int 
        helpers = request.data.get("helpers")  # int 
        shuttle = request.data.get("shuttle") # int 
        vehicle_size = request.data.get("vehicle_size") # float 
        distance = request.data.get("distance") # float 
        job_date = request.data.get("job_date")  # string 
   
        # .. verify exists 
        if(floors is None 
            or helpers is None 
                or vehicle_size is None 
                        or distance is None 
                            or job_date is None 
                                or shuttle is None):
            
            # // set payload 
            payload["msg"] = "floors|helpers|vSize|distance|shuttle and date cannot be null"
            
            # //send response 
            return Response(payload, status= status.HTTP_400_BAD_REQUEST)
        
        # .. generate quote 
        jInstance = GenerateQuote(job_date = job_date,
                                  distance = float("%.0f"%round(distance)),
                                  floors = floors,
                                  helpers = helpers,
                                  vSize = vehicle_size,
                                  shuttle= shuttle)

        # .. resolve 
        customerQuote, peakDiscount = jInstance.generate_quote_discount

        # ... generate return customer discount if customer is logged in 
        return_customer_d = self.return_customer_discount(cUser, (customerQuote-peakDiscount))

        # ... generating current user details cDetails = Current User details 
        userDetails = self.getUserType(cUser)
        
        # set set payload 
        payload["quote"] = float("%.0f"%round(customerQuote)) 
        payload["middle_month_discount"] = float("%.0f"%round(peakDiscount)) 
        payload["return_customer_discount"] = float("%.0f"%round(return_customer_d))
        payload["amount_due"] = float("%.0f"%(customerQuote - peakDiscount - return_customer_d))
        payload["user_details"] = userDetails
        
        # return 
        return Response(payload, status = status.HTTP_200_OK)
        
#// Generate Distance ApiView 
class GenerateDistanceAPIVIEW(APIView):
    
    # ... permission class
    permission_classes = [AllowAny,]

    # post 
    def post(self, request, *args, **kwargs):
        
        # declare payload 
        payload = {}
        
        # // init client      
        client = googlemaps.Client(key = config("GOOGLE_API_KEY", cast=str))

        #// 
        routes = request.data.get("routes") 
        
        # .. verify correct routes
        if(isinstance(routes, type(None))):
            
            # .. set payload 
            payload["msg"] = "Routes cannot be null"
            
            # .. respond 
            return Response(payload, status = status.HTTP_400_BAD_REQUEST)
        
        #// variables 
        startRoutes, endRoutes = list(), list()

        #// populatate 
        for index in range(len(routes) - 1):
            
            #// start destinations  
            startRoutes.append((routes[index]["lat"],
                                        routes[index]["lng"]))
            #end destinations 
            endRoutes.append((routes[index + 1]["lat"], 
                                        routes[index + 1]["lng"]))
            
        #// check if theres something in the lists 
        if( len(startRoutes) > 0 and len(endRoutes) > 0): 
            
            try:
                #// then this is where we need to do miracles 
                results = client\
                        .distance_matrix(
                                        startRoutes, 
                                        endRoutes,
                                        mode = "driving")
                #// distance 
                dStance = 0.0
                
                #// forloop
                for i in range(len(results["rows"])):
                    
                    #// retrieve the distance 
                    itemDistance = results["rows"][i]["elements"][i]["distance"]["value"] #//m 
                    
                    #// add 
                    dStance += itemDistance
                    
                #// set payload  
                payload["distance"] = dStance/1000.0
                payload["msg"] = "Successfully generated distance"
                
                #// respond 
                return Response(payload, status=status.HTTP_200_OK)
            except Exception as e:
                
                #// set payload 
                payload["distance"] = 0.0
                payload["msg"] = 'Error {0}'.format(e)
                
                #// respond 
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)
            
        #// set payload  
        payload["distance"] = 0.0
        payload["msg"] = "list locations is empty, cant be empty"
        payload["status_code"] = str(status.HTTP_400_BAD_REQUEST)
        
        #// respond 
        return Response(payload, status=status.status.HTTP_400_BAD_REQUEST)
                
            

    