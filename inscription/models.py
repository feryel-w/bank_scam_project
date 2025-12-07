from django.db import models

class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)

    nationality = models.CharField(max_length=100)
    residence_country = models.CharField(max_length=100)

    phone = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()

    profession = models.CharField(max_length=255)
    revenue = models.IntegerField()
    source_of_income = models.CharField(max_length=100)
    account_purpose = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)

    id_type = models.CharField(max_length=50)
    id_number = models.CharField(max_length=255)

    # Fraud detection fields
    # ... your existing fields ...

    is_suspected = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # new field
    rib_code = models.CharField(max_length=50, blank=True, null=True)



    # Optional admin info
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.id_number}"
