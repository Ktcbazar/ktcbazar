from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Department


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email')


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegisterForm, self).__init__(*args, **kwargs)
        if self.request:
            logged_user = self.request.user
            if logged_user:
                used_placements = CustomUser.objects.filter(parent=logged_user).values_list('placement', flat=True)
                self.fields['placement'].choices = [(choice[0], choice[1]) for choice in self.fields['placement'].choices if choice[0] not in used_placements]

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'placement','user_type')
        


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        
#....................................................................................................#

from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['email'].label = 'Enter your email'
        self.fields['email'].widget.attrs['placeholder'] = 'Your email address'        
        

#....................................................................................................#

from django import forms
from .models import CustomerProfile, AgentProfile, StaffProfile, EmployeeProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CustomerProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].queryset = User.objects.filter(pk=user.pk)

    class Meta:
        model = CustomerProfile
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        

class AgentProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AgentProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].queryset = User.objects.filter(pk=user.pk)
            
    class Meta:
        model = AgentProfile
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
class StaffProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(StaffProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].queryset = User.objects.filter(pk=user.pk)
            
    class Meta:
        model = StaffProfile
        fields = ['user','bio', 'profile_image', 'phone_number', 'date_of_birth', 'address', 'district', 'zipcode', 'country', 'nid_number', 'nid_front_image', 'nid_back_image', 'is_updated']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        

class EmployeeProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EmployeeProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].queryset = User.objects.filter(pk=user.pk)
            
            
    class Meta:
        model = EmployeeProfile
        fields = ['user', 'department', 'profile_image', 'phone_number', 'date_of_birth', 'address', 'district', 'zipcode', 'country', 'nid_number', 'nid_front_image', 'nid_back_image', 'is_updated']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        
#....................................................................................................#

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        
#....................................................................................................#
from .models import Supplier, ParentCategory, ProductCategory, Product

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone_number', 'address']
        
class ParentCategoryForm(forms.ModelForm):
    class Meta:
        model = ParentCategory
        fields = ['name']      
          

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['parent_category', 'name',  'agent_commission' ,'description']
        
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

#....................................................................................................#
from .models import CheckoutForm, DeliveryForm, SendMoney, Earning, PaymentMethod, Withdrawal, AgentWithdrawal


class CheckoutFormModelForm(forms.ModelForm):
    class Meta:
        model = CheckoutForm
        fields = ['full_name', 'email', 'phone_number', 'address', 'city', 'postal_code', 'country','order_notes']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CheckoutFormModelForm, self).__init__(*args, **kwargs)
        
    

    def save(self, commit=True):
        instance = super(CheckoutFormModelForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance


# class DeliveryFormForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)  
#         super().__init__(*args, **kwargs)
#         if user:
#             self.fields['user'].initial = user  
#             self.fields['user'].queryset = user.__class__.objects.filter(pk=user.pk)  

#     class Meta:
#         model = DeliveryForm
#         fields = ['user', 'checkout_form', 'agent', 'delivery_method', 'delivery_status']


class DeliveryFormForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['user'].initial = user  
            self.fields['user'].queryset = user.__class__.objects.filter(pk=user.pk)
        if 'initial' in kwargs and 'checkout_form' in kwargs['initial']:
            initial_checkout_form = kwargs['initial']['checkout_form']
            self.fields['checkout_form'].queryset = CheckoutForm.objects.filter(pk=initial_checkout_form.pk)
        else:
            self.fields['checkout_form'].queryset = CheckoutForm.objects.none()  
            
    class Meta:
        model = DeliveryForm
        fields = ['user', 'checkout_form', 'agent', 'delivery_method', 'delivery_status']


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['method', 'account', 'number', 'transaction_id', 'payment_date']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['method'].widget.attrs.update({'class': 'form-control'})
        self.fields['account'].widget.attrs.update({'class': 'form-control'})
        self.fields['number'].widget.attrs.update({'class': 'form-control'})
        self.fields['transaction_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['payment_date'].widget.attrs.update({'class': 'form-control'})
        

class SendMoneyForm(forms.ModelForm):
    class Meta:
        model = SendMoney
        fields = ['sender','receiver', 'amount', 'note']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SendMoneyForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['sender'].queryset = self.fields['sender'].queryset.filter(pk=user.pk)
            self.fields['receiver'].queryset = self.fields['receiver'].queryset.exclude(pk=user.pk)
            
    def save(self, commit=True):
        instance = super().save(commit=False)
        sender = instance.sender
        receiver = instance.receiver
        amount = instance.amount
        
        sender_earning = Earning.objects.get_or_create(user=sender)[0]
        sender_earning.ref_amount -= amount
        sender_earning.total_amount = sender_earning.sales_amount + sender_earning.ref_amount
        sender_earning.save()
        
        receiver_earning = Earning.objects.get_or_create(user=receiver)[0]
        receiver_earning.ref_amount += amount
        receiver_earning.total_amount = receiver_earning.sales_amount + receiver_earning.ref_amount
        receiver_earning.save()
        
        if commit:
            instance.save()
        return instance


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['method', 'account', 'number', 'amount', 'note']
    
            
class AgentWithdrawalForm(forms.ModelForm):
    class Meta:
        model = AgentWithdrawal
        fields = ['method', 'account', 'number', 'amount', 'note']
        
        
        
#....................................................................................................#
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Old Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm New Password'
        
        
        
#....................................................................................................#
