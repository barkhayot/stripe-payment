from django.shortcuts import render, redirect, get_object_or_404
import stripe
from .models import Product, Pack, Order
from django.http import JsonResponse
# Create your views here.

# API KEY (.ENV is not used)
stripe.api_key = 'API_KEY'

# Get list of all products and make pack model of all selected products 
def get_list_products(request):
    products = Product.objects.all()
    data =  request.POST.getlist('scales')
    if request.method == 'POST':
        pack = Pack.objects.create()
        for i in data:
            order = Order.objects.create(
                product = Product.objects.get(id=i),
                cart = pack,
                qantity = 1
            )
        return redirect('cart', pack.pk)
    context = {
        'products':products
    }
    return render(request, 'list.html', context)


# Get pack model by id
def get_pack(request, pk):
    cart = get_object_or_404(Pack, pk=pk)
    orders = Order.objects.filter(cart=cart)
    context = {
        'cart': cart,
        'orders':orders
    }
    return render(request, 'cart.html', context)


# Payment function to create session and pass all related order to list for sending stripe API
def pay_cart(request, pk):
    data = []
    cart = Pack.objects.get(pk=pk)
    orders = Order.objects.filter(cart=cart)
    for i in orders:
        temp={}
        ver = {}
        product_data = {}
        ver['currency'] = 'usd'
        product_data['name'] = i.product.name
        ver['product_data'] = product_data
        ver['unit_amount'] = i.product.price

        temp['price_data'] = ver
        
        temp['quantity'] = i.qantity

        data.append(temp)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=data,
            mode= 'payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/canceled',
    )
     
    print(data)

    return JsonResponse({'session_id': session.id})

# Success call back
def success(request):
    return render(request, 'success.html')

# Cancel call back
def cancel(request):
    return render(request, 'cancel.html')


# Demo Structure
# def buy_product(request, id):
#     product = Product.objects.get(id=id)
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items =[{
#                     'price_data' :{
#                         'currency' : 'usd',  
#                         'product_data': {
#                             'name': product.name
#                         },
#                     'unit_amount': product.price
#                     },
#                     'quantity' : 2
#                 },
#                 {
#                     'price_data' :{
#                         'currency' : 'usd',  
#                         'product_data': {
#                             'name': "Test"
#                         },
#                     'unit_amount': 23333
#                     },
#                     'quantity' : 2
#                 }],
#             mode= 'payment',
#             success_url='http://localhost:8000/success',
#             cancel_url='http://localhost:8000/canceled',
#     )
#     return JsonResponse({'session_id': session.id})

