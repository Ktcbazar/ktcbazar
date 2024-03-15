from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, RegisterForm, CustomAuthenticationForm
from .models import CustomUser, Commission, CompanyCommission, RankCommission, ReferralCommission, CheckoutForm, Product, ProductCategory, ParentCategory
from django.db import transaction
from decimal import Decimal


def home(request):
    featured_products = Product.objects.filter(is_featured=True)
    arriavals_products = Product.objects.filter(is_arrival=True)
    
    context = {
        'featured_products': featured_products,
        'arriavals_products': arriavals_products,
    }

    return render(request, 'forntend/home.html', context)


def about_us(request):
    return render(request, 'forntend/about_us.html')


def how_we_work(request):
    return render(request, 'forntend/how_we_work.html')


def contact_us(request):
    return render(request, 'forntend/contact_us.html')


def become_marketer(request):
    return render(request, 'forntend/become_marketer.html')


def privacy_policy(request):
    return render(request, 'forntend/become_marketer.html')


def terms_of_use(request):
    return render(request, 'forntend/terms_of_use.html')


def notice_board(request):
    return render(request, 'forntend/notice_board.html')


def updates(request):
    return render(request, 'forntend/updates.html')


def partners(request):
    return render(request, 'forntend/partners.html')



BASE_URL = 'http://127.0.0.1:8000/'

def generate_referral_link(username):
    return f"{BASE_URL}referral/?ref={username}"

def calculate_commission(generation):
    if generation <= 8:
        return Decimal('0.04') * 100
    elif generation == 9:
        return Decimal('0.08') * 100
    elif generation == 10:
        return Decimal('0.20') * 100
    else:
        return Decimal('0')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.referral_link = generate_referral_link(user.username)
            user.save()
            referrer_username = request.GET.get('ref')
            if referrer_username:
                try:
                    referrer = CustomUser.objects.get(username=referrer_username)
                    user.referrer = referrer
                    user.save()
                    referrer.children.add(user)
                    referrer.save()
                except CustomUser.DoesNotExist:
                    pass
            return redirect('registration_success')  
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})



def referral(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request=request)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.referral_link = generate_referral_link(user.username)
                user.save()
                
                company_commission = CompanyCommission.objects.create(
                    registered_user=user,
                    amount=50  
                )
                company_commission.save()
                
                rank_amount = RankCommission.objects.create(
                    registered_user=user,
                    amount=20  
                )
                rank_amount.save()
                
                referrer_username = request.GET.get('ref')
                if referrer_username:
                    try:
                        referrer = CustomUser.objects.get(username=referrer_username)
                        user.referrer = referrer
                        user.save()
                        referrer.children.add(user)
                        referrer.save()
                        
                        referral_commission = ReferralCommission.objects.create(
                            referrer=referrer,
                            referred_user=user,
                            amount=30  
                        )
                        referral_commission.save()
                        
                        current_user = user
                        for generation in range(1, 11):
                            if referrer is not None:
                                commission_amount = calculate_commission(generation)
                                if referrer.amount is None:
                                    referrer.amount = commission_amount
                                else:
                                    referrer.amount += commission_amount
                                referrer.save()
                                Commission.objects.create(user=referrer, registered_user=user, generation=generation, amount=commission_amount)
                                
                                referrer = referrer.referrer
                            else:
                                break
                    except CustomUser.DoesNotExist:
                        pass
            return redirect('registration_success')
    else:
        form = RegisterForm(request=request)
    return render(request, 'registration/register_customer.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'staff':
                    return redirect('admin_dashboard')
                elif user.user_type == 'employee':
                    return redirect('employee_dashboard')
                elif user.user_type == 'agent':
                    return redirect('agent_dashboard')
                elif user.user_type == 'customer':
                    return redirect('customer_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def registration_success(request):
    return render(request, 'registration/registration_success.html')


@login_required
def waiting_for_approval(request):
    return render(request, 'registration/waiting_for_approval.html')


#....................................................................................................#
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import CustomPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password/password_reset_form.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'password/password_reset_email.html'
    success_url = '/password-reset/done/'
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password/password_reset_done.html'
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password/password_reset_confirm.html'
    success_url = '/password-reset/complete/'
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password/password_reset_complete.html'
    


#....................................................................................................#

@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')

@login_required
def employee_dashboard(request):
    return render(request, 'dashboard/employee_dashboard.html')

@login_required
def agent_dashboard(request):
    return render(request, 'dashboard/agent_dashboard.html')


@login_required
def customer_dashboard(request):
    return render(request, 'dashboard/customer_dashboard.html')

#....................................................................................................#
from .forms import DepartmentForm
from .models import Department

@login_required
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'data_input/create_department.html', {'form': form})


@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'data_input/department_list.html', {'departments': departments})


#....................................................................................................#
from .models import CheckoutForm, SaleReferralCommission, SaleRankCommission, SaleCompanyCommission, SaleCommission, DeliveryForm, CheckoutItem
from django.utils import timezone
from django.db.models import Sum

@login_required
def delivery_approval_requests(request):
    if request.user.user_type not in ['staff', 'employee']:
        return render(request, 'permission_denied.html')
    
    orders_to_approve = CheckoutForm.objects.filter(is_delivered=False)

    return render(request, 'shop/delivery_approval_requests.html', {'orders_to_approve': orders_to_approve})


@login_required
def approve_delivery(request, order_id):
    if request.user.user_type in ['staff', 'employee']:
        order = get_object_or_404(CheckoutForm, id=order_id)
        order.is_delivered = True
        order.save()
        
        referrer = order.user.referrer
        referred_user = order.user
        
        total_amount = 250
        quantity = CheckoutItem.objects.filter(checkout_form=order).aggregate(Sum('quantity'))['quantity__sum']
        
        referral_commission_amount = total_amount * Decimal('0.12') * quantity
        
        referral_commission_referrer = SaleReferralCommission.objects.create(
            referrer=referrer,
            referred_user=referred_user,
            amount=referral_commission_amount,
            created_at=timezone.now()
        )
        referral_commission_referrer.save()
        
        current_user = referred_user
        total_amount = 250
        for generation in range(1, 11):
            if referrer is not None:
                commission_percentage = calculate_commission(generation)
                commission_amount = total_amount * commission_percentage / 100 * quantity
                
                if referrer.amount is None:
                    referrer.amount = commission_amount
                else:
                    referrer.amount += commission_amount
                referrer.save()
                
                SaleCommission.objects.create(
                    user=referrer,
                    registered_user=current_user,
                    generation=generation,
                    amount=commission_amount,
                    created_at=timezone.now()
                )
                
                referrer = referrer.referrer
            else:
                break
            
        rank_commission_amount = total_amount * Decimal('0.08') * quantity
        
        SaleRankCommission.objects.create(
            registered_user=referred_user,
            rank="0",  
            amount=rank_commission_amount,  
            created_at=timezone.now()
        )
        
        company_commission_amount = total_amount * Decimal('0.20') * quantity
        
        SaleCompanyCommission.objects.create(
            registered_user=referred_user,
            amount=company_commission_amount,  
            created_at=timezone.now()
        )
        
        
    return redirect('delivery_approval_requests')


@login_required
def reject_delivery(request, order_id):
    if request.user.user_type in ['staff', 'employee']:
        order = get_object_or_404(CheckoutForm, id=order_id)
        order.delete()
    return redirect('delivery_approval_requests')


#....................................................................................................#
@login_required
def shipped_approval_requests(request):
    if request.user.user_type in ['staff', 'employee']:
        pending_deliveries = DeliveryForm.objects.filter(is_shipped=False)
        return render(request, 'shop/shipped_requests.html', {'pending_deliveries': pending_deliveries})
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('shipped_approval_requests')

from .models import SaleCommission, Earning

@login_required
def approve_shipped(request, delivery_id):
    if request.user.user_type in ['staff', 'employee']:
        delivery = get_object_or_404(DeliveryForm, id=delivery_id)
        delivery.is_shipped = True
        delivery.delivery_status = 'Delivered'  
        delivery.save()     
        
        messages.success(request, f'Delivery {delivery.id} has been approved.')
        return redirect('shipped_approval_requests')
    else:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('shipped_approval_requests')

@login_required
def reject_shipped(request, delivery_id):
    if request.user.user_type in ['staff', 'employee']:
        delivery = get_object_or_404(DeliveryForm, id=delivery_id)
        delivery.delete()
        messages.success(request, f'Delivery {delivery.id} has been rejected.')
        return redirect('shipped_approval_requests')
    else:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('shipped_approval_requests') 

#....................................................................................................#
# Chnage Password

from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy



class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'password/change_password.html'
    success_url = reverse_lazy('password_change_success')  
    
    
    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data['new_password1'])
        self.request.user.save()
        messages.success(self.request, 'Your password has been changed successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid form submission. Please correct the errors.')
        return super().form_invalid(form)



@login_required
def password_change_success(request):
    return render(request, 'password/password_change_success.html')

#....................................................................................................#


@login_required
def downline(request, referrer_id):
    depth = 10 
    downline_users = []

    def get_downline(referrer, current_depth):
        if current_depth > depth:
            return
        downline = CustomUser.objects.filter(referrer=referrer)
        for user in downline:
            downline_users.append((user, current_depth))
            get_downline(user, current_depth + 1)

    referrer = CustomUser.objects.get(id=referrer_id)
    get_downline(referrer, 1)
    downline_users_with_depth = [(user, depth + 1) for user, depth in downline_users]

    return render(request, 'tree/downline.html', {'referrer': referrer, 'downline_users': downline_users_with_depth})