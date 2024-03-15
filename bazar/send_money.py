from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SendMoney, Earning
from .forms import SendMoneyForm


@login_required
def send_money_list(request):
    send_transactions = SendMoney.objects.filter(sender=request.user)
    return render(request, 'send_money/send_money_list.html', {'send_transactions': send_transactions})

@login_required
def admin_send_money_list(request):
    send_transactions = SendMoney.objects.all()
    return render(request, 'send_money/admin_send_money_list.html', {'send_transactions': send_transactions})

@login_required
def send_money_detail(request, pk):
    send_money = get_object_or_404(SendMoney, pk=pk)
    return render(request, 'send_money/send_money_detail.html', {'send_money': send_money})

@login_required
def send_money_create(request):
    if request.method == 'POST':
        form = SendMoneyForm(request.POST, user=request.user)  
        if form.is_valid():
            sender_earning = Earning.objects.get_or_create(user=request.user)[0]
            if sender_earning.total_amount >= form.cleaned_data['amount']:
                form.save()
                return redirect('send_success')
            else:
                return redirect('insufficient_balance')
    else:
        form = SendMoneyForm(user=request.user)  
    return render(request, 'send_money/send_money_form.html', {'form': form})

@login_required
def send_money_update(request, pk):
    send_money = get_object_or_404(SendMoney, pk=pk)
    if request.method == 'POST':
        form = SendMoneyForm(request.POST, instance=send_money, user=request.user)  
        if form.is_valid():
            form.save()
            return redirect('send_money_list')
    else:
        form = SendMoneyForm(instance=send_money, user=request.user)  
    return render(request, 'send_money/send_money_form.html', {'form': form})


@login_required
def send_money_delete(request, pk):
    send_money = get_object_or_404(SendMoney, pk=pk)
    if request.method == 'POST':
        send_money.delete()
        return redirect('send_money_list')
    return render(request, 'send_money/send_money_confirm_delete.html', {'send_money': send_money})




@login_required
def insufficient_balance(request):
    return render(request, 'send_money/insufficient_balance.html')


@login_required
def send_success(request):
    return render(request, 'send_money/send_money_success.html')

