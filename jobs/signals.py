from django.db.models.signals import post_save, pre_delete, pre_save 
from django.dispatch import receiver
from rest_framework.authentication import get_user_model

# ... 
        
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# ... import models 
from .models import Job #, Route
# from accounts.models import AccountProfile
# from referals.models import Referal
# .. utils 
from .g_quote import GenerateQuote

 
# ... is executed at the end
#  .. of the save method
# @receiver(post_save, sender = Job)
# def created_job(sender, instance = None, created = False, **kwargs):
#     if(created):
#         # .. compute customer name cName = Customer Name
#         cName = "{0} {1}".format(instance.customer.f_name, 
#                                  instance.customer.s_name)

#         # ... template data tData = template Data
#         templateData = {"id": instance.pk,
#                  "quote": instance.quote,
#                  "mDiscount": instance.middle_month_discount,
#                  "rCustomer": instance.return_customer_discount,
#                  "amountDue": instance.amount_due,
#                  "paymentOption": instance.payment_option,
#                  "cName": cName,
#                  "date": instance.job_date,
#                  "time": instance.job_time,
#                  "helpers": instance.helpers,
#                  "floors": instance.floors,
#                  "distance": instance.distance,
#                  "vSize": instance.vehicle_size,
#                  "jobLink": f"https://xcrossinglines.co.za/jobs/job/{instance.pk}/update"}

#                     # ... this is where I send the email
#         htmlContent = render_to_string("newJob.html", templateData)
#         textContent = strip_tags(htmlContent)

#                 #.. send email 
#         sendEmail = EmailMultiAlternatives(
#                     f"XCROSSING LINES TRANSPORT PTY(LTD) JOB INVOICE {instance.pk}",
#                     textContent, 
#                     settings.EMAIL_HOST_USER,
#                     ["u12318958@tuks.co.za", f"{instance.customer.email}", "xcrossinglines@gmail.com"]
#                 )

#         sendEmail.attach_alternative(htmlContent, "text/html")  
#         sendEmail.fail_silently = True
#         sendEmail.send()

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
                    ["u12318958@tuks.co.za", 
                     f"{instance.customer.email}", 
                     "xcrossinglines@gmail.com"])

        sendEmail.attach_alternative(htmlContent, "text/html")  
        sendEmail.fail_silently = True
        sendEmail.send()

# ... generate return customer discount 
def generate_return_customer_discount(nQuote, cUser, give_extra_discount):

    # ... zero
    zero_discount = 0.0
    
    # .. verify that cUser is of type get_user_model
    if(isinstance(cUser, get_user_model())):

        # .. verify that the customer is corperate 
        if(cUser.is_corperate):
            # .. continue 
            customerJobs = Job.\
                            objects.\
                                filter(customer = cUser)\
                                    .order_by('-created_at')
            
            # count 
            cJobCount = len(customerJobs)
            # .. reffer
            if(cJobCount >= 1): return nQuote*(5/100.0)

            # ... otherwise dont apply discount 
            return zero_discount
        
        # ... if requested to give extra discount 
        elif(give_extra_discount): return nQuote*(5/100.0)
        
        # ... otherwise dont give discount
        return zero_discount
    # ... otherwise 
    return zero_discount
 
 # .. send email 
def completed_job(instance):
    
    # .. first check if job complete 
    if(instance.job_completed):
        # .. check if feed back email was sent 
        if(instance.feedback_email_sent):return
        
        # .. check if usermodel is correct 
        if(isinstance(instance.account, get_user_model())):

            # .. here we send email to customer and admin
            # .. compute customer name cName = Customer Name
            cName = f"{0} {1}".format(instance.customer.f_name, 
                                    instance.customer.s_name)
            
            # ... template data tData = template Data
            templateData = {"cName": cName,
                            "feedbackLink": "https://xcrossinglines.co.za/feedback"}
            
            # ... this is where I send the email
            htmlContent = render_to_string("feedback.html", templateData)
            textContent = strip_tags(htmlContent)

                    #.. send email 
            sendEmail = EmailMultiAlternatives(
                        f"XCROSSING LINES TRANSPORT PTY(LTD) FEED BACK REQUEST",
                        textContent, 
                        settings.EMAIL_HOST_USER,
                        ["u12318958@tuks.co.za", 
                        f"{instance.customer.email}",])
            
            # .. send 
            sendEmail.attach_alternative(htmlContent, "text/html")  
            sendEmail.fail_silently = True
            sendEmail.send()
            
            # .. when done mark as sent
            instance.feedback_email_sent = True
            return # .. then break
        
        # .. cancel 
        return
    
    # ... break 
    return

# ... job invoice sent ? 
def job_invoice_issued(instance):

    # ... if invoice sent cancel execution
    if(instance.job_invoice_sent): return

    # ... 
    cName = "{0} {1}".format(instance.customer.f_name, 
                                instance.customer.s_name)

    # ... template data tData = template Data
    templateData = {"id": instance.pk,
                "quote": instance.quote,
                "mDiscount": instance.middle_month_discount,
                "rCustomer": instance.return_customer_discount,
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

    # ... toggle 
    instance.job_invoice_sent = True

#  .. executed at the beginning
#  .. of the save method
@receiver(pre_save, sender = Job)
def before_saved(sender, instance, *args, **kwargs):
    
    # ... check correct instance
    if(isinstance(instance, Job)):
        
        # .. compute distance 
        dStance = float("%.0f"%round(instance.distance))
    
        # .. generate instance 
        gQuoteClass = GenerateQuote(distance = dStance,
                                    floors = instance.floors,
                                    helpers = instance.helpers,
                                    vSize = instance.vehicle_size,
                                    job_date = instance.job_date,
                                    shuttle=instance.shuttle)
        # .. generated quote 
        customerQuote, peakDiscount = gQuoteClass.generate_quote_discount
    
        # .. apply return customer discount 
        rCustomerDiscount = generate_return_customer_discount((customerQuote -peakDiscount), 
                                                                instance.customer, 
                                                                instance.give_extra_discount)

        # .. set 
        instance.quote = float("%.0f"%round(customerQuote)) 
        instance.distance = float("%.0f"%round(dStance))
        instance.middle_month_discount = float("%.0f"%round(peakDiscount))
        instance.return_customer_discount = float("%.0f"%round(rCustomerDiscount))
        instance.amount_due = float("%.0f"%(customerQuote - peakDiscount - rCustomerDiscount)) 
        
        # ... send job invoice 
        job_invoice_issued(instance)
        
        # job completed 
        completed_job(instance)

        #... job cancellation 
        jobCancellation(instance)

 