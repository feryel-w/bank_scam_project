from django.contrib import admin
from django.core.mail import send_mail
import random
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'email', 'id_number', 
        'is_suspected', 'is_blacklisted', 'is_verified', 'rib_code'
    )
    list_filter = ('is_suspected', 'is_blacklisted', 'is_verified')
    actions = ['verify_clients', 'blacklist_clients']

    def verify_clients(self, request, queryset):
        for customer in queryset:
            if not customer.is_verified and not customer.is_blacklisted:
                customer.is_verified = True
                # generate RIB
                customer.rib_code = "TN" + str(random.randint(10**19, 10**20 - 1))
                customer.save()

                send_mail(
                    subject="Votre RIB - BlueWave Bank",
                    message=(
                        f"Bonjour {customer.full_name},\n\n"
                        f"Votre compte a été approuvé après vérification.\n"
                        f"Voici votre RIB : {customer.rib_code}\n\n"
                        f"Merci,\nBlueWave Bank"
                    ),
                    from_email=None,
                    recipient_list=[customer.email],
                    fail_silently=False,
                )
        self.message_user(request, "Selected clients have been verified and RIB sent.")
    verify_clients.short_description = "Verify selected clients"

    def blacklist_clients(self, request, queryset):
        for customer in queryset:
            if not customer.is_blacklisted:
                customer.is_blacklisted = True
                customer.save()
        self.message_user(request, "Selected clients have been blacklisted.")
    blacklist_clients.short_description = "Blacklist selected clients"
