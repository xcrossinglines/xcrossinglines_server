
# third party
from django.conf import settings as _set
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import uuid

        
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created

# .. models 
from .models import AccountProfile, Account

# create signal  _set.AUTH_USER_MODEL
@receiver(post_save, sender = _set.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    
    # create token when user registers 
    if created:
        #Token.objects.create(user = instance)
        # we need to create user profile 
        try:
            #//generate uuid 
            referal_code = "{0}-{1}XCL"\
                    .format(str(uuid.uuid4())[:8], instance.id)\
                        .lower()
            
            #// create Account Profile
            AccountProfile\
                    .objects\
                        .create(account = instance,  
                                referal_code = referal_code)
                
            #.... send a welcome email to the customer
            if(isinstance(instance, Account)):

                # .. Customer Name = cName
                cName = "{0} {1}"\
                        .format(f"{instance.f_name}"\
                                    .capitalize(),
                                f"{instance.s_name}"\
                                    .capitalize())
                
                # ... template 
                templateData = {"cName": cName}

                # ... this is where I send the email
                htmlContent = render_to_string("newCustomer.html", templateData)
                textContent = strip_tags(htmlContent)

                #.. send email 
                sendEmail = EmailMultiAlternatives(
                    "XCROSSING LINES TRANSPORT PTY(LTD)",
                    textContent, 
                    settings.EMAIL_HOST_USER,
                    [f"{instance.email}"]
                )

                sendEmail.attach_alternative(htmlContent, "text/html")  
                sendEmail.fail_silently = True
                sendEmail.send()
                # ... 

        except Exception as e:
            return
        
    
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    templateData = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.f_name,
        'email': reset_password_token.user.email,
        
        'reset_password_url': "https://xlines.co.za/password/reset/{0}".format(reset_password_token.key)
    }
 
    # ... this is where I send the email
    htmlContent = render_to_string("resetPassword.html", templateData)
    textContent = strip_tags(htmlContent)

    #.. send email 
    sendEmail = EmailMultiAlternatives(
        "XCROSSING LINES TRANSPORT PTY(LTD)",
        textContent, 
        settings.EMAIL_HOST_USER,
        ["u12318958@tuks.co.za", f"{reset_password_token.user.email}"]
    )

    sendEmail.attach_alternative(htmlContent, "text/html")  
    sendEmail.fail_silently = True
    sendEmail.send()
