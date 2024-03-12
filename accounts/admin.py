from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# local imports 
from .models import Account, AccountProfile

# customize the admin panel
class UserAdminConfig(UserAdmin):
    
    readonly_fields = ('email', 'f_name', 's_name', 'm_number', 'register_method',)
    
    search_fields = ('id',
                    'email',
                    'f_name',
                    'register_method',)
    
    list_filter = ('email',
                   'f_name',
                   'is_active',
                   'register_method',)
                   
    ordering = ('-d_joined', )
    
    list_display = ('email',
                    'f_name', 
                    's_name', 
                    'is_active', 
                    'is_staff',
                    'register_method',
                    'd_joined',
                    )
    
    fieldsets = (
        (None, {'fields': ('email',
                           'f_name', 
                           's_name',
                           'm_number',
                           'register_method',
                           'password',)}),
        
        ('Permissions', {'fields': ('is_staff',
                                    'is_active',
                                    'verified',
                                    'is_superuser',
                                    'is_corperate',
                                    'customer',
                                    'driver',)}),
        
        #('Personal', {'fields': ('pdf_id_copy',
        #                                 'pdf_drivers_license_copy',)})
    )
    
    # check new
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'f_name',
                       's_name',
                       'password1',
                       'password2',
                        'is_active',
                        'is_staff',
                        'verified', 
                        'is_corperate'),
        }),
    )
    
    
# customize the admin panel
class AccountProfileAdminConfig(admin.ModelAdmin):
     
    readonly_fields = ('use_crossing_lines_for',
                        'id_number', 'account', 'referal_code',)
    
    search_fields = ('id_number',
                     'id',
                  )
    
    list_filter = ('account',
                   'id_number',)
    
    ordering = ('-created_at', )
    
    list_display = ('account',
                    'id_number', 
                    'created_at',)
        # # check new
    add_fieldsets = (
        (None, { 
            'classes': ('wide',),
            'fields': ('account', 
                    'id_number', 
                    'created_at'),
        }),
    )


# register to the site 
admin.site.register(Account, UserAdminConfig)
admin.site.register(AccountProfile, AccountProfileAdminConfig)
