from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, profile, supplier, product_category, product, shop, commission, send_money, withdrawal, agent_withdrawal



urlpatterns = [
    
    #Forntend
    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
    path('how_we_work/', views.how_we_work, name='how_we_work'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('become_marketer/', views.become_marketer, name='become_marketer'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_use/', views.terms_of_use, name='terms_of_use'),
    path('notice_board/', views.notice_board, name='notice_board'),
    path('updates/', views.updates, name='updates'),
    path('partners/', views.partners, name='partners'),
    
    #Authentication 
    path('login/', views.custom_login, name='login'),
    path('referral/', views.referral, name='referral'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    
    #Registration Messages
    path('registration_success/', views.registration_success, name='registration_success'),
    path('waiting-for-approval/', views.waiting_for_approval, name='waiting_for_approval'),
    
    #Reset Password 
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    #Change Password 
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_change_success/', views.password_change_success, name='password_change_success'),
    
    #Dashboard
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('agent_dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    
    #Staff Profile
    path('staff/create/', profile.create_staff_profile, name='create_staff_profile'),
    path('staff_profile_list', profile.staff_profile_list, name='staff_profile_list'),
    path('admin_staff_profile_list', profile.admin_staff_profile_list, name='admin_staff_profile_list'),
    path('staff/<int:pk>/', profile.read_staff_profile, name='read_staff_profile'),
    path('staff/<int:pk>/update/', profile.update_staff_profile, name='update_staff_profile'),
    path('staff/<int:pk>/delete/', profile.delete_staff_profile, name='delete_staff_profile'),
    path('staff/approval/requests/', profile.staff_approval_requests, name='staff_approval_requests'),
    path('staff/approve/<int:user_id>/', profile.approve_staff_profile, name='approve_staff_profile'),
    path('staff/reject/<int:user_id>/', profile.reject_staff_profile, name='reject_staff_profile'),
    
    #Employee Profile
    path('employee/create/', profile.create_employee_profile, name='create_employee_profile'),
    path('employee/<int:pk>/', profile.read_employee_profile, name='read_employee_profile'),
    path('employee_profile_list', profile.employee_profile_list, name='employee_profile_list'),
    path('admin_employee_profile_list', profile.admin_employee_profile_list, name='admin_employee_profile_list'),
    path('employee/<int:pk>/update/', profile.update_employee_profile, name='update_employee_profile'),
    path('employee/<int:pk>/delete/', profile.delete_employee_profile, name='delete_employee_profile'),
    path('employee/approval/requests/', profile.employee_approval_requests, name='employee_approval_requests'),
    path('employee/approve/<int:user_id>/', profile.approve_employee_profile, name='approve_employee_profile'),
    path('employee/reject/<int:user_id>/', profile.reject_employee_profile, name='reject_employee_profile'),
    
    
    #Agent Profile
    path('agent/create/', profile.create_agent_profile, name='create_agent_profile'),
    path('agent_profile_list', profile.agent_profile_list, name='agent_profile_list'),
    path('admin_agent_profile_list', profile.admin_agent_profile_list, name='admin_agent_profile_list'),
    path('agent/<int:pk>/', profile.read_agent_profile, name='agent_profile_detail'),
    path('agent/<int:pk>/update/', profile.update_agent_profile, name='update_agent_profile'),
    path('agent/<int:pk>/delete/', profile.delete_agent_profile, name='delete_agent_profile'),
    
    #Customer Profile
    path('customer/create/', profile.create_customer_profile, name='create_customer_profile'),
    path('customer_profile_list', profile.customer_profile_list, name='customer_profile_list'),
    path('admin_customer_profile_list', profile.admin_customer_profile_list, name='admin_customer_profile_list'),
    path('customer/<int:pk>/', profile.read_customer_profile, name='read_customer_profile'),
    path('customer/<int:pk>/update/', profile.update_customer_profile, name='update_customer_profile'),
    path('customer/<int:pk>/delete/', profile.delete_customer_profile, name='delete_customer_profile'),
    
    #Department
    path('department/create/', views.create_department, name='create_department'),
    path('department_list/', views.department_list, name='department_list'),
    
    #Supplier
    path('supplier/create/', supplier.create_supplier, name='create_supplier'),
    path('supplier/<int:pk>/', supplier.supplier_detail, name='supplier_detail'),
    path('supplier/', supplier.supplier_list, name='supplier_list'),
    path('supplier/<int:pk>/update/', supplier.update_supplier, name='update_supplier'),
    path('supplier/<int:pk>/delete/', supplier.delete_supplier, name='delete_supplier'),
    
    #Parent Category 
    path('create_parent_category', product_category.create_parent_category, name='create_parent_category'),
    
    #Product Category
    path('categories/', product_category.product_category_list, name='product_category_list'),
    path('category/<int:pk>/', product_category.product_category_detail, name='product_category_detail'),
    path('category/create/', product_category.create_product_category, name='create_product_category'),
    path('category/update/<int:pk>/', product_category.update_product_category, name='update_product_category'),
    path('category/delete/<int:pk>/', product_category.delete_product_category, name='delete_product_category'),
    
    
    #Product 
    path('create-product/', product.create_product, name='create_product'),
    path('product/<int:pk>/', product.product_detail, name='product_detail'),
    path('product-update/<int:pk>/', product.update_product, name='update_product'),
    path('product-delete/<int:pk>/', product.delete_product, name='delete_product'),
    path('product-list', product.product_list, name='product_list'),
    path('company_stock_list', product.company_stock_list, name='company_stock_list'),
    
    #Shop
    path('shop/', shop.shop, name='shop'),
    path('backend_shop/', shop.backend_shop, name='backend_shop'),
    path('cart/', shop.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', shop.add_to_cart, name='add_to_cart'),
    path('reset_cart/', shop.reset_cart, name='reset_cart'),
    path('checkout/', shop.checkout, name='checkout'),
    path('create_delivery_form/<int:checkout_form_id>/', shop.create_delivery_form, name='create_delivery_form'),
    path('payment-method/<int:checkout_form_id>/', shop.payment_method_form, name='payment_method_form'),
    
    path('delivery_approval_requests/', views.delivery_approval_requests, name='delivery_approval_requests'),
    path('approve_delivery/<int:order_id>/', views.approve_delivery, name='approve_delivery'),
    path('reject_delivery/<int:order_id>/', views.reject_delivery, name='reject_delivery'),
    
    path('thanks-for-shopping/', shop.thanks_for_shopping, name='thanks_for_shopping'),
    
    path('shipped_approval_requests/', views.shipped_approval_requests, name='shipped_approval_requests'),
    path('approve_shipped/<int:delivery_id>/', views.approve_shipped, name='approve_shipped'),
    path('reject_shipped/<int:delivery_id>/', views.reject_shipped, name='reject_shipped'),
    
    path('order_details/', shop.order_details, name='order_details'),
    path('admin_order_details/', shop.admin_order_details, name='admin_order_details'),
    
    #Commission
    path('agent-commissions/', commission.agent_commission_list, name='agent_commission_list'),
    path('admin-agent-commissions/', commission.admin_agent_commission_list, name='admin_agent_commission_list'),
    path('sales-commissions/', commission.sale_commission_list, name='sale_commission_list'),
    path('admin-sales-commissions/', commission.admin_sale_commission_list, name='admin_sale_commission_list'),
    path('sale-referral-commissions/', commission.sale_referral_commission_list, name='sale_referral_commission_list'),
    path('admin-sale-referral-commissions/', commission.admin_sale_referral_commission_list, name='admin_sale_referral_commission_list'),
    path('sale-rank-commissions/', commission.sale_rank_commission_list, name='sale_rank_commission_list'),
    path('admin-sale-rank-commissions/', commission.admin_sale_rank_commission_list, name='admin_sale_rank_commission_list'),
    path('sale-company-commissions/', commission.sale_company_commission_list, name='sale_company_commission_list'),
    path('earning-detail/', commission.earning_detail, name='earning_detail'),
    path('admin-earning-detail/', commission.admin_earning_detail, name='admin_earning_detail'),
    
    #Send Money 
    path('send-money/', send_money.send_money_list, name='send_money_list'),
    path('admin_send_money_list/', send_money.admin_send_money_list, name='admin_send_money_list'),
    path('send-money/<int:pk>/', send_money.send_money_detail, name='send_money_detail'),
    path('send-money/create/', send_money.send_money_create, name='send_money_create'),
    path('send-money/update/<int:pk>/', send_money.send_money_update, name='send_money_update'),
    path('send-money/delete/<int:pk>/', send_money.send_money_delete, name='send_money_delete'),
    path('send-money/insufficient-balance/', send_money.insufficient_balance, name='insufficient_balance'),
    path('send-money/success/', send_money.send_success, name='send_success'),
    
    #Withdrawal
    path('withdrawal', withdrawal.withdrawal_list, name='withdrawal_list'),
    path('admin_withdrawal_list', withdrawal.admin_withdrawal_list, name='admin_withdrawal_list'),
    path('withdrawal/<int:pk>/', withdrawal.withdrawal_detail, name='withdrawal_detail'),
    path('withdrawal/create/', withdrawal.withdrawal_create, name='withdrawal_create'),
    path('withdrawal/<int:pk>/update/', withdrawal.withdrawal_update, name='withdrawal_update'),
    path('withdrawal/<int:pk>/delete/', withdrawal.withdrawal_delete, name='withdrawal_delete'),
    
    path('withdrawal/approval/', withdrawal.withdrawal_approval_requests, name='withdrawal_approval_requests'),
    path('withdrawal/approve/<int:withdrawal_id>/', withdrawal.approve_withdrawal, name='approve_withdrawal'),
    path('withdrawal/reject/<int:withdrawal_id>/', withdrawal.reject_withdrawal, name='reject_withdrawal'),
    
    #Agent Withdrawal
    path('agent-withdrawals/', agent_withdrawal.agent_withdrawal_list, name='agent_withdrawal_list'),
    path('agent-withdrawals/create/', agent_withdrawal.agent_withdrawal_create, name='agent_withdrawal_create'),
    path('agent-withdrawals/<int:pk>/', agent_withdrawal.agent_withdrawal_detail, name='agent_withdrawal_detail'),
    path('agent-withdrawals/<int:pk>/update/', agent_withdrawal.agent_withdrawal_update, name='agent_withdrawal_update'),
    path('agent-withdrawals/<int:pk>/delete/', agent_withdrawal.agent_withdrawal_delete, name='agent_withdrawal_delete'),
    
    path('agent_withdrawal_list/', agent_withdrawal.agent_withdrawal_list, name='agent_withdrawal_list'),
    path('admin_agent_withdrawal_list/', agent_withdrawal.admin_agent_withdrawal_list, name='admin_agent_withdrawal_list'),
    
    path('agent_withdrawal_requests/', agent_withdrawal.agent_withdrawal_requests, name='agent_withdrawal_requests'),
    path('approve_agent_withdrawal/<int:withdrawal_id>/', agent_withdrawal.approve_agent_withdrawal, name='approve_agent_withdrawal'),
    path('reject_agent_withdrawal/<int:withdrawal_id>/', agent_withdrawal.reject_agent_withdrawal, name='reject_agent_withdrawal'),
    
    
    #Tree
    path('downline/<int:referrer_id>/', views.downline, name='downline'),
    
]   


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 