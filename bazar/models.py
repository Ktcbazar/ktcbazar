from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models import Sum
import uuid
import random
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('agent', 'Agent'),
        ('staff', 'Staff'),
        ('employee', 'Admin')
    ]

    PLACEMENT_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    referral_link = models.CharField(max_length=100, unique=True, blank=True, null=True)
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    placement = models.CharField(max_length=20, choices=PLACEMENT_CHOICES, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,)
    is_approved = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.username
    
    
#....................................................................................................#

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='customer_profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/')
    loyalty_points = models.IntegerField(default=0, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255, null=True,blank=True)
    district = models.CharField(max_length=100, null=True,blank=True)
    zipcode = models.CharField(max_length=20, null=True,blank=True)
    country = models.CharField(max_length=100, null=True,blank=True)
    nid_number = models.CharField(max_length=50, blank=True)
    nid_front_image = models.ImageField(upload_to='nid/', null=True, blank=True)
    nid_back_image = models.ImageField(upload_to='nid/', null=True, blank=True)
    is_updated = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username 
    
    
class AgentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='agent_profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/')
    loyalty_points = models.IntegerField(default=0, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255, null=True,blank=True)
    district = models.CharField(max_length=100, null=True,blank=True)
    zipcode = models.CharField(max_length=20, null=True,blank=True)
    country = models.CharField(max_length=100, null=True,blank=True)
    nid_number = models.CharField(max_length=50, blank=True)
    nid_front_image = models.ImageField(upload_to='nid/', null=True, blank=True)
    nid_back_image = models.ImageField(upload_to='nid/', null=True, blank=True)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username 


class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='staff_profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/')
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255, null=True,blank=True)
    district = models.CharField(max_length=100, null=True,blank=True)
    zipcode = models.CharField(max_length=20, null=True,blank=True)
    country = models.CharField(max_length=100, null=True,blank=True)
    nid_number = models.CharField(max_length=50, blank=True)
    nid_front_image = models.ImageField(upload_to='nid/', null=True, blank=True)
    nid_back_image = models.ImageField(upload_to='nid/', null=True, blank=True)
    is_updated = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    

class EmployeeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='employee_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/')
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255, null=True,blank=True)
    district = models.CharField(max_length=100, null=True,blank=True)
    zipcode = models.CharField(max_length=20, null=True,blank=True)
    country = models.CharField(max_length=100, null=True,blank=True)
    nid_number = models.CharField(max_length=50, blank=True)
    nid_front_image = models.ImageField(upload_to='nid/', null=True, blank=True)
    nid_back_image = models.ImageField(upload_to='nid/', null=True, blank=True)
    is_updated = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Add Department field based on the department model into staff profile model. and add approved field by superuser (without superuser approval staff or employee can not login) 

#....................................................................................................#

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name
    

class ParentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name    
    
    
class ProductCategory(models.Model):
    parent_category = models.ForeignKey(ParentCategory, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    agent_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, db_index=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/')
    size = models.CharField(max_length=20, blank=True, null=True)
    weight = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    is_featured = models.BooleanField(default=False)
    is_arrival = models.BooleanField(default=False)
    is_best_sale = models.BooleanField(default=False)
    is_special_offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name'] 


class CompanyStock(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='stock_entries')
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stock for {self.product.name}"


class CheckoutForm(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    agent = models.ForeignKey(AgentProfile, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    order_notes = models.TextField(blank=True)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Checkout Information for {self.full_name}"


class CheckoutItem(models.Model):
    checkout_form = models.ForeignKey(CheckoutForm, on_delete=models.CASCADE, related_name='checkout_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Checkout Item for {self.checkout_form.full_name} - {self.product.name}"
    


class DeliveryForm(models.Model):
    
    DELIVERY_METHOD_CHOICES = (
        ('Standard', 'Standard'),
        ('Express', 'Express'),
        ('Next Day', 'Next Day'),
        ('Pickup', 'Pickup'),
    )
    
    DEFAULT_DELIVERY_STATUS = 'Pending'
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    checkout_form = models.ForeignKey(CheckoutForm, on_delete=models.CASCADE, related_name='checkout_delivery')
    agent = models.ForeignKey(AgentProfile, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_method = models.CharField(max_length=100, choices=DELIVERY_METHOD_CHOICES)
    delivery_status = models.CharField(max_length=100, null=True, blank=True, default=DEFAULT_DELIVERY_STATUS)
    is_shipped = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Delivery Information for {self.user.username}"
    
    
class PaymentMethod(models.Model):
    METHOD_CHOICES = (
        ('Bksah', 'Bksah'),
        ('Nagad', 'Nagad'),
        ('Rokect', 'Rokect'),
    )
    
    ACCOUNT_CHOICES = (
        ('personal', 'Personal'),
        ('agent', 'Agent'),
        ('merchant ', 'Merchant '),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    checkout_form = models.ForeignKey(CheckoutForm, on_delete=models.CASCADE, related_name='checkout_payment')
    method = models.CharField(max_length=100, choices=METHOD_CHOICES)
    account = models.CharField(max_length=100, choices=ACCOUNT_CHOICES)
    number = models.CharField(max_length=20, blank=True, null=True)
    transaction_id = models.CharField(max_length=50, unique=True)
    payment_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.method} - {self.user.username}"


class AgentCommission(models.Model):
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='agent_commissions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    checkout_form = models.ForeignKey(CheckoutForm, on_delete=models.CASCADE, related_name='checkout_commissions')
    delivery_form = models.ForeignKey(DeliveryForm, on_delete=models.CASCADE, related_name='delivery_commissions')
    sales_amount = models.DecimalField(max_digits=10, decimal_places=2)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE) 
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2) 
    payable_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Agent Commission for {self.agent.user.username} - Product: {self.product.name}" 

    def save(self, *args, **kwargs):
            if not self.pk: 
                commission_amount = self.sales_amount * (self.product_category.agent_commission / 100)
                self.commission_percentage = self.product_category.agent_commission
                self.payable_amount = commission_amount
                total_payable_amount = AgentCommission.objects.aggregate(total=Sum('payable_amount'))['total'] or 0
                self.total_amount = total_payable_amount + commission_amount
            super().save(*args, **kwargs)



#....................................................................................................#


class SaleCommission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    registered_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='registered_sale_commissions')
    generation = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sale Commission for {self.user.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_earning_sales_amount()

    def update_earning_sales_amount(self):
        total_sales_amount = SaleCommission.objects.filter(user=self.user).aggregate(total_sales=Sum('amount'))['total_sales']
        if total_sales_amount is None:
            total_sales_amount = 0
        earning_instance, _ = Earning.objects.get_or_create(user=self.user)
        earning_instance.sales_amount = total_sales_amount
        earning_instance.save()
    
    
class SaleCompanyCommission(models.Model):
    registered_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='company_registered_sale_commissions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sale Company Commission for {self.registered_user.username}"
    
    
class SaleRankCommission(models.Model):
    registered_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rank_sale_commissions')
    rank = models.CharField(max_length=50, null=True, blank=True, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sale Rank Commission for {self.registered_user.username}, Rank {self.rank}"
    
    def save(self, *args, **kwargs):
        if not self.pk: 
            self.rank = self.calculate_rank(self.amount)

        super().save(*args, **kwargs)

    @staticmethod
    def calculate_rank(amount):
        if amount >= 2620000:
            return 5
        elif amount >= 650000:
            return 4
        elif amount >= 170000:
            return 3
        elif amount >= 50000:
            return 2
        elif amount >= 10000:
            return 1
        else:
            return 0
    

class SaleReferralCommission(models.Model):
    referrer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sale_referral_commissions_earned')
    referred_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sale_referral_commissions_generated')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sale Referral Commission from {self.referrer.username} to {self.referred_user.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_earning_ref_amount()

    def update_earning_ref_amount(self):
        total_ref_amount = SaleReferralCommission.objects.filter(referrer=self.referrer).aggregate(total_ref=Sum('amount'))['total_ref']
        if total_ref_amount is None:
            total_ref_amount = 0
        earning_instance, _ = Earning.objects.get_or_create(user=self.referrer)
        earning_instance.ref_amount = total_ref_amount
        earning_instance.save()
    
   
    
class Earning(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rank = models.CharField(max_length=50, null=True, blank=True, default=0)
    sales_amount = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    ref_amount = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.total_amount}"    
    
    def save(self, *args, **kwargs):
        self.total_amount = self.sales_amount + self.ref_amount
        super().save(*args, **kwargs)


@receiver(post_save, sender=Earning)
def update_user_balance(sender, instance, **kwargs):
    user = instance.user
    total_amount = instance.total_amount
    
    user_balance, created = UserBalance.objects.get_or_create(user=user)
    
    user_balance.balance = total_amount
    user_balance.save()

       

class UserBalance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Balance for {self.user.username}: {self.balance}"
    
    
    
def generate_transaction_id():
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(16))
    

class SendMoney(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Money sent from {self.sender.username} to {self.receiver.username} - Amount: {self.amount}"
    

    
class Withdrawal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    )
    
    METHOD_CHOICES = (
        ('Bksah', 'Bksah'),
        ('Nagad', 'Nagad'),
        ('Rokect', 'Rokect'),
    )
    
    ACCOUNT_CHOICES = (
        ('personal', 'Personal'),
        ('agent', 'Agent'),
        ('merchant ', 'Merchant '),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='withdrawals')
    method = models.CharField(max_length=100, choices=METHOD_CHOICES)
    account = models.CharField(max_length=100, choices=ACCOUNT_CHOICES)
    number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    withdrawal_date = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Withdrawal by {self.user.username} - Amount: {self.amount} - Status: {self.status}"

@receiver(post_save, sender=Withdrawal)
def update_user_balance(sender, instance, created, **kwargs):
    if instance.is_approved and not created:
        user_balance = UserBalance.objects.get(user=instance.user)
        user_balance.balance -= instance.amount
        user_balance.save()
        
        

class AgentWithdrawal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    )
    
    METHOD_CHOICES = (
        ('Bksah', 'Bksah'),
        ('Nagad', 'Nagad'),
        ('Rokect', 'Rokect'),
    )
    
    ACCOUNT_CHOICES = (
        ('personal', 'Personal'),
        ('agent', 'Agent'),
        ('merchant ', 'Merchant '),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='agent_withdrawals')
    method = models.CharField(max_length=100, choices=METHOD_CHOICES)
    account = models.CharField(max_length=100, choices=ACCOUNT_CHOICES)
    number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    withdrawal_date = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Withdrawal by {self.user.username} - Amount: {self.amount} - Status: {self.status}"

@receiver(post_save, sender=AgentWithdrawal)
def update_agent_commission(sender, instance, created, **kwargs):
    if instance.is_approved and not created:  
        agent_commission = AgentCommission.objects.filter(agent=instance.user.agent_profile).last()
        if agent_commission:
            agent_commission.total_amount -= instance.amount
            agent_commission.save()
    

#....................................................................................................#
# BackUp code for KTC Bazar 


class Commission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    registered_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='registered_commissions')
    generation = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Commission for {self.user.username}, Generation {self.generation}"
    
    
class CompanyCommission(models.Model):
    registered_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='company_registered_commissions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Company Commission for {self.company.username}, Generation {self.generation}"
    
    
class RankCommission(models.Model):
    registered_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rank_commissions')
    rank = models.CharField(max_length=50,null=True, blank=True,)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Rank Commission for {self.user.username}, Rank {self.rank}"
    
    
class ReferralCommission(models.Model):
    referrer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referral_commissions_earned')
    referred_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referral_commissions_generated')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Referral Commission from {self.referrer.username} to {self.referred_user.username}"
    


class Purchase(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase {self.id} - {self.supplier.name} - {self.purchase_date}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey('Purchase', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase Item {self.id} - {self.product.name} - {self.quantity} units"    
    
class Sales(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sale_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale {self.id} - {self.customer.username} - {self.sale_date}"
    

class SalesItem(models.Model):
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale Item {self.id} - {self.product.name} - {self.quantity} units"

# Not Needed for Ktc Bazar



class ten_Commission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    registered_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ten_commissions')
    generation = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Commission for {self.user.username}, Generation {self.generation}"
    

class RegisteredBalanceTransfer(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_transfers')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Transfer from {self.sender.username} to {self.receiver.username}, Amount: {self.amount}"


class GenEarning(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.total_amount}"

    def update_earning(self):
        total_commission = Commission.objects.filter(user=self.user).aggregate(total=Sum('amount'))['total'] or 0
        total_sale_commission = SaleCommission.objects.filter(user=self.user).aggregate(total=Sum('amount'))['total'] or 0

        self.total_amount = total_commission + total_sale_commission
        self.save()


class RefEarning(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.total_amount}"
    
    def update_total_amount(self):
        total_referral_commission = ReferralCommission.objects.filter(referrer=self.user).aggregate(total=Sum('amount'))['total'] or 0
        total_sale_referral_commission = SaleReferralCommission.objects.filter(referrer=self.user).aggregate(total=Sum('amount'))['total'] or 0
        self.total_amount = total_referral_commission + total_sale_referral_commission
        self.save()
        
#....................................................................................................#