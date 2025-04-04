from django.db.models.signals import post_save, pre_save 
from django.dispatch import receiver
from rest_framework.authentication import get_user_model

# ... 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# ... import models 
from .models import Job #, Route

# .. utils 
from generate_quote.generate_quote import GenerateQuote
from generate_quote.variables import  RETURN_CUSTOMER_DISCOUNT, DATE_TIME_FORMAT

# packages 
from datetime import datetime


# invalid changes 
def _date_past(instance):
    # ....
    date = "{0} {1}".format(instance.job_date, instance.job_time) # string respresentation 

    # .. epocs 
    date_epochs = datetime.\
                    strptime(date, DATE_TIME_FORMAT).\
                    timestamp() # job date time epochs 
    current_datetime_epochs = datetime.now().timestamp() # current time 
    # evalute date passed 
    return True if ((date_epochs - current_datetime_epochs) < 0) else False


    

# update prices 
def valid_update(instance):
    # evaluate 
    if(instance.job_completed or 
                instance.job_canceled or 
                        _date_past(instance)): return False
    return True

# generate extra given discount 
def generate_extra_given_discount(instance, quote):
    # default extra discount 
    extra_discount_amount = 0.0
    # check extra discount 
    if(instance.give_extra_discount):
        # customer given 
        extra_discount_amount = quote*((instance.extra_discount_pecentage)/100.0)
        return extra_discount_amount
    # otherwise 
    return extra_discount_amount

# generate price adjustment 
def generate_price_adjustment(instance):
    
    # default price adjustment 
    price_adjustment = 0.0
    # issue price adjustment 
    if(instance.set_price_adjustment and 
            isinstance(instance.price_adjustment, type(None)) == False):
        # set price
        price_adjustment = instance.price_adjustment
        return price_adjustment
    
    #otherwise 
    return price_adjustment

# ... job invoice sent ? 
def job_invoice_issue(instance):

    # ... if invoice sent cancel execution
    if(instance.job_invoice_sent 
       or isinstance(instance.pk, type(None))): return
    
    # ... 
    cName = "{0} {1}".format(instance.customer.f_name, 
                                instance.customer.s_name)

    # ... template data tData = template Data
    templateData = {"id": instance.pk,
                "quote": instance.base_fee,
                "mDiscount": instance.mid_discount,
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
                "jobLink": f"https://xlines.co.za/jobs/job/{instance.pk}/update"}

                # ... this is where I send the email
    htmlContent = render_to_string("newJob.html", templateData)
    textContent = strip_tags(htmlContent)

            #.. send email 
    sendEmail = EmailMultiAlternatives(
                f"XCROSSING LINES TRANSPORT PTY(LTD) JOB INVOICE {instance.pk}",
                textContent, 
                settings.EMAIL_HOST_USER,
                [f"{instance.customer.email}", "xcrossinglines@gmail.com"]
            )

    sendEmail.attach_alternative(htmlContent, "text/html")  
    sendEmail.fail_silently = True
    sendEmail.send()

    # ... toggle 
    instance.job_invoice_sent = True




# ... Job Cancellation
def jobCancellation(instance):

    #.. check job cancelled
    if(instance.job_canceled and 
        instance.job_cancellation_feedback_sent == False):
        # .. here we send email to customer and admin
        # .. compute customer name cName = Customer Name
        cName = "{0} {1}".format(instance.customer.f_name, 
                                 instance.customer.s_name)
        
        # ... template data tData = template Data
        templateData = {"id": instance.pk,
                        "cName": cName,
                        "jobLink": f"https://xlines.co.za/jobs/job/{instance.pk}/update"}
        
        # ... this is where I send the email
        htmlContent = render_to_string("cancelledJob.html", templateData)
        textContent = strip_tags(htmlContent)

        #.. send email 
        sendEmail = EmailMultiAlternatives(
                    f"XCROSSING LINES TRANSPORT PTY(LTD) JOB CANCELLATION",
                    textContent, 
                    settings.EMAIL_HOST_USER,
                    [f"{instance.customer.email}", 
                     "xcrossinglines@gmail.com"])

        sendEmail.attach_alternative(htmlContent, "text/html")  
        sendEmail.fail_silently = True
        sendEmail.send()

        # .. toggle
        instance.job_cancellation_feedback_sent = True

# ... generate return customer discount 
def generate_return_customer_discount(new_quote, user_account):

    # ... zero
    zero_discount = 0.0

    # ... end it right there 
    if(user_account.is_superuser): return zero_discount

    # .. verify that cUser is of type Account model
    if(isinstance(user_account, get_user_model())):

        # .. continue 
        customerJobs = Job.\
                        objects.\
                            filter(customer = user_account)\
                                .order_by('-created_at')
    
        # .. reffer
        if(len(customerJobs) > 1): return new_quote*(RETURN_CUSTOMER_DISCOUNT/100.0)

        # ... otherwise dont apply discount 
        return zero_discount
        
    # ... otherwise 
    return zero_discount
 
 # .. send email 
def completed_job(instance):
    
    # .. first check if job complete 
    if(isinstance(instance, Job)):
        # .. is job
        if(instance.job_completed):
            # .. check if usermodel is correct 
            if(isinstance(instance.customer, get_user_model())):
                # .. compute customer name cName = Customer Name
                cName = "{0} {1}".format(instance.customer.f_name, 
                                        instance.customer.s_name)
                
                # ... template data tData = template Data
                templateData = {"cName": cName,
                                "feedbackLink": "https://xlines.co.za/feedback"}
                
                # ... this is where I send the email
                htmlContent = render_to_string("feedback.html", templateData)
                textContent = strip_tags(htmlContent)

                #.. send email 
                sendEmail = EmailMultiAlternatives(
                            "XCROSSING LINES TRANSPORT PTY(LTD) FEED BACK REQUEST",
                            textContent, 
                            settings.EMAIL_HOST_USER,
                            [f"{instance.customer.email}"])
                
                # .. send 
                sendEmail.attach_alternative(htmlContent, "text/html")  
                sendEmail.fail_silently = True
                sendEmail.send()
                
                # .. when done mark as sent
                instance.feedback_email_sent = True
                print("Are we even running this block of code 123211")
                
                return # .. then break
            # .. cancel 
            return
        # ... break 
        return

# ... executed after the model is saved 
# ... of the save method
@receiver(post_save, sender = Job)
def created_job(sender, instance = None, created = False, **kwargs):
    # ... activate when created is true 
    if(created):
        # ... send the email 
        job_invoice_issue(instance)
        instance.job_invoice_sent = True
        instance.save()

#  .. executed before the model is saved 
#  .. of the save method
@receiver(pre_save, sender = Job)
def before_saved(sender, instance, *args, **kwargs):
    # validate 
    update = valid_update(instance)
    # ... check correct instance
    if(isinstance(instance, Job) and update):
        
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
        customerQuote, mid_discount = gQuoteClass.generate_pricing
    
        # .. apply return customer discount 
        rCustomerDiscount = generate_return_customer_discount((customerQuote - mid_discount), 
                                                                instance.customer)
        
        # generate extra given discount 
        extra_discount_amount = generate_extra_given_discount(instance, 
                                                              (customerQuote - 
                                                                mid_discount - 
                                                                rCustomerDiscount))
        
        price_adjustment = generate_price_adjustment(instance)

        #... set     
        instance.base_fee = float("%.0f"%round(customerQuote)) 
        instance.distance = float("%.0f"%round(dStance))
        instance.mid_discount = float("%.0f"%round(mid_discount))
        instance.return_customer_discount = float("%.0f"%round(rCustomerDiscount))
        instance.extra_discount = float("%.0f"%round(extra_discount_amount))
        instance.amount_due = float("%.0f"%(price_adjustment + 
                                            (customerQuote - 
                                            mid_discount - 
                                            rCustomerDiscount - 
                                            extra_discount_amount))) 
        #........... 
        job_invoice_issue(instance)
        completed_job(instance)
        jobCancellation(instance)

 