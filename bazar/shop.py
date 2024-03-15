from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, CheckoutItem, CheckoutForm, AgentCommission, ProductCategory, DeliveryForm, PaymentMethod
from django.contrib import messages 
from .forms import CheckoutFormModelForm, DeliveryFormForm, PaymentMethodForm
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min, Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def shop(request):
    sort_by = request.GET.get('sort_by')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if category_id:
        category = get_object_or_404(ProductCategory, pk=category_id)
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if sort_by == 'popularity':
        pass
    elif sort_by == 'date':
        products = products.order_by('-created_at')
    elif sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'price-desc':
        products = products.order_by('-price')

    paginator = Paginator(products, 10)  
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    categories = ProductCategory.objects.all()
    min_price = Product.objects.aggregate(Min('price'))['price__min']
    max_price = Product.objects.aggregate(Max('price'))['price__max']

    return render(request, 'shop/shop.html', {'products': products, 'categories': categories, 'min_price': min_price, 'max_price': max_price})



@login_required
def backend_shop(request):
    products = Product.objects.all()
    return render(request, 'shop/backend_shop.html', {'products': products})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if 'cart' not in request.session:
        request.session['cart'] = {}
    quantity = int(request.POST.get('quantity', 1))

    if str(product.id) in request.session['cart']:
        request.session['cart'][str(product.id)]['quantity'] += quantity
        messages.success(request, f'{quantity} {product.name}(s) added to the cart.')
    else:
        request.session['cart'][str(product.id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
        }
        messages.success(request, f'{quantity} {product.name}(s) added to the cart.')

    request.session.modified = True  

    return redirect('backend_shop')



@login_required
def reset_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True

    return redirect('cart')



@login_required
def cart(request):
    cart_data = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item in cart_data.items():
        product = Product.objects.get(id=product_id)
        quantity = item['quantity']
        price = item['price']
        total_price += quantity * price

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': quantity * price,
        })

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def checkout(request):
    logged_in_user = request.user
    form = CheckoutFormModelForm(request.POST or None, user=logged_in_user) 

    if request.method == 'POST':
        if form.is_valid():
            total_price = sum(
                item['quantity'] * item['price'] for item in request.session.get('cart', {}).values()
            )

            checkout_form_instance = form.save(commit=False)
            checkout_form_instance.user = logged_in_user
            checkout_form_instance.total_amount = total_price
            checkout_form_instance.save()

            cart_items = request.session.get('cart', {})
            for item_id, item in cart_items.items():
                product = get_object_or_404(Product, id=item_id)
                CheckoutItem.objects.create(
                    checkout_form=checkout_form_instance,
                    product=product,
                    quantity=item['quantity'],
                    unit_price=item['price']
                )

            request.session['cart'] = {}

            messages.success(request, 'Checkout successful!')
            return redirect(reverse('create_delivery_form', kwargs={'checkout_form_id': checkout_form_instance.id}))

    cart_items = request.session.get('cart', {})
    total_price = sum(item['quantity'] * item['price'] for item in cart_items.values())

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total_price': total_price, 'form': form})



@login_required
def create_delivery_form(request, checkout_form_id):
    checkout_form = get_object_or_404(CheckoutForm, id=checkout_form_id)
    form = DeliveryFormForm(request.POST or None, initial={'checkout_form': checkout_form}, user=request.user)

    if request.method == 'POST':
        if form.is_valid():
            delivery_form = form.save()
            selected_agent = delivery_form.agent
            products = checkout_form.checkout_items.values_list('product', flat=True)
            for product_id in products:
                product = get_object_or_404(Product, id=product_id)
                
                try:
                    product_category = product.category
                except ObjectDoesNotExist:
                    product_category = None

                agent_commission = AgentCommission.objects.create(
                    agent=selected_agent,
                    product=product,
                    checkout_form=checkout_form,
                    delivery_form=delivery_form,
                    sales_amount=product.price * checkout_form.checkout_items.get(product=product).quantity,
                    product_category=product_category  
                )

            return redirect(reverse('payment_method_form', kwargs={'checkout_form_id': checkout_form_id}))

    return render(request, 'shop/create_delivery_form.html', {'form': form})


@login_required
def payment_method_form(request, checkout_form_id):
    checkout_form = get_object_or_404(CheckoutForm, id=checkout_form_id)
    form = PaymentMethodForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            payment_method_instance = form.save(commit=False)
            payment_method_instance.checkout_form = checkout_form
            payment_method_instance.user = request.user
            payment_method_instance.save()

            return redirect('thanks_for_shopping')  

    return render(request, 'shop/payment_method_form.html', {'form': form})



@login_required
def thanks_for_shopping(request):
    return render(request, 'shop/thanks_for_shopping.html')


@login_required
def order_details(request):
    checkout_forms = CheckoutForm.objects.filter(user=request.user) 
    delivery_forms = DeliveryForm.objects.filter(checkout_form__in=checkout_forms)
    payment_methods = PaymentMethod.objects.filter(checkout_form__in=checkout_forms)
    return render(request, 'product/order_details.html', {'checkout_forms': checkout_forms, 'delivery_forms': delivery_forms, 'payment_methods': payment_methods})


@login_required
def admin_order_details(request):
    checkout_forms = CheckoutForm.objects.all()  
    delivery_forms = DeliveryForm.objects.all()  
    payment_methods = PaymentMethod.objects.all()
    return render(request, 'product/admin_order_details.html', {'checkout_forms': checkout_forms, 'delivery_forms': delivery_forms, 'payment_methods': payment_methods})





#....................................................................................................#




