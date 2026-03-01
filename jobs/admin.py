from django.contrib import admin

# .. models
from rest_framework.authentication import get_user_model
from .models import Job, Route

# from django.contrib.admin.widgets import AdminTimeWidget
from django import forms


class JobAdminForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = "__all__"
        widgets = {
            "job_time": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
        }


# customize the admin panel
class JobAdminConfig(admin.ModelAdmin):

    form = JobAdminForm

    readonly_fields = (
        "customer",
        # 'job_date',
        # 'job_time',
        "created_at",
        "base_fee",
        "amount_due",
        "mid_discount",
        "extra_discount",
        "return_customer_discount",
        "referal_discount",
        "payment_option",
        "shuttle",
        "routes",
        "distance",
        "driver_note",
        # 'job_canceled',
        "set_price_adjustment",
        "price_adjustment_justification",
        "job_out_sourced",
        "feedback_email_sent",
        "extra_discount_pecentage",
        "job_cancellation_feedback_sent",
        "extra_discount",
        "give_extra_discount",
        "job_invoice_sent",
        "referal_code",
        "hear_about_us",
    )

    search_fields = (
        "id",
        "pk",
    )

    ordering = ("-created_at",)

    list_filter = (
        "job_completed",
        "job_out_sourced",
        "job_canceled",
        "vehicle_size",
    )

    list_display = (
        "id",
        "customer",
        "vehicle_size",
        "amount_due",
        "base_fee",
        "job_date",
        "job_time",
        "job_completed",
    )

    # # # check new
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "id",
                    "customer",
                    "vehicle_size",
                    "amount_due",
                    "base_fee",
                    "distance",
                    "job_date",
                    "job_time",
                ),
            },
        ),
    )

    # // override as intructed
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # // check
        if db_field.name == "driver":
            kwargs["queryset"] = get_user_model().objects.filter(driver=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# customize the admin panel
class RoutesAdminConfig(admin.ModelAdmin):

    readonly_fields = (
        "route_name",
        "lat",
        "lng",
        "description",
    )

    search_fields = (
        "id",
        "pk",
    )

    ordering = ("-created_at",)

    list_filter = ("id",)

    list_display = (
        "id",
        "route_name",
        "created_at",
    )

    # # # check new
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "id",
                    "lat",
                    "lng",
                    "route_name",
                    "description",
                    "created_at",
                ),
            },
        ),
    )


# .. register models
admin.site.register(Job, JobAdminConfig)
admin.site.register(Route, RoutesAdminConfig)
