from django.db.models.signals import post_save, pre_delete, pre_save 
from django.dispatch import receiver

# ... 
        
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# ... import models 
from .models import Job, Route
from accounts.models import AccountProfile
from referals.models import Referal
# .. utils 
from .g_quote import GenerateQuote

 
# ... is executed at the end
#  .. of the save method
@receiver(post_save, sender = Job)
def created_job(sender, instance = None, created = False, **kwargs):
    if(created):
        # .. compute customer name cName = Customer Name
        cName = "{0} {1}".format(instance.customer.f_name, 
                                 instance.customer.s_name)

        # ... template data tData = template Data
        templateData = {"id": instance.pk,
                 "quote": instance.quote,
                 "mDiscount": instance.middle_month_discount,
                 "rDiscount": instance.referal_discount,
                 "amountDue": instance.amount_due,
                 "paymentOption": instance.payment_option,
                 "cName": cName,
                 "date": instance.job_date,
                 "time": instance.job_time,
                 "helpers": instance.helpers,
                 "floors": instance.floors,
                 "distance": instance.distance,
                 "vSize": instance.vehicle_size,
                 "jobLink": f"https://xcrossinglines.co.za/jobs/job/{instance.pk}/update"}

                    # ... this is where I send the email
        htmlContent = render_to_string("newJob.html", templateData)
        textContent = strip_tags(htmlContent)

                #.. send email 
        sendEmail = EmailMultiAlternatives(
                    f"XCROSSING LINES TRANSPORT PTY(LTD) JOB INVOICE {instance.pk}",
                    textContent, 
                    settings.EMAIL_HOST_USER,
                    ["u12318958@tuks.co.za", f"{instance.customer.email}", "xcrossinglines@gmail.com"]
                )

        sendEmail.attach_alternative(htmlContent, "text/html")  
        sendEmail.fail_silently = True
        sendEmail.send()


#  .. add refferal discount 
def referalDiscount(instance, quote):

    #... execute only when job is completed
    if(instance.job_completed):
        ## instance.referal_code 
        # ... we need the current customer profile 
        userProfile = AccountProfile\
                        .objects\
                        .filter(account = instance.customer)\
                        .first()
        # ... check instance correct 
        if(isinstance(userProfile, AccountProfile)):
            # ... check if referal code is the same
            if(str(instance.referal_code) == str(userProfile.referal_code)):
                return
            # .. otherwise
            referer = Referal\
                        .objects\
                        .filter(referal_code = instance.referal_code)\
                        .first()
            # ... check 
            if(isinstance(referer, Referal)):
                # .. credit with zaka 
                referer.referal_discount += quote*(2/100.0)
                referer.save()
                return
            
#// generate customer referal discount 
def applyCustomerReferalDiscount(instance):
    # ... Account Profile
    userProfile = AccountProfile\
                    .objects\
                    .filter(account = instance.customer)\
                    .first()

    # ... fetch referal
    referer = Referal\
                .objects\
                .filter(referal_code = userProfile.referal_code)\
                .first()
    
    # .. resolve and zero out
    rDiscount = referer.referal_discount
    referer.referal_discount = 0.0
    referer.save()

    # .. return 
    return rDiscount
 
#//
def verifyReferalCode(instance, quote):
    # find referer 
    referer = Referal\
                .objects\
                .filter(referal_code = instance.referal_code)\
                .first()
        # ... check 
    if(isinstance(referer, Referal)): 
        return quote*(102/100.0)
    return quote

# ... Job Cancellation
def jobCancellation(instance):

    #.. check job cancelled
    if(instance.job_canceled):
        # .. here we send email to customer and admin
        # .. compute customer name cName = Customer Name
        cName = "{0} {1}".format(instance.customer.f_name, 
                                 instance.customer.s_name)
        
        # ... template data tData = template Data
        templateData = {"id": instance.pk,
                 "cName": cName,
                 "jobLink": f"https://xcrossinglines.co.za/jobs/job/{instance.pk}/update"}
        
        # ... this is where I send the email
        htmlContent = render_to_string("cancelledJob.html", templateData)
        textContent = strip_tags(htmlContent)

                #.. send email 
        sendEmail = EmailMultiAlternatives(
                    f"XCROSSING LINES TRANSPORT PTY(LTD) JOB CANCELLATION",
                    textContent, 
                    settings.EMAIL_HOST_USER,
                    ["u12318958@tuks.co.za", f"{instance.customer.email}", "xcrossinglines@gmail.com"]
                )

        sendEmail.attach_alternative(htmlContent, "text/html")  
        sendEmail.fail_silently = True
        sendEmail.send()
 

#  .. executed at the beginning
#  .. of the save method
@receiver(pre_save, sender = Job)
def before_saved(sender, instance, *args, **kwargs):
    
    # ... check correct instance
    if(isinstance(instance, Job)):
        
        # .. compute distance 
        dStance = float("%.0f"%instance.distance)
    
        # .. generate instance 
        gQuoteClass = GenerateQuote(distance = dStance,
                                    floors = instance.floors,
                                    helpers = instance.helpers,
                                    vSize = instance.vehicle_size,
                                    job_date = instance.job_date)
        # .. generated quote 
        _quote, dPeak = gQuoteClass.base_discounts
        # ... 
        referalDiscount(instance, _quote)
        # .. 
        nQuote = verifyReferalCode(instance, _quote)
        # .. apply customer referal discount 
        rDiscount = applyCustomerReferalDiscount(instance)

        # .. set 
        instance.quote = float("%.0f"%nQuote) 
        instance.distance = float("%.0f"%dStance)
        instance.referal_discount = float("%.0f"%rDiscount)
        instance.middle_month_discount = float("%.0f"%dPeak)
        instance.amount_due = float("%.0f"%(nQuote - rDiscount - dPeak)) 
        
        #...
        #... job cancellation 
        jobCancellation(instance)

 