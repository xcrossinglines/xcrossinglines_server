from django.contrib import admin

# Register your models here.
from .models import QuoteJob, QuoteRoutes



class QuoteJobAdminConfig(admin.ModelAdmin):

    readonly_fields = (
                    "id", 
                    "distance",
                    "shuttle",
                    "routes",
                    "driver_note",
                    "base_fee",
                    "amount_due",
                    "mid_discount",
                    "created_at",
                    "updated_at"
            )
    
    search_fields = ('id', 'pk',  )
    ordering = ('-created_at', )
    list_filter =  ('id',)
    list_display = ('id',
                    'vehicle_size', 
                    'base_fee', 
                    'job_date',
                    'job_time',
                   )
        # # # check new
    add_fieldsets = (
        (None, { 
            'classes': ('wide',),
            'fields': ('id', 
                    'vehicle_size', 
                    'base_fee', 
                    'distance',
                    'job_date',
                    'job_time',
                        ),
        }),
    )
    
        

# customize the admin panel
class QuoteRoutesAdminConfig(admin.ModelAdmin):
    
    readonly_fields = ('id', 'route_name', 'lat', 'lng',) 
      
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
    




admin.site.register(QuoteJob, QuoteJobAdminConfig)
admin.site.register(QuoteRoutes, QuoteRoutesAdminConfig)
