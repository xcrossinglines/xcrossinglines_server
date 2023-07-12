
from django.urls import path

# .. views 
from . import views

# ... urlparttens 
urlpatterns = [

    path("post/feedback/", views.CreateFeedBackAPIVIEW.as_view(), name="customer-feed-back"), 
    path("get/feedback/", views.GetFeedBackAPIVIEW.as_view(), name="get-customer-feed-back"),

] 
