from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib import messages
from app.models import CustomUser, category, Product,User_Profile
from cart.models import Strap
from django.contrib.auth.models import auth
from django.views.decorators.cache import never_cache
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
# Create your views here.





@never_cache
# @login_required(login_url='admin_signin')
def add_product(request):
    categories = category.objects.all()
    strap = ['Rubber', 'Leather', 'Chain']
    if request.method == 'POST':
        product_name = request.POST.get('name')
        category_name = request.POST.get('category')
        product_Image = request.FILES.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        print('product image:', product_Image)

        if Product.objects.filter(product_name=product_name).exists():
            return render(request, 'admin/add_product.html', {'error_message': 'Product already exists.'})
        else:
            try:
                selected_category = category.objects.get(
                    categories=category_name)
            except category.DoesNotExist:
                selected_category = category.objects.create(
                    category_name=category_name)

            product = Product(
                product_name=product_name,
                category=selected_category,
                product_Image=product_Image,
                description=description,
                # strap=strap,
                price=price,
                offer_price=offer_price,
                # quantity=quantity,
            )
            product.save()
            messages.success(request, 'New product added successfully')
        for straps in strap:
            quantity = request.POST.get(f'quantity-{straps}')
            print(f'{straps} quantity: {quantity}')
            strap.append({'name':straps,'quantity':quantity})
            strap=Strap(product_id=product,strap=strap,quantity=quantity)
            strap.save()

    return render(request, "admin/add_product.html", {'categories': categories, 'strap': strap})



@never_cache
# @login_required(login_url='admin_signin')
def edit_productpage(request, id):
    try:
        product = Product.objects.get(pk=id)
        strap=Strap.objects.filter(product=product)
        categories = category.objects.all()
        context = {
            'product': product,
            # 'shape': shape,
            'categories': categories
        }
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")
    if request.method == 'POST':
        product_name = request.POST.get('productName')
        category_id = request.POST.get('categoryId')
        category = get_object_or_404(category, pk=category_id)
        description = request.POST.get('description')
        product_image = request.FILES.get('image')

        product.product_name = product_name
        product.category = category
        product.description = description

        if product_image:
            product.product_Image = product_image
        product.save()
        return redirect('products')
    return render(request, "admin/edit_product.html", context)





@never_cache
def admin_logout(request):
    auth.logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_signin')


@never_cache
# @login_required(login_url='admin_signin')
def userspage(request):
    stu = CustomUser.objects.all()
    return render(request, "admin/users.html", {'stu': stu})


# @login_required(login_url='admin_signin')
def user_blockpage(request, id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active = False
        user.save()
    return redirect('users')


# @login_required(login_url='admin_signin')
def user_unblockpage(request, id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active = True
        user.save()
    return redirect('users')


@never_cache
@login_required(login_url='admin_signin')
def admin_index(request):
    return render(request, "admin/admin_index.html")

@never_cache
@login_required(login_url='admin_signin')
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST['categoryname']
        if category.objects.filter(categories=category_name).exists():
            error_message = 'Category name already exists.'
            return render(request, 'admin/category_list.html')
        else:
            Category = category.objects.create(categories=category_name)
            # stu = category.objects.all()
            return redirect('category_list')
    return render(request, "admin/category_list.html")

@never_cache
@login_required(login_url='admin_signin')
def category_listpage(request):
    stu = category.objects.all()
    return render(request, "admin/category_list.html", {'stu': stu})

@never_cache
def edit_category(request,id):
    catgry=category.objects.get(pk=id)
    if request.method=='POST':
        categories=request.POST.get('category')
        if category.objects.filter(categories=categories).exclude(pk=id).exists():
            messages.error(request,'Category name already exists')
            return redirect('category_list')
        else:
            catgry.categories = categories
            catgry.save()
            messages.success(request,'edit successful')
        return redirect('category_list')
    return render(request,'admin/category_list.html',{'category':categories})


@never_cache
@login_required(login_url='admin_signin')
def delete_categorypage(request, id):
    if request.method == 'POST':
        co = get_object_or_404(category,pk=id)
        co.delete()
        return redirect('category_list')

@never_cache
@login_required(login_url='admin_signin')
def productspage(request):
    stu = category.objects.all()
    products = Product.objects.all()
    strap=Strap.objects.all()
    context={
        'products': products,
        'strap': strap
    }

    return render(request, 'admin/products.html', context)


@login_required(login_url='admin_signin')
def delete_productpage(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=id)
        product.soft_delete()
        return redirect('products')


@login_required(login_url='admin_signin')
def undo_productpage(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=id)
        product.is_deleted = False
        product.save()
        return redirect('products')



def admin_signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user.is_superuser:
            auth.login(request, user)
            return redirect('/users')
        else:
            messages.error(request, "User email or password is incorrect")
            return redirect('/admin_signin')
    return render(request, 'admin/admin_signin.html')








