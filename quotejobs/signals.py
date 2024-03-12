from django.db.models.signals import post_save, pre_delete, pre_save 
from django.dispatch import receiver

# .. model 
from .models import QuoteJob

# ... pricing model 
from generate_quote.generate_quote import GenerateQuote


# ... register presave 
@receiver(pre_save, sender=QuoteJob)
def save(sender, instance, *args, **kwargs):

    distance = float("%.0f"%round(instance.distance))

    pricing_instance = GenerateQuote(
                        distance=distance,
                        floors=instance.floors,
                        helpers=instance.helpers,
                        vSize=instance.vehicle_size,
                        shuttle=instance.shuttle,
                        job_date=instance.job_date)
    
    # generate pricing 
    base_fee, peak_discount = pricing_instance.generate_pricing


    # set values 
    instance.distance = distance
    instance.base_fee = float("%.0f"%round(base_fee)) 
    instance.mid_discount = float("%.0f"%round(peak_discount)) 
    instance.amount_due = float("%.0f"%round(base_fee - peak_discount)) 
