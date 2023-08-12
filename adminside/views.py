from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib import messages
from app.models import CustomUser, Category, Product,User_Profile
from cart.models import Order, OrderItem, Strap
from django.contrib.auth.models import auth
from django.views.decorators.cache import never_cache
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from coupon.models import Coupon
# Create your views here.
def delete_coupon(request,id):
    print('11111111111111111111111111111111111111111111111111111111111111111')
    coupon=get_object_or_404(Coupon,pk=id)
    print(coupon,'22222222222222222222222222222222222222222222222222      ')
    # if request.method=='POST':
    coupon.delete()
    return redirect('coupon_list')

def edit_coupon(request,id):
    coupon=get_object_or_404(Coupon,pk=id)

    print(coupon,'111111111111111111111111111')
    if request.method=='POST':
        coupon_code=request.POST.get('coupon_code')
        description=request.POST.get('description')
        minimum_amount=request.POST.get('minimum_amount')
        discount_type=request.POST.get('discount_type')
        discount=request.POST.get('discount')
        valid_from=request.POST.get('valid_from')
        valid_to=request.POST.get('valid_to')

        
        coupon.coupon_code=coupon_code,
        coupon.description=description,
        coupon.minimum_amount=minimum_amount,
        coupon.discount_type=discount_type,
        coupon.discount=discount,
        coupon.valid_from=valid_from,
        coupon.valid_to=valid_to,
        
        coupon.save()
        return redirect('coupon_list')
    return render(request,'admin/coupon_list.html',{'coupon':coupon})

def update_order_status(request,id):
    if request.method=='POST':
        stu=request.POST.get('order_status')
        edit=OrderItem.objects.get(id=id)
        edit.order_status=stu
        edit.save()
        return redirect('orders')

def cancel_order(request,id):
    if request.method == 'POST':
        order_item = OrderItem.objects.get(pk=id)
        if order_item:
            order_item.order_status = 'Cancelled'
            order_item.save()
            strap = order_item.strap
            strap.quantity += order_item.quantity
            strap.save()    
        return redirect('myorders')

def add_coupon(request):
    if request.method=='POST':
        coupon_code=request.POST.get('coupon_code')
        description=request.POST.get('description')
        minimum_amount=request.POST.get('minimum_amount')
        discount_type=request.POST.get('discount_type')
        discount=request.POST.get('discount')
        valid_from=request.POST.get('valid_from')
        valid_to=request.POST.get('valid_to')

        coupon=Coupon(
            coupon_code=coupon_code,
            description=description,
            minimum_amount=minimum_amount,
            discount_type=discount_type,
            discount=discount,
            valid_from=valid_from,
            valid_to=valid_to,
        )
        coupon.save()
        return redirect('coupon_list')
    return render(request,'admin/coupon_list.html')




def coupon_list(request):
    coupon = Coupon.objects.all()
    context ={
        'coupon':coupon,
    }
    return render(request,"admin/coupon_list.html",context)


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
    categories = Category.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('name')
        category_name = request.POST.get('category')
        category1 = Category.objects.get(categories=category_name)
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
        strap=Strap.objects.filter(product_id=product)
        categories = Category.objects.all()
        context = {
            'product': product,
            'categories': categories,
            'strap':strap,
        }
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")
    if request.method == 'POST':
        product_name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        print(category_id,'11111111111111111111111111')
        category = get_object_or_404(Category, pk=category_id) 
        print(category,'22222222222222222222222222222222222')
        shape = request.POST.get('shape')
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        product_image = request.FILES.get('image')
        product=Product(
            product_name = product_name,
            category = category,
            description = description,
            price=price,
            offer_price=offer_price,
            shape=shape,
            product_Image=product_image,
        )
        product.save()
        for strap in strap:
            strap=request.POST.get('strap')
            quantity=request.POST.get('quantity')
            straps=Strap(
                strap=strap,
                quantity=quantity,
            )
            strap.save()
        return redirect('admin/products')
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
        category_name = request.POST.get('categoryname')
        ctg=Category.objects.filter(categories=category_name)
        if ctg.exists():
            # error_message = 'Category name already exists.'
            return render(request, 'admin/category_list.html')
        else:
            category = Category.objects.create(categories=category_name)
            # stu = category.objects.all()
            return redirect('category_list')
    return render(request, "admin/category_list.html")

@never_cache
@login_required(login_url='admin_signin')
def category_listpage(request):
    stu = Category.objects.all()
    return render(request, "admin/category_list.html", {'stu': stu})

@never_cache
def edit_category(request,id):
    catgry=Category.objects.get(pk=id)
    if request.method=='POST':
        categories=request.POST.get('category')
        if Category.objects.filter(categories=categories).exclude(pk=id).exists():
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
def delete_category(request, id):
    # if request.method == 'POST':
    co = get_object_or_404(Category,id=id)
    print('11111111111111111111111111111111111111111111111111111111111111111')
    co.delete()
    return redirect('category_list')

@never_cache
@login_required(login_url='admin_signin')
def productspage(request):
    stu = Category.objects.all()
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
        product.undo()
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








