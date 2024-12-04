from django.db import models
from django.contrib.auth.models import User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('Pending', 'Pending'), ('Completed', 'Completed')),
                              default='Pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def _str_(self):
        return f"{self.user.username} - {self.transaction_id}"



