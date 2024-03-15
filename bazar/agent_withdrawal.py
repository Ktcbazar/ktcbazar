from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AgentWithdrawal, AgentCommission
from .forms import AgentWithdrawalForm
from django.contrib import messages 


@login_required
def agent_withdrawal_list(request):
    agent_withdrawals = AgentWithdrawal.objects.filter(user=request.user)
    return render(request, 'agent_withdrawal/agent_withdrawal_list.html', {'agent_withdrawals': agent_withdrawals})


@login_required
def admin_agent_withdrawal_list(request):
    agent_withdrawals = AgentWithdrawal.objects.all()
    return render(request, 'agent_withdrawal/admin_agent_withdrawal_list.html', {'agent_withdrawals': agent_withdrawals})


@login_required
def agent_withdrawal_detail(request, pk):
    agent_withdrawal = get_object_or_404(AgentWithdrawal, pk=pk)
    return render(request, 'agent_withdrawal/agent_withdrawal_detail.html', {'agent_withdrawal': agent_withdrawal})


@login_required
def agent_withdrawal_create(request):
    if request.method == 'POST':
        form = AgentWithdrawalForm(request.POST)
        if form.is_valid():
            agent_withdrawal = form.save(commit=False)
            agent_withdrawal.user = request.user
            
            agent_commission = AgentCommission.objects.filter(agent=request.user.agent_profile).last()
            if agent_commission and agent_commission.total_amount < agent_withdrawal.amount:
                messages.error(request, "Insufficient balance.")
                return redirect('insufficient_balance')  
                
            agent_withdrawal.save()
            return redirect('agent_withdrawal_list')
    else:
        form = AgentWithdrawalForm()
    return render(request, 'agent_withdrawal/agent_withdrawal_form.html', {'form': form})


@login_required
def agent_withdrawal_update(request, pk):
    agent_withdrawal = get_object_or_404(AgentWithdrawal, pk=pk)
    if request.method == 'POST':
        form = AgentWithdrawalForm(request.POST, instance=agent_withdrawal)
        if form.is_valid():
            form.save()
            return redirect('agent_withdrawal_list')
    else:
        form = AgentWithdrawalForm(instance=agent_withdrawal)
    return render(request, 'agent_withdrawal/agent_withdrawal_form.html', {'form': form})

@login_required
def agent_withdrawal_delete(request, pk):
    agent_withdrawal = get_object_or_404(AgentWithdrawal, pk=pk)
    if request.method == 'POST':
        agent_withdrawal.delete()
        return redirect('agent_withdrawal_list')
    return render(request, 'agent_withdrawal/agent_withdrawal_confirm_delete.html', {'agent_withdrawal': agent_withdrawal})




@login_required
def agent_withdrawal_requests(request):
    if request.user.user_type not in ['staff', 'employee']:
        return render(request, 'permission_denied.html')
    
    withdrawal_requests = AgentWithdrawal.objects.filter(is_approved=False)
    
    return render(request, 'agent_withdrawal/agent_withdrawal_requests.html', {'withdrawal_requests': withdrawal_requests})



@login_required
def approve_agent_withdrawal(request, withdrawal_id):
    if request.user.user_type in ['staff', 'employee']:
        withdrawal = get_object_or_404(AgentWithdrawal, id=withdrawal_id)
        withdrawal.is_approved = True
        withdrawal.status = 'approved'
        withdrawal.save()
        
        
    return redirect('agent_withdrawal_requests')

@login_required
def reject_agent_withdrawal(request, withdrawal_id):
    if request.user.user_type in ['staff', 'employee']:
        withdrawal = get_object_or_404(AgentWithdrawal, id=withdrawal_id)
        withdrawal.delete()
        
        
    return redirect('agent_withdrawal_requests')