from django.urls import path, include


#.. import the view 
from . import views

# ... 
urlpatterns = [

    path("get/config/", views.VerifyCompleteProfileView.as_view(), name="app-configs"),
]
