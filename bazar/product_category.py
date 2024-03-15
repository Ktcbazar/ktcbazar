from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductCategory
from .forms import ProductCategoryForm, ParentCategoryForm
from django.contrib.auth.decorators import login_required



@login_required
def create_parent_category(request):
    if request.method == 'POST':
        form = ParentCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_category_list')
    else:
        form = ParentCategoryForm()
    return render(request, 'product_category/create_parent_category.html', {'form': form})


@login_required
def product_category_list(request):
    categories = ProductCategory.objects.all()
    return render(request, 'product_category/product_category_list.html', {'categories': categories})


@login_required
def product_category_detail(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    return render(request, 'product_category/product_category_detail.html', {'category': category})


@login_required
def create_product_category(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_category_list')
    else:
        form = ProductCategoryForm()
    return render(request, 'product_category/create_product_category.html', {'form': form})


@login_required
def update_product_category(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('product_category_list')
    else:
        form = ProductCategoryForm(instance=category)
    return render(request, 'product_category/update_product_category.html', {'form': form})


@login_required
def delete_product_category(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('product_category_list')
    return render(request, 'product_category/delete_product_category.html', {'category': category})
