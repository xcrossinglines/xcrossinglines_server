from django.contrib import admin

# .. models 
from .models import Job, Route



# customize the admin panel
class JobAdminConfig(admin.ModelAdmin):
    
    readonly_fields = ('routes', 
                    #    'customer', 
                       'driver_note', 
                       'job_canceled',) 
      
    search_fields = ('id', 'pk' )

    ordering = ('-created_at', )
    
    list_filter =  ('job_completed',
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
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
    #     #// check 
    #     if(db_field.name == "assigned_driver"):
    #         kwargs["queryset"] = get_user_model().objects.filter(is_driver = True)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
    


# .. register models 
admin.site.register(Job, JobAdminConfig)
admin.site.register(Route)
