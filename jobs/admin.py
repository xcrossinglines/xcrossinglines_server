from django.contrib import admin

# .. models 
from rest_framework.authentication import get_user_model
from .models import Job, Route



# customize the admin panel
class JobAdminConfig(admin.ModelAdmin):
    
    readonly_fields = (
                    'customer', 
                    'job_date',
                    'job_time',
                    'quote',
                    'amount_due',
                    'middle_month_discount',
                    'return_customer_discount', 
                    'referal_discount',
                    'payment_option',
                    'routes', 
                    'distance',
                    'driver_note', 
                    'job_canceled',
                    'feedback_email_sent',
                    'job_invoice_sent',
                    'referal_code',
                    'driver_note',
                    'hear_about_us',) 
      
    search_fields = ('id', 'pk',  )

    ordering = ('-created_at', )
    
    list_filter =  ('job_completed',
                    'job_out_sourced',
                    'job_canceled',
                    'vehicle_size',)
    
    list_display = ('id',
                    'customer', 
                    'vehicle_size', 
                    'quote', 
                    'job_date',
                    'job_time',
                    'job_completed',
                   )
    
    # # # check new
    add_fieldsets = (
        (None, { 
            'classes': ('wide',),
            'fields': ('id',
                    'customer', 
                    'vehicle_size', 
                    'quote', 
                    'distance',
                    'job_date',
                    'job_time',
                        ),
        }),
    )
    
    #// override as intructed 
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        #// check 
        if(db_field.name == "driver"):
            kwargs["queryset"] = get_user_model().objects.filter(driver = True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

# customize the admin panel
class RoutesAdminConfig(admin.ModelAdmin):
    
    readonly_fields = ('route_name', 'lat', 'lng',) 
      
    search_fields = ('id', 'pk',  )

    ordering = ('-created_at', )
    
    list_filter =  ('id',)
    
    list_display = ('id',
                    'route_name', 
                    'created_at',)
    
    # # # check new
    add_fieldsets = (
        (None, { 
            'classes': ('wide',),
            'fields': ('id',
                        'lat', 
                        'lng', 
                        'route_name', 
                        'created_at',),
        }),
    )
    

# .. register models 
admin.site.register(Job, JobAdminConfig)
admin.site.register(Route, RoutesAdminConfig)
