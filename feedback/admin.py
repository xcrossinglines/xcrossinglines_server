from django.contrib import admin

# models 
from .models import FeedBack


# customize the admin panel
class FeedBackAdminConfig(admin.ModelAdmin):
     
    readonly_fields = ('customer_id',
                        'service_commentry', 
                        'website_commentry', 
                        'service_rating',
                        'website_rating',)
    
    search_fields = ('customer_id', )
    
    list_filter = ('customer_id', )
    
    ordering = ('-created_at', )
    
    list_display = ('customer_id',
                    'service_commentry', 
                    'website_commentry',
                    'created_at',)
        # # check new
    add_fieldsets = (
        (None, { 
            'classes': ('wide',),
            'fields': ('customer_id', 
                    'service_commentry', 
                    'created_at'),
        }),
    )


# .. register 
admin.site.register(FeedBack, FeedBackAdminConfig)