import reversion
from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    company = models.ForeignKey(Company, related_name='contacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=100, help_text="e.g., Primary, Billing")

    def __str__(self):
        return f"{self.name} ({self.company.name})"

@reversion.register()
class AMCContract(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Inactive', 'Inactive'),
        ('Draft', 'Draft'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('Paid', 'Paid'),
        ('Partially Paid', 'Partially Paid'),
        ('Unpaid', 'Unpaid'),
    )

    company = models.ForeignKey(Company, related_name='contracts', on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, through='ContractService')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Unpaid')
    auto_renew = models.BooleanField(default=False)
    tags = models.CharField(max_length=255, blank=True, help_text="e.g., Critical Client, High Value")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Contract for {self.company.name}"

class ContractService(models.Model):
    contract = models.ForeignKey(AMCContract, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ('contract', 'service')

    def __str__(self):
        return f"{self.service.name} in contract for {self.contract.company.name}"
