from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def productdetail(request, product_id): 
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items': items,'product':product, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/productdetail.html', context)
 

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        country = request.POST['country']

        if request.user.is_authenticated:
            customer = request.user.customer
            
            shipping_address = ShippingAddress.objects.create(
                customer=customer,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                country=country
            )
            
            
            
            order_details = OrderDetails.objects.create(
                customer=customer,
                shipping_address=shipping_address
               
            )
            
            
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            order.get_cart_items
            order_items = order.orderitem_set.all()
            
            # Associate the OrderItem objects with the OrderDetails---manytomanyfield
            order_details.order_item.set(order_items)

            # Mark the order as complete
            order.complete = True
            order.save()
            grand_total = order.get_cart_total
            
              # Create an instance of OrderDetails and set the total_price field
            order_details = OrderDetails.objects.create(
                customer=customer,
                shipping_address=shipping_address,
                total_price=grand_total
            )

            order_items = order.orderitem_set.all()

            # Associate the OrderItem objects with the OrderDetails---manytomanyfield
            order_details.order_item.set(order_items)

            return render(request, "store/order_placed.html", {"order_details": order_details,"grand_total":grand_total} )

        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
    else:
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']

        context = {'items': items, 'order': order, 'cartItems': cartItems}
        return render(request, 'store/checkout.html', context)
    



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def removeUserCartItems(request):
    data = json.loads(request.body)
    productId = data['productId']

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItems = OrderItem.objects.filter(order=order, product=product)

        if orderItems.exists():
            # total_items_removed = orderItems.count()
            # total_price_removed = sum([item.get_total for item in orderItems])
            orderItems.delete()
            # print("-------------------------")
            # print("CART TOTAL: ", order.get_cart_total)
            order.save()    
            return JsonResponse({'message': 'Items removed',"cart_total":order.get_cart_items, "current_total": order.get_cart_total}, status=200)
        else:
            return JsonResponse({'error': 'Item not found in cart'}, status=400, safe=False)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401, safe=False)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')  
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'store/login.html')

def logout_view(request):
    logout(request)
    return redirect('store')
