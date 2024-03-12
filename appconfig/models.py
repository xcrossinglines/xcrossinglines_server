from django.db import models
from rest_framework.authentication import get_user_model
from django.utils.translation import gettext_lazy as _

# // shutdown website 
class AppConfigModel(models.Model):

    # .. set variables
    NO = False
    YES = True

    YES_NO_CHOICES = [(NO, "No"), (YES, "Yes")]

    id = models.AutoField(primary_key=True)
        
    super_user = models.ForeignKey(get_user_model(), 
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True)
    
    shutdown_website =  models.BooleanField(default=NO, 
                                       choices = YES_NO_CHOICES, 
                                       null = False, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    # overide the string method 
    def __str__(self):
        return "AppConfig: {0} => {1}".format(self.id, self.shutdown_website)
      


    