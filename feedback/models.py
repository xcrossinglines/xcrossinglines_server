from django.db import models

# ... create FAQsModel 
class FeedBack(models.Model):
    
    # .. stop skipping 
    id = models.AutoField(primary_key=True)

    # .. string 
    customer_id = models.CharField(default = "", 
                                    max_length = 100, 
                                    null=True, 
                                    blank=True)

    service_commentry = models.CharField(default = "", 
                                        max_length = 250, 
                                        null=True, 
                                        blank=True)
    
    website_commentry = models.CharField(default = "", 
                                        max_length = 250, 
                                        null=True, 
                                        blank=True)
    
    # ... numerical values
    service_rating = models.FloatField(default = 0.0, 
                                        null = True, 
                                        blank = True)
    
    website_rating  = models.FloatField(default = 0.0, 
                                        null = True, 
                                        blank = True)

    # .. date fields 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # overide the string method 
    def __str__(self):
        return "FeedBack: {0} = {1}".format(self.id, self.service_commentry)
      


    