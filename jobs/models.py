from django.db import models
from rest_framework.authentication import get_user_model
from django.utils.translation import gettext_lazy as _


# .. create route model 
class Route(models.Model):

    DESCRIPTIONCHOICES = [(0, "Pickup"), (1, "Dropoff"), (2, "Both")]

    # stop skipping 
    id = models.AutoField(primary_key=True)
    
    # ... route details 
    route_name = models.CharField(default = '', max_length = 400, null=True, blank=True)
    description = models.IntegerField(default = 2, choices= DESCRIPTIONCHOICES, null = True, blank = True)
    lat =  models.DecimalField(max_digits=35, decimal_places=30, null=True, blank=True)
    lng =  models.DecimalField(max_digits=35, decimal_places=30, null=True, blank=True)
    
    # date fields 
    created_at = models.DateTimeField(auto_now_add= True)

    # overide the string method 
    def __str__(self):
        return '(Route: ||{0}||-{1})'.format(self.id, self.route_name)
      

# .. create Job Model 
class Job(models.Model):

    # .. set variables
    NO = False
    YES = True

    # .. 
    YES_NO_CHOICES = [(NO, "No"), (YES, "Yes")]
    
    # set 
    VSIZECHOICES = [(1.0, "1.0 Ton"), (1.5, "1.5 Ton"), 
                    (2.0, "2.0 Ton"), (3.0, "3.0 Ton"),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                    (4.0, "4.0 Ton"), (8.0, "8.0 Ton")]
    
    PAYMENTOPTIONS = [("EFT", "EFT"), ("CASH", "CASH")]
    FLOORSCHOICES = [(f, f) for f in range(11)]
    SHUTTLECHOICES = [(s,  ["None", "Pick up", "Drop off", "both"][s]) for s in range(4)]
    HELPERCHOICES = [(h + 1, h + 1) for h in range(3)]
    HEARABOUTUS = [("None", "None"), ("Facebook", "Facebook"), ("Gumtree", "Gumtree"), ("Referral", "Referral")]
    
    
    # .. stop skipping 
    id = models.AutoField(primary_key=True)
    
    # .. personel 
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name=_("customer_identity"), null=True)
    driver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name=_("driver_identity"), null=True, blank=True)
    
    # ... additional information 
    helpers = models.IntegerField(default = 1, choices=HELPERCHOICES, null = True, blank = True)
    floors = models.IntegerField(default = 0, choices=FLOORSCHOICES, null = True, blank = True)
    shuttle = models.IntegerField(default = 0, choices=SHUTTLECHOICES, null = True, blank = True)

    payment_option = models.CharField(default = 'CASH', choices=PAYMENTOPTIONS, max_length = 50, null=True, blank=True)
    driver_note = models.TextField(default= 'No note left', max_length = 1000, null = True, blank = True)
    price_adjustment_justification = models.TextField(default= 'No note left', max_length = 2500, null = True, blank = True)

    hear_about_us = models.CharField(default= 'None', max_length = 100, null = True, blank = True, choices=HEARABOUTUS)
 
    # ... referal code for discount 
    referal_code = models.CharField(max_length=150, null=True, blank=True, default="xcrossinglines") 
    referal_discount = models.FloatField(default = 0.0, null = True, blank = True)
    
    vehicle_size = models.FloatField(default = 1.0, choices=VSIZECHOICES, null = True, blank = True)
    
    # ... job money 
    base_fee = models.FloatField(default = 0.0, null = True, blank = True)
    amount_due = models.FloatField(default = 0.0, null = True, blank = True)
    mid_discount = models.FloatField(default = 0.0, null = True, blank = True)
    distance = models.FloatField(default = 0.0, null = True, blank = True)
    extra_discount = models.FloatField(default = 0.0, null = True, blank = True)
    extra_discount_pecentage = models.FloatField(default = 0.0, null = False, blank = False)
    price_adjustment = models.FloatField(default = 0.0, null = False, blank = False)
    return_customer_discount = models.FloatField(default = 0.0, null = True, blank = True)
    
    # ... 
    routes = models.ManyToManyField(Route, blank = True)
    
    # ... booleans 
    job_completed = models.BooleanField(default=NO, choices=YES_NO_CHOICES, null = False, blank=False)
    job_canceled = models.BooleanField(default=NO, choices = YES_NO_CHOICES, null = False, blank=False)
    job_cancellation_feedback_sent = models.BooleanField(default=NO, choices = YES_NO_CHOICES, null = False, blank=False)
    job_invoice_sent = models.BooleanField(default=NO, choices = YES_NO_CHOICES, null = False, blank=False)
    feedback_email_sent = models.BooleanField(default=NO, choices = YES_NO_CHOICES, null = False, blank=False)
    job_out_sourced = models.BooleanField(default=NO, choices = YES_NO_CHOICES, null = False, blank=False)
    give_extra_discount = models.BooleanField(default=NO, choices = YES_NO_CHOICES, null = False, blank=False)
    set_price_adjustment = models.BooleanField(default=NO, choices = YES_NO_CHOICES, null = False, blank=False)
    
    # .. date fields 
    job_date = models.DateField(null = True)
    job_time = models.TimeField(null = True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    # overide the string method 
    def __str__(self):
        return 'JOB INVOICE: {0}'.format(self.id)
      

