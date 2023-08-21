from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models import CustomUser, Category, Product
from cart.models import Order, OrderItem, Strap
from django.contrib.auth.models import auth
from django.views.decorators.cache import never_cache
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from coupon.models import Coupon
from django.db.models import Sum
from datetime import timedelta,datetime
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.core.serializers import serialize
import json
from django.db.models.functions import TruncDate,TruncYear
# Create your views here.



@never_cache
@login_required(login_url='admin_signin')
def admin_index(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    prod = Product.objects.all()
    orders_within_range = Order.objects.filter(order_date__range=(start_date, end_date))
    total_payment_amount = orders_within_range.aggregate(total_payment=Sum('payment_amount'))['total_payment']
    order_item = OrderItem.objects.all()
    total_order_items = OrderItem.objects.count()
    order=Order.objects.all().order_by('-order_date')[:5]
    daily_order_data = Order.objects.annotate(date=TruncDate('order_date')).values('date').annotate(order_count=Count('id')).order_by('date')
    labels = [item['date'].strftime('%Y-%m-%d') for item in daily_order_data]
    data = [item['order_count'] for item in daily_order_data]

    current_year = datetime.now().year
    query_condition = {'order_status': 'Confirmed'}
    orders_count = Order.objects.filter(order_date__year=current_year, **query_condition).count()

    

    context = {
        'orders_count':orders_count,
        'order_item':order_item,
        'total_order_items':total_order_items,
        'prod':prod,
        'total_payment_amount': total_payment_amount,
        'labels': labels,
        'data': data,
        'order':order,

    }
    return render(request, 'admin/admin_index.html', context)

@never_cache
@login_required(login_url='admin_signin')
def yearly(request):
    yearly_order_data=Order.objects.annotate(year=TruncYear('order_date')).values('year').annotate(order_count=Count('id')).order_by('year')
    labels = [item['year'].strftime('%Y') for item in yearly_order_data]
    data = [item['order_count'] for item in yearly_order_data]
    context = {
        'labels': labels,
        'data': data,
    }
    return render(request,'admin/yearly_chart.html',context)

@never_cache
@login_required(login_url='admin_signin')
def monthly(request):
    monthly_order_data = Order.objects.annotate(month=TruncMonth('order_date')).values('month').annotate(order_count=Count('id')).order_by('month')
    labels = [item['month'].strftime('%Y-%m') for item in monthly_order_data]
    data = [item['order_count'] for item in monthly_order_data]
    context = {
        'labels': labels,
        'data': data,
    }
    return render(request,'admin/monthly_chart.html',context)

@never_cache
@login_required(login_url='admin_signin')
def chart(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    monthly_sales = Order.objects.filter(order_date__range=(start_date, end_date)) \
        .annotate(month=TruncMonth('order_date')) \
        .values('month') \
        .annotate(total_sales=Sum('payment_amount')) \
        .order_by('month')
    
    
    sales = Order.objects.exclude(order_status='Cancelled')
    monthly_sales_list = list(monthly_sales)
    monthly_sales_json = json.dumps(monthly_sales_list, default=str)
    context = {
        'monthly_sales':monthly_sales_json,
        'sales':sales,
    }

    return render(request, 'admin/chart.html', context)


@never_cache
@login_required(login_url='admin_signin')
def sales_report(request):
    order=OrderItem.objects.all()
    
    context={
        'order':order,
    }
    return render(request,'admin/sales_report.html',context)



@never_cache
@login_required(login_url='admin_signin')
def cancel_report(request):
    cancelled_orders = OrderItem.objects.filter(order_status='Cancelled')
    context={
        'order':cancelled_orders,
    }
    return render(request,'admin/cancel_report.html',context)



@never_cache
@login_required(login_url='admin_signin')
def stock_report(request):
    strap=Strap.objects.all()
    context={
        'strap': strap,
    }
    return render(request,'admin/stock_report.html',context)


# def varient(request):
#     strap=Strap.objects.all()
#     return render(request,'admin/varient.html',{'strap':strap})

# def add_varient(request):
#     return render(request,'admin/add_varient.html')

# def edit_varient(request):
#     return render(request,'admin/edit_varient.html')

@never_cache
@login_required(login_url='admin_signin')
def admin_order_details(request,id):
    order = get_object_or_404(Order, order_id=id)
    product = OrderItem.objects.filter(order_no=order)
    order_item=OrderItem.objects.all()
    order_status_choices=OrderItem.ORDER_STATUS
    context={
        'product':product,
        'order':order,
        'order_item':order_item,
        'order_status_choices':order_status_choices,
        }
    return render(request,'admin/admin_order_details.html',context)



@never_cache
@login_required(login_url='admin_signin')
def delete_coupon(request,id):
    coupon=get_object_or_404(Coupon,pk=id)
    coupon.delete()
    return redirect('coupon_list')

def update_order_status(request,id):
    if request.method=='POST':
        stu=request.POST.get('order_status')
        edit=OrderItem.objects.get(id=id)
        edit.order_status=stu
        edit.save()
        return redirect('orders')

@never_cache
@login_required(login_url='admin_signin')
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

@never_cache
@login_required(login_url='admin_signin')
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




@never_cache
@login_required(login_url='admin_signin')
def coupon_list(request):
    coupon = Coupon.objects.all()
    context = {
        'coupon': coupon, 
        }

    return render(request,"admin/coupon_list.html",context)


@never_cache
@login_required(login_url='admin_signin')
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
@login_required(login_url='admin_signin')
def add_product(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('name')
        print("Shape:", product_name)
        category_name = request.POST.get('category')
        category1 = Category.objects.get(categories=category_name)
        product_Image = request.FILES.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price')
        shape=request.POST.get('shape')
        print("Shape:", shape)
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
        print("Shape:", sele_strap)
        strap1=Strap(product_id=product,strap=sele_strap,quantity=quantity)
        print(sele_strap)
        strap1.save()
        messages.success(request, 'New product added successfully')

    return render(request, "admin/add_products.html", {'categories': categories})



@never_cache
@login_required(login_url='admin_signin')
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
        selected_category_name = request.POST.get('selected_category')
        shape = request.POST.get('shape')
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        product_image = request.FILES.get('image')
        print('22222222222222222222222222222222222222222')
        selected_category = get_object_or_404(Category, categories=selected_category_name)
        print('22222222222222222222222222222222222222222')

        product.product_name = product_name
        product.category = selected_category
        product.description = description
        product.price = price
        product.offer_price = offer_price
        product.shape = shape
        print('22222222222222222222222222222222222222222')

        if product_image:
            product.product_Image = product_image
        product.save()  
        print('22222222222222222222222222222222222222222')

        for strap_s in strap:
            strap=strap_s.strap
            quantity=request.POST.get('quantity')
            strap_s.quantity = quantity
            strap_s.save()
            print('llllllllllllllllllllllllllllllllllllllllllllllllllll')
            return redirect('products')
    return render(request, "admin/edit_product.html", context)





@never_cache
def admin_logout(request):
    auth.logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_signin')


@never_cache
@login_required(login_url='admin_signin')
def userspage(request):
    stu = CustomUser.objects.all()
    return render(request, "admin/users.html", {'stu': stu})


@login_required(login_url='admin_signin')
def user_blockpage(request, id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active = False
        user.save()
    return redirect('users')


@login_required(login_url='admin_signin')
def user_unblockpage(request, id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active = True
        user.save()
    return redirect('users')

@never_cache
@login_required(login_url='admin_signin')
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('categoryname')
        ctg=Category.objects.filter(categories=category_name)
        if ctg.exists():
            messages.info(request,'category already exist')
            return render   (request, 'admin/category_list.html')
        else:
            category = Category.objects.create(categories=category_name)
            messages.success(request,'New category added successfully')
            return redirect('category_list')
    return render(request, "admin/category_list.html")

@never_cache
@login_required(login_url='admin_signin')
def category_listpage(request):
    stu = Category.objects.all()
    return render(request, "admin/category_list.html", {'stu': stu})

@never_cache
@login_required(login_url='admin_signin')
def edit_coupon(request,id):
    coupon=Coupon.objects.get(pk=id)
    if request.method=='POST':
        coupon_code=request.POST.get('coupon_code')
        description=request.POST.get('description')
        minimum_amount=request.POST.get('minimum_amount')
        discount_type=request.POST.get('discount_type')
        discount=request.POST.get('discount')
        valid_from=request.POST.get('valid_from')
        valid_to=request.POST.get('valid_to')
        
        coupon.coupon_code=coupon_code
        coupon.description=description
        coupon.minimum_amount=minimum_amount
        coupon.discount_type=discount_type
        coupon.discount=discount
        coupon.valid_from=valid_from
        coupon.valid_to=valid_to
        
        coupon.save()
        messages.success(request,'coupon edit success')
        return redirect('coupon_list')
    return render(request,'admin/edit_coupon.html',{'coupon':coupon})


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
    return render(request,'admin/edit_category.html',{'catgry':catgry})


@never_cache
@login_required(login_url='admin_signin')
def delete_category(request, id):
    co = get_object_or_404(Category,id=id)
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
        strap = get_object_or_404(Strap, pk=id)
        strap.soft_delete()
        return redirect('products')


@login_required(login_url='admin_signin')
def undo_productpage(request, id):
    if request.method == 'POST':
        strap = get_object_or_404(Strap, pk=id)
        strap.undo()
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
            return render(request, 'admin/admin_signin.html') 
    return render(request, 'admin/admin_signin.html')








