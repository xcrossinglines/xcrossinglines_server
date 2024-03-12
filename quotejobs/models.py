from django.db import models


# ... 
class QuoteRoutes(models.Model):

    # .. description 
    DESCRIPTIONCHOICES = [(0, "Pickup"), (1, "Dropoff"), (2, "Both")]
    # .. generate id 
    id = models.AutoField(primary_key=True)

    # ... route details 
    route_name = models.CharField(default="", max_length=400, null=True, blank=True)
    description = models.IntegerField(default = 2, choices= DESCRIPTIONCHOICES, null = True, blank = True)
    lat = models.DecimalField(max_digits=35, decimal_places=30, null=True, blank=True)
    lng = models.DecimalField(max_digits=35, decimal_places=30, null=True, blank=True)

    # ... 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    # overide the string method 
    def __str__(self):
        return '(Route: ||{0}||-{1})'.format(self.id, self.route_name)

# ... job 
class QuoteJob(models.Model):

    # .. set variables
    NO = False
    YES = True

    # .. 
    YES_NO_CHOICES = [(NO, "No"), (YES, "Yes")]
    VSIZECHOICES = [(1.0, "1.0 Ton"), (1.5, "1.5 Ton"), 
                    (2.0, "2.0 Ton"), (3.0, "3.0 Ton"),  
                    (4.0, "4.0 Ton"), (8.0, "8.0 Ton")]
    PAYMENTOPTIONS = [("EFT", "EFT"), ("CASH", "CASH")]
    FLOORSCHOICES = [(f, f) for f in range(11)]
    SHUTTLECHOICES = [(s,  ["None", "Pick up", "Drop off", "both"][s]) for s in range(4)]
    HELPERCHOICES = [(h + 1, h + 1) for h in range(3)]

    # .. generate unskipping id
    id = models.AutoField(primary_key=True)

        # ... additional information 
    helpers = models.IntegerField(default = 1,
                                  choices=HELPERCHOICES, 
                                  null = True, 
                                  blank = True)
    
    floors = models.IntegerField(default = 0, 
                                 choices=FLOORSCHOICES,
                                 null = True, 
                                 blank = True)

    shuttle = models.IntegerField(default = 0, 
                                 choices=SHUTTLECHOICES,
                                 null = True, 
                                 blank = True)
    
    vehicle_size = models.FloatField(default = 1.0, 
                                     choices=VSIZECHOICES,
                                     null = True, 
                                     blank = True)
    
    payment_option = models.CharField(default = 'CASH', choices=PAYMENTOPTIONS, 
                                     max_length = 50, null=True, blank=True)
   
    distance = models.FloatField(default = 0.0, null = True, blank = True)

    # ... 
    routes = models.ManyToManyField(QuoteRoutes, blank = True)

    # drivernote
    driver_note = models.TextField(default= '', max_length = 1000, null = True, blank = True)
    
    # ... job money 
    base_fee = models.FloatField(default = 0.0, null = True, blank = True)
    amount_due = models.FloatField(default = 0.0, null = True, blank = True)
    mid_discount = models.FloatField(default = 0.0, null = True, blank = True)

    # .. date fields 
    job_date = models.DateField(null = True)
    job_time = models.TimeField(null = True)

    # .. created at 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    # overide the string method 
    def __str__(self):
        return 'Quote Invoice: {0}'.format(self.id)
      


    