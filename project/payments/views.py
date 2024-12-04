from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from .forms import PaymentForm

@login_required
def payment_list(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'payment/payment_list.html', {'payments': payments})

@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk, user=request.user)
    return render(request, 'payment/payment_detail.html', {'payment': payment})

@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'payment/payment_form.html', {'form': form})

@login_required
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'payment/payment_form.html', {'form': form})

@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk, user=request.user)
    if request.method == 'POST':
        payment.delete()
        return redirect('payment_list')
    return render(request, 'payment/payment_confirm_delete.html', {'payment': payment})