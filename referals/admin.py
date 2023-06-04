from django.contrib import admin

#// models 
from .models import Referal



# customize the admin panel
class ReferalPanelAdminConfig(admin.ModelAdmin):
    
    readonly_fields = ('account', 'referal_code', 'referal_discount',) 
      
    search_fields = ('id', 'referal_code',  )

    ordering = ('-created_at', )
    
    list_filter =  ('referal_code',)
    
    list_display = ('id',
                    'referal_code', 
                    'account',
                    'referal_discount',)
    
    # # # check new
    add_fieldsets = (
        (None, { 
            'classes': ('wide',),
            'fields': ('id',
                    'referal_code', 
                    'account',
                    'referal_discount',),
        }),
    )
    


#register model 
admin.site.register(Referal, ReferalPanelAdminConfig)