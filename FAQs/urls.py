from django.urls import path, include


#.. import the view 
from . import views

# ... 
urlpatterns = [

    path("get/", views.FAQsGetListAPIVIEW.as_view(), name="FAQS")

]
