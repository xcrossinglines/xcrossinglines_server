# ... 3rd party imports 
from rest_framework.serializers import ModelSerializer, SerializerMethodField

# ... local imports 
from .models import QuoteJob, QuoteRoutes


# generate QuoteRoutes Serializer 
class QuoteRouteSerializer(ModelSerializer):

    class Meta: 
        model = QuoteRoutes
        fields = "__all__"

# .... 
class GetQuoteJobSerializer(ModelSerializer):

    # ... 
    # routes = SerializerMethodField(read_only = True)
    routes = QuoteRouteSerializer(read_only=True, many = True)

    class Meta: 
        # ... 
        model = QuoteJob
        fields = [
            "id",
            "helpers",
            "floors",
            "shuttle",
            "vehicle_size",
            "payment_option",
            "driver_note",
            "routes",
            "base_fee",
            "amount_due",
            "mid_discount",
            "distance",
            "job_date",
            "job_time",
            "created_at",
        ]
    # # .. retrieve routes 
    # def get_routes(self, instance):

    #     # ... safety precaution
    #     if(isinstance(instance, QuoteJob)):
    #         #.. return routes 
    #         return [{"lat":route.lat, 
    #                 "lng": route.lng,
    #                 "route_name": route.route_name} 
    #                     for route in instance.routes.all() ]

# ... post serializer 
class PostQuoteJobSerializer(ModelSerializer):

    # ... meta
    class Meta: 
        model = QuoteJob
        fields = [
            "helpers",
            "floors",
            "shuttle",
            "vehicle_size",
            "payment_option",
            "driver_note",
            "distance",
            "job_date",
            "job_time",
        ]


class UpdateQuoteJobSerializer(ModelSerializer):

    class Meta: 
        model = QuoteJob
        fields = [
            "helpers",
            "floors",
            "shuttle",
            "vehicle_size",
            "driver_note",
            "payment_option",
            "distance",
            "job_date",
            "job_time", 
        ]

