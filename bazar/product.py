from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, CompanyStock



@receiver(post_save, sender=Product)
def update_company_stock(sender, instance, created, **kwargs):
    if created:  
        CompanyStock.objects.create(product=instance, quantity=instance.quantity)
    else:  
        stock_entry, created = CompanyStock.objects.get_or_create(product=instance)
        stock_entry.quantity = instance.quantity
        stock_entry.save()


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product/create_product.html', {'form': form})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:5]  
    return render(request, 'product/product_detail.html', {'product': product, 'related_products': related_products})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})

@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/update_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product/delete_product.html', {'product': product})


@login_required
def company_stock_list(request):
    stocks = CompanyStock.objects.all()
    return render(request, 'product/company_stock_list.html', {'stocks': stocks})