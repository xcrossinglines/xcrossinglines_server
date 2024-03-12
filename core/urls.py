
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

admin.site.site_title = "XcrossingLines"
admin.site.site_header = "XcrossingLines Transport Services (Pty) Ltd"

urlpatterns = [
    path("admin/", admin.site.urls),
    
    #// urls for the rest framework include("jobs.urls"),
    path("accounts/api/account/", include("accounts.urls")),
    path("jobs/api/", include("jobs.urls")),
    path("fqa/api/", include("FAQs.urls")),
    path("config/api/", include("appconfig.urls")),
    path("feedbacks/api/", include("feedback.urls")),
    path("quote/job/api/", include("quotejobs.urls")),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

