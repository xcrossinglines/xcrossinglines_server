from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics 
from rest_framework.permissions import AllowAny, IsAuthenticated

# ... import models 
from .models import QuoteJob, QuoteRoutes

# ... serializers 
from .serializers import (GetQuoteJobSerializer, 
                          PostQuoteJobSerializer, 
                          UpdateQuoteJobSerializer)

# ... get Quote Job 
class GetQuoteJobAPIView(APIView):

    # ... init 
    queryset = QuoteJob.objects.all()
    lookup_field = "pk"
    serializer_class = GetQuoteJobSerializer
    permission_classes = [AllowAny]

    # ... get 
    def get(self, request, *args, **kwargs):

        # .. variables 
        payload = dict()

        # ... fields 
        jpk = self.kwargs.get("pk")

        # ... verify that its not none 
        if(isinstance(jpk, type(None))):
            # .. populate 
            payload["msg"] = "job primary key cannot be null" 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        #.. otherwise everything is fine 
        QJob = get_object_or_404(QuoteJob, pk = int(jpk))

        # ... otherwise we found it 
        QJobSerializer = GetQuoteJobSerializer(QJob)
        # #.. return response 
        return Response(QJobSerializer.data, status=status.HTTP_200_OK)
      
# .. create QuoteJob
class PostQuoteJobAPIView(APIView):

    # ... init 
    queryset = QuoteJob.objects.all()
    serializer_class = PostQuoteJobSerializer
    permission_classes = [AllowAny, ]

        # ...register all routes 
    def register_routes(self, routes):
        
        # ... jRoute = Job Routes
        # ... create and store in list 
        jRoutes = [QuoteRoutes
                    .objects
                    .create(
                        route_name = a["route_name"], 
                        lat = a["lat"], 
                        lng = a["lng"]) 
                        # /// forloop 
                        for a in routes]
        # ... return List 
        return jRoutes
    
    # ... verify routes 
    def verify_routes(self, routes): 

        # ... 
        length_routes = len(routes)
        # .. if 
        if(length_routes < 2): 
            # ... generate 
            message = "Empty routes, routes cannot be null"
            verification = False
            status_code = status.HTTP_412_PRECONDITION_FAILED

            # ... return 
            return message, verification, status_code
        
        #.. otherwise everything is fine 
        return "", True, status.HTTP_200_OK
    
    # ... post
    def post(self, request, *args, **kwargs):

        # variables 
        payload = dict()

        # ... get params 
        helpers = request.data.get("helpers")  # int 
        floors = request.data.get("floors") # int 
        vehicle_size = request.data.get("vehicle_size") # float 
        payment_option = request.data.get("payment_option")  # string 
        distance = request.data.get("distance") # float 
        routes = request.data.get("routes")  # list[string, float, float]

        # dates 
        job_date = request.data.get("job_date")  # string 
        job_time = request.data.get("job_time")  # string 


    
        # verify that they are not none 
        if(helpers is None or
             floors is None or 
                vehicle_size is None or 
                    payment_option is None or 
                        distance is None or 
                            routes is None or 
                                job_date is None 
                                    or job_time is None):
            
            # ... set payload 
            payload["msg"] = "params cannot be null, Bad request."

            # return 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        
        #... otherwise if everything fine
        registered_routes = self.register_routes(routes=routes)

        #... very route lengths 
        msg, verification, status_code = self.verify_routes(routes=registered_routes)
        #  
        if(verification == False):
            # ..verification failed
            payload["msg"] = msg
            # .. 
            return Response(payload, status=status_code)
        
        # ... otherwise we alright 
        QJobSerializer = PostQuoteJobSerializer(data=request.data)
        if(QJobSerializer.is_valid(raise_exception=True)):
            # .. success 
            qJob = QJobSerializer.save()
            # .. if 
            if(isinstance(qJob, QuoteJob)):
                qJob.routes.add(*registered_routes)
                # ..
                payload["msg"] = "success!"
                payload["jpk"] = qJob.pk
                # ... 
                return Response(payload, status=status.HTTP_201_CREATED)
            
            #... error message 
            payload["msg"] = "Instance is not of instance"
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        # otherwise we had a problem 
        return Response(QJobSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

         
# ... update Job
class UpdateQuoteJobUpdateAPIView(generics.UpdateAPIView):
    # ... 
    queryset = QuoteJob.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = UpdateQuoteJobSerializer
    lookup_field = "pk"

    # ... function to update routes 
    def update_routes(self, routes): 

        # ... verify 
        if(isinstance(routes, type(None))):
            return False, []
        
        # .. new Routes 
        new_routes = [
            QuoteRoutes.objects.create(
                route_name = route["route_name"],
                lat = route["lat"],
                lng = route["lng"],
                    ) for route in routes]
        
        # ... return 
        return True, new_routes
    
    # ... 
    def update(self, request, *args, **kwargs):

        # ... 
        QJob = self.get_object()
        # ... 
        updated, routes = self.update_routes(request.data.get("routes"))

        # init serializer 
        serializer = UpdateQuoteJobSerializer(QJob, 
                                              data=request.data, 
                                              partial = True,
                                              many = False)
        # ... 
        if(serializer.is_valid(raise_exception=True)):
            updated_qjob = serializer.save()
            # ... 
            if(updated):
                # ... 
                for route in updated_qjob.routes.all():
                    route.delete()
                
                # ... update routes 
                updated_qjob.routes.add(*routes)
            
            # payload
            serializer.data["msg"] = "Updated successfully"
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # ... 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


                



