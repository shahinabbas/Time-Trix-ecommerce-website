from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib import messages
from app.models import CustomUser, category, Product,User_Profile
from cart.models import Order, OrderItem, Strap
from django.contrib.auth.models import auth
from django.views.decorators.cache import never_cache
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
# Create your views here.



def orders(request):
    use=CustomUser.objects.all()
    order=Order.objects.all()
    order_item=OrderItem.objects.all()
    order_status_choices=OrderItem.ORDER_STATUS
    context={
        'order': order,
        'order_item':order_item,
        'choice':order_status_choices
    }
    return render(request,"admin/orders.html",context)
 

@never_cache
# @login_required(login_url='admin_signin')
def add_product(request):
    categories = category.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('name')
        category_name = request.POST.get('category')
        category1 = category.objects.get(categories=category_name)
        product_Image = request.FILES.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price')
        shape=request.POST.get('shape')
        offer_price = request.POST.get('offer_price')

        if Product.objects.filter(product_name=product_name).exists():
            return render(request, 'admin/add_products.html', {'error_message': 'Product already exists.'})
        else:
            product = Product(
                product_name=product_name,
                category=category1,
                product_Image=product_Image,
                description=description,
                price=price,
                offer_price=offer_price,
                shape=shape,
            )
            product.save()
        quantity = request.POST.get('quantity')
        sele_strap=request.POST.get('strap')
        strap1=Strap(product_id=product,strap=sele_strap,quantity=quantity)
        print(sele_strap)
        strap1.save()
        messages.success(request, 'New product added successfully')

    return render(request, "admin/add_products.html", {'categories': categories})



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
def delete_product(request, id):
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
        return redirect('admin_index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_superuser:

            auth.login(request, user)
            return redirect('admin_index')
        else:
            messages.error(request, "User email or password is incorrect")
            return redirect('/admin_signin')
    return render(request, 'admin/admin_signin.html')








