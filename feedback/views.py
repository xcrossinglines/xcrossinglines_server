
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics 
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

# ... models 
from .models import FeedBack

# ... serializers 
from .serializers import FeedBackSerializer

# ... paginator
from .feedbackPagination import FeedbackPaginator

# ... create view 
class CreateFeedBackAPIVIEW(APIView):

    # .. rough setup
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackSerializer
    permission_classes = [AllowAny,]

    # ... 
    def post(self, request, *args, **kwargs): 

        # .. define payload 
        payload = dict()

        # .. request 
        customer_id = request.data.get("customer_id")
        service_commentry = request.data.get("service_commentry")
        website_commentry = request.data.get("website_commentry")
        service_rating = request.data.get("service_rating")
        website_rating = request.data.get("website_rating")

        # .. verify 
        if(customer_id is None or service_commentry is None 
                or website_commentry is None or service_rating is None 
                    or website_rating is None): 
            
            # .. prepare payload 
            payload["msg"] = "Params cannot be null! Bad request 400."

            # respond 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        # .. otherwise we are all good 
        feedbackSerializer = FeedBackSerializer(data=request.data, many = False)
        if(feedbackSerializer.is_valid(raise_exception=True)):
            feedbackSerializer.save()
            payload["msg"] = "Thank you for your feed back."
            return Response(payload, status=status.HTTP_200_OK)
        # ... otherwise error 
        payload["msg"] = feedbackSerializer.errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
    
# ... fetch testimonials 
class GetFeedBackAPIVIEW(generics.ListAPIView):

    # ... 
    queryset = FeedBack\
                .objects\
                .filter(allow_display = True)\
                .order_by("-created_at")
    
    serializer_class = FeedBackSerializer
    pagination_class = FeedbackPaginator
    permission_classes = [AllowAny,]

