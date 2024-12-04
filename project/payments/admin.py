from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_id', 'amount', 'status', 'payment_date')
    search_fields = ('transaction_id', 'user__username')
    list_filter = ('status', 'payment_date')


