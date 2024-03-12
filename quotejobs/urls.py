from django.urls import path, include


from . import views


# ... url patterns 
urlpatterns = [
    
     # ... 
    path("get/<int:pk>/", views.GetQuoteJobAPIView.as_view(), name = "get-quote-job-view"),
    path("post/", views.PostQuoteJobAPIView.as_view(), name = "post-quote-job-view"),
    path("update/<int:pk>/", views.UpdateQuoteJobUpdateAPIView.as_view(), name = "update-quote-job-view"),
         
]