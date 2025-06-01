from django.db import models
from core_account.models import *

# ---------------------- #
# Trip Model             #
# ---------------------- #
class Trip(models.Model):
    agency = models.ForeignKey(AgencyProfile, on_delete=models.CASCADE, related_name='trips')
    destination = models.CharField(max_length=100)
    trip_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, default='USD')  # Added currency field

    def __str__(self):
        return f"Trip to {self.destination} on {self.trip_date}"

    class Meta:
        verbose_name = "Поездка"
        verbose_name_plural = "Поездки"