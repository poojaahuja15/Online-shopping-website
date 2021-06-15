from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json

# Create your views here.
def index(request):
    products = Product.objects.all()
    n = len(products)

    nSlides = n//4 + ceil((n/4) - (n//4))

    params = {'no_of_slides': nSlides,'range': range(1, nSlides),'product': products}
    return render(request,'index.html', params)

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        c = Contact(name=name, email=email, phone=phone, message=message)
        c.save()
        return redirect('/')
    else:
        return render(request, 'contact.html')

def products(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, 'products.html', params)


def productview(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'productview.html', {'product':product})

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'tracker.html')


def checkout(request):
    if request.method == "POST":
        items_json= request.POST.get('itemsJson', '')
        name = request.POST.get('name','')
        amount = request.POST.get('amount','')
        email = request.POST.get('email','')
        address1 = request.POST.get('address1','')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')

        order = Order(items_json=items_json, amount=amount, name=name, email=email, address1=address1, address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'checkout.html', {'thank': thank, 'id': id})

    else:
         return render(request, 'checkout.html')