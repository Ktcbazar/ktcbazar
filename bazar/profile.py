from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile, AgentProfile, StaffProfile, EmployeeProfile, ten_Commission
from .forms import CustomerProfileForm, AgentProfileForm, StaffProfileForm, EmployeeProfileForm
from django.contrib import messages


@login_required
def customer_profile_list(request):
    profiles = CustomerProfile.objects.filter(user=request.user) 
    return render(request, 'customer_profile/customer_profile_list.html', {'profiles': profiles})

@login_required
def admin_customer_profile_list(request):
    profiles = CustomerProfile.objects.all()
    return render(request, 'customer_profile/admin_customer_profile_list.html', {'profiles': profiles})


@login_required
def create_customer_profile(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('customer_dashboard')
    else:
        form = CustomerProfileForm(user=request.user)
    return render(request, 'customer_profile/customer_create.html', {'form': form})



@login_required
def recharge_needed(request):
    return render(request, 'register_balance/recharge_needed.html')


@login_required
def read_customer_profile(request, pk):
    profile = get_object_or_404(CustomerProfile, pk=pk)
    return render(request, 'customer_profile/customer_detail.html', {'profile': profile})



@login_required
def update_customer_profile(request, pk):
    profile = get_object_or_404(CustomerProfile, pk=pk)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('read_customer_profile', pk=pk)
    else:
        form = CustomerProfileForm(instance=profile, user=request.user)
    return render(request, 'customer_profile/customer_update.html', {'form': form})



@login_required
def delete_customer_profile(request, pk):
    profile = get_object_or_404(CustomerProfile, pk=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('customer_dashboard')
    return render(request, 'customer_profile/customer_delete.html', {'profile': profile})



#....................................................................................................#
@login_required
def agent_profile_list(request):
    profiles = AgentProfile.objects.filter(user=request.user) 
    return render(request, 'agent_profile/agent_profile_list.html', {'profiles': profiles})

@login_required
def admin_agent_profile_list(request):
    profiles = AgentProfile.objects.all()
    return render(request, 'agent_profile/admin_agent_profile_list.html', {'profiles': profiles})

@login_required
def create_agent_profile(request):
    if request.method == 'POST':
        form = AgentProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('agent_dashboard')
    else:
        form = AgentProfileForm(user=request.user)
    return render(request, 'agent_profile/agent_create.html', {'form': form})

@login_required
def read_agent_profile(request, pk):
    profile = get_object_or_404(AgentProfile, user__pk=pk)
    return render(request, 'agent_profile/agent_detail.html', {'profile': profile})

@login_required
def update_agent_profile(request, pk):
    profile = get_object_or_404(AgentProfile, user__pk=pk)
    if request.method == 'POST':
        form = AgentProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('agent_profile_detail', pk=pk)
    else:
        form = AgentProfileForm(instance=profile, user=request.user)
    return render(request, 'agent_profile/agent_update.html', {'form': form})

@login_required
def delete_agent_profile(request, pk):
    profile = get_object_or_404(AgentProfile, user__pk=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('agent_dashboard')
    return render(request, 'agent_profile/agent_delete.html', {'profile': profile})

#....................................................................................................#

@login_required
def create_staff_profile(request):
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            staff_profile = form.save(commit=False)
            staff_profile.is_approved = False  
            staff_profile.save()
            referrer = request.user.referrer
            if referrer:
                ten_commission = ten_Commission.objects.create(
                    user=referrer,
                    registered_user=request.user,
                    generation=0,
                    amount=10.00,
                )
                ten_commission.save()
            if not staff_profile.is_approved:
                return redirect('waiting_for_approval')
            else:
                return redirect('admin_dashboard')
    else:
        form = StaffProfileForm(user=request.user)
    return render(request, 'staff_profile/staff_create.html', {'form': form})


@login_required
def staff_profile_list(request):
    profiles = StaffProfile.objects.filter(user=request.user) 
    return render(request, 'staff_profile/staff_profile_list.html', {'profiles': profiles})

@login_required
def admin_staff_profile_list(request):
    profiles = StaffProfile.objects.all()
    return render(request, 'staff_profile/admin_staff_profile_list.html', {'profiles': profiles})

@login_required
def read_staff_profile(request, pk):
    profile = get_object_or_404(StaffProfile, pk=pk)
    return render(request, 'staff_profile/staff_detail.html', {'profile': profile})

@login_required
def update_staff_profile(request, pk):
    profile = get_object_or_404(StaffProfile, pk=pk)
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('read_staff_profile', pk=pk)
    else:
        form = StaffProfileForm(instance=profile, user=request.user)
    return render(request, 'staff_profile/staff_update.html', {'form': form})

@login_required
def delete_staff_profile(request, pk):
    profile = get_object_or_404(StaffProfile, pk=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('admin_dashboard')  
    return render(request, 'staff_profile/staff_delete.html', {'profile': profile})


    
@login_required
def staff_approval_requests(request):
    if request.user.user_type in ['staff', 'employee']:
        pending_profiles = StaffProfile.objects.filter(is_approved=False)
        return render(request, 'staff_profile/staff_approval_requests.html', {'pending_profiles': pending_profiles})
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('admin_dashboard')

@login_required
def approve_staff_profile(request, user_id):
    if request.user.user_type in ['staff', 'employee']:
        profile = get_object_or_404(StaffProfile, user_id=user_id)
        profile.is_approved = True
        profile.save()
        messages.success(request, f'Staff profile for {profile.user.username} has been approved.')
        return redirect('staff_approval_requests')
    else:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('admin_dashboard')

@login_required
def reject_staff_profile(request, user_id):
    if request.user.user_type in ['staff', 'employee']:
        profile = get_object_or_404(StaffProfile, user_id=user_id)
        profile.delete()
        messages.success(request, f'Staff profile for {profile.user.username} has been rejected.')
        return redirect('staff_approval_requests')
    else:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('admin_dashboard')

#....................................................................................................#

@login_required
def create_employee_profile(request):
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            employee_profile = form.save(commit=False)
            employee_profile.save()
            referrer = request.user.referrer
            if referrer:
                ten_commission = ten_Commission.objects.create(
                    user=referrer,
                    registered_user=request.user,  
                    generation=0,  
                    amount=10.00,  
                )
                ten_commission.save()
            
            if not employee_profile.is_approved:
                return redirect('waiting_for_approval')  
                
            return redirect('employee_dashboard')
    else:
        form = EmployeeProfileForm(user=request.user)
    return render(request, 'employee_profile/employee_create.html', {'form': form})


@login_required
def employee_profile_list(request):
    profiles = EmployeeProfile.objects.filter(user=request.user) 
    return render(request, 'employee_profile/employee_profile_list.html', {'profiles': profiles})

@login_required
def admin_employee_profile_list(request):
    profiles = EmployeeProfile.objects.all()
    return render(request, 'employee_profile/admin_employee_profile_list.html', {'profiles': profiles})


@login_required
def read_employee_profile(request, pk):
    profile = get_object_or_404(EmployeeProfile, pk=pk)
    return render(request, 'employee_profile/employee_detail.html', {'profile': profile})

@login_required
def update_employee_profile(request, pk):
    profile = get_object_or_404(EmployeeProfile, pk=pk)
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('read_employee_profile', pk=pk)
    else:
        form = EmployeeProfileForm(instance=profile, user=request.user)
    return render(request, 'employee_profile/employee_update.html', {'form': form})

@login_required
def delete_employee_profile(request, pk):
    profile = get_object_or_404(EmployeeProfile, pk=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('employee_dashboard')  
    return render(request, 'employee_profile/employee_delete.html', {'profile': profile})



@login_required
def employee_approval_requests(request):
    if request.user.user_type in ['staff', 'admin']:
        pending_profiles = EmployeeProfile.objects.filter(is_approved=False)
        return render(request, 'employee_profile/employee_approval_requests.html', {'pending_profiles': pending_profiles})
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('admin_dashboard')

@login_required
def approve_employee_profile(request, user_id):
    if request.user.user_type in ['staff', 'admin']:
        profile = get_object_or_404(EmployeeProfile, user_id=user_id)
        profile.is_approved = True
        profile.save()
        messages.success(request, f'Employee profile for {profile.user.username} has been approved.')
        return redirect('employee_approval_requests')
    else:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('admin_dashboard')

@login_required
def reject_employee_profile(request, user_id):
    if request.user.user_type in ['staff', 'admin']:
        profile = get_object_or_404(EmployeeProfile, user_id=user_id)
        profile.delete()
        messages.success(request, f'Employee profile for {profile.user.username} has been rejected.')
        return redirect('employee_approval_requests')
    else:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('admin_dashboard')

#....................................................................................................#

