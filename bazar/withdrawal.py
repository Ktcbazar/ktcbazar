from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Withdrawal, UserBalance
from .forms import WithdrawalForm
from django.contrib import messages 
from django.core.exceptions import ObjectDoesNotExist


@login_required
def withdrawal_list(request):
    withdrawals = Withdrawal.objects.filter(user=request.user)
    return render(request, 'withdrawal/withdrawal_list.html', {'withdrawals': withdrawals})


@login_required
def admin_withdrawal_list(request):
    withdrawals = Withdrawal.objects.all()
    return render(request, 'withdrawal/admin_withdrawal_list.html', {'withdrawals': withdrawals})


@login_required
def withdrawal_detail(request, pk):
    withdrawal = get_object_or_404(Withdrawal, pk=pk)
    return render(request, 'withdrawal/withdrawal_detail.html', {'withdrawal': withdrawal})




@login_required
def withdrawal_create(request):
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user
            try:
                user_balance = UserBalance.objects.get(user=request.user)
            except ObjectDoesNotExist:
                user_balance = UserBalance.objects.create(user=request.user, balance=0)

            if user_balance.balance < withdrawal.amount:
                messages.error(request, "Insufficient balance.")
                return redirect('insufficient_balance')  
                
            withdrawal.save()
            if withdrawal.is_approved:
                user_balance.balance -= withdrawal.amount
                user_balance.save()
                
            return redirect('withdrawal_list')
    else:
        form = WithdrawalForm()
    return render(request, 'withdrawal/withdrawal_form.html', {'form': form})

@login_required
def withdrawal_update(request, pk):
    withdrawal = get_object_or_404(Withdrawal, pk=pk)
    if request.method == 'POST':
        form = WithdrawalForm(request.POST, instance=withdrawal)
        if form.is_valid():
            form.save()
            return redirect('withdrawal_list')
    else:
        form = WithdrawalForm(instance=withdrawal)
    return render(request, 'withdrawal/withdrawal_form.html', {'form': form})


@login_required
def withdrawal_delete(request, pk):
    withdrawal = get_object_or_404(Withdrawal, pk=pk)
    if request.method == 'POST':
        withdrawal.delete()
        return redirect('withdrawal_list')
    return render(request, 'withdrawal/withdrawal_confirm_delete.html', {'withdrawal': withdrawal})



@login_required
def withdrawal_approval_requests(request):
    if request.user.user_type in ['staff', 'employee']:
        pending_withdrawals = Withdrawal.objects.filter(status='pending')
        return render(request, 'withdrawal/withdrawal_approval_requests.html', {'pending_withdrawals': pending_withdrawals})
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('withdrawal_list') 

@login_required
def approve_withdrawal(request, withdrawal_id):
    if request.user.user_type in ['staff', 'employee']:
        withdrawal = get_object_or_404(Withdrawal, id=withdrawal_id)
        withdrawal.is_approved = True
        withdrawal.status = 'paid'  
        withdrawal.save()
        
        messages.success(request, f'Withdrawal {withdrawal_id} has been approved and marked as paid.')
        return redirect('withdrawal_list')
    else:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('withdrawal_approval_requests')

@login_required
def reject_withdrawal(request, withdrawal_id):
    if request.user.user_type in ['staff', 'employee']:
        withdrawal = get_object_or_404(Withdrawal, id=withdrawal_id)
        withdrawal.status = 'cancelled'  
        withdrawal.save()
        
        messages.success(request, f'Withdrawal {withdrawal_id} has been rejected and marked as cancelled.')
        return redirect('withdrawal_list')
    else:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('withdrawal_approval_requests')