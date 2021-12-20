from secrets import token_hex

from django.core import paginator
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate 
from django.contrib import messages
from django.http import HttpResponse
from .models import Category, Delivery, Item, Payment, Basket, BasketItem



def home(request):
    categories = Category.objects.all().order_by('id')
    items = Item.objects.all()

    first_category = None
    if len(categories) > 0:
        first_category = categories[0]
        categories = categories[1:]

    search = request.GET.get("search", None)
    if search is not None:
        items1 = Item.objects.filter(name__contains=search)
        items2 = Item.objects.filter(category__name__contains=search)
        items = [*items1, *items2]

    category = request.GET.get("category", None)
    if category is not None:
        items = Item.objects.filter(category__name=category)

    paginator = Paginator(items.filter(amount_in_stock__gte=1), 8)
    page_number = request.GET.get('page', 1)
    items = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'first_category': first_category,
        'items': items,
    }
    
    basket_id = request.COOKIES.get('basket_id', None)
    if basket_id is not None:
        items = BasketItem.objects.filter(basket__token=basket_id, purchase_made=False)

        request.session['basket_count'] = len(items)
        response = render(request, 'market/index.html', context)
    else:
        basket_id = token_hex(16)
        basket = Basket(token=basket_id)
        basket.save()

        request.session['basket_count'] = 0
        response = render(request, 'market/index.html', context)
        response.set_cookie('basket_id', basket_id)

    return response


def sign_up(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            user = User.objects.create_user(
                first_name=name,
                username=email,
                email=email,
                password=password
            )
            Delivery(user=user).save()
            Payment(user=user).save()

            messages.add_message(request, messages.INFO, 'Account succesfully created.')
            return redirect("sign_in")

        messages.add_message(request, messages.INFO, 'Please fill data correctly.')
        return render(request, "market/sign_up.html")

    return render(request, 'market/sign_up.html')


def sign_in(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.add_message(request, messages.INFO, 'No such a user!')
            return render(request, 'market/sign_in.html')

    return render(request, 'market/sign_in.html')


def log_out(request):
    logout(request)
    return redirect("home")


def profile(request):
    delivery = Delivery.objects.get(user=request.user)
    payment = Payment.objects.get(user=request.user)

    context = {
        'user': request.user,
        'delivery': delivery,
        'payment': payment,
    }

    return render(request, 'market/profile.html', context)


def contacts(request):
    return render(request, 'market/contacts.html')


def update_user_profile(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username

        user.save()

        # messages.add_message(request, messages.INFO, 'Profile updated Succeccfully!')
        return redirect('profile')
    
    # messages.add_message(request, messages.INFO, 'Some Errors!')
    return redirect('profile')


def update_user_delivery(request):
    if request.method == "POST":
        street = request.POST['street']
        building = request.POST['building']
        floor = request.POST['floor']
        apartment = request.POST['apartment']

        delivery = Delivery.objects.get(user=request.user)
        delivery.street = street
        delivery.building = building
        delivery.floor = floor
        delivery.apartment = apartment

        delivery.save()
        return redirect('profile')

    return redirect('profile')


def update_user_payment(request):
    if request.method == "POST":
        credit_card = request.POST['payment']

        payment = Payment.objects.get(user=request.user)
        payment.payment = credit_card

        payment.save()
        return redirect('profile')

    return redirect('profile')


def item_info(request, item_id):
    return render(request, 'market/item_page.html', {'item': Item.objects.get(id=item_id)})


def basket(request):
    basket_items = BasketItem.objects.filter(basket=Basket.objects.get(token=request.COOKIES['basket_id']), purchase_made=False)
    total = sum([item.price for item in basket_items])

    less_amount_item_id = request.GET.get("less_amount", None)
    if less_amount_item_id is not None:
        less_amount = BasketItem.objects.get(id=less_amount_item_id).item.amount_in_stock
        messages.add_message(request, messages.INFO, f'Amount of this item = {less_amount}')

    context = {
        'basket_items': basket_items, 
        'total': total,
    }

    if request.user.is_authenticated:
        context['delivery'] = Delivery.objects.get(user=request.user)
        context['payment'] = Payment.objects.get(user=request.user)
    return render(request, 'market/basket.html', context)


def add_to_basket(request, item_id):
    if request.method == "POST":
        basket = Basket.objects.get(token=request.COOKIES['basket_id'])
        item = Item.objects.get(id=item_id)

        exists = BasketItem.objects.filter(basket=basket, item=item, purchase_made=False).exists()
        print(f'------ exists-{exists}')
        if exists:
            basket_item = BasketItem.objects.get(basket=basket, item=item, purchase_made=False)
            if basket_item.count + 1 <= basket_item.item.amount_in_stock:
                basket_item.count += 1
                basket_item.price = basket_item.price + basket_item.item.price
        else:
            basket_item = BasketItem(basket=basket,
                                item=item,
                                count=1,
                                price=item.price)
        basket_item.save()

    return redirect('home')


def update_basket_item(request):
    if request.method == "POST":
        basket_item = BasketItem.objects.get(id=request.POST['basket_item_id'])

        count = int(request.POST['count'])

        if count > basket_item.item.amount_in_stock:
            return redirect(f'/basket?less_amount={basket_item.id}')

        basket_item.count = count
        basket_item.price = count * basket_item.item.price
        basket_item.save()

    return redirect('basket')


def delete_basket_item(request):
    if request.method == "POST":
        basket_item = BasketItem.objects.get(id=request.POST['basket_item_id'])
        basket_item.delete()

        basket_id = request.COOKIES.get('basket_id', None)
        items = BasketItem.objects.filter(basket__token=basket_id, purchase_made=False)
        request.session['basket_count'] = len(items)

    return redirect('basket')


def buy_basket_items(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('sign_in')

        # update `item.amount_in_stock`
        basket_items = BasketItem.objects.filter(basket__token=request.COOKIES['basket_id'], purchase_made=False)
        for b_item in basket_items:
            b_item.item.amount_in_stock -= b_item.count
            b_item.item.save()

        BasketItem.objects.filter(basket__token=request.COOKIES['basket_id']).update(purchase_made=True)

    return redirect('home')


def create_items(request):
    import pandas as pd 

    if request.method == "GET":
        data = pd.read_excel(r'C:\Users\zaman\Desktop\passive\django help\Eldiar\file.xlsx')
        data = data.to_dict('records')

        for rec in data:
            item = Item(image=rec['Images'],
                        name=rec['name'],
                        description=rec['description'],
                        amount_in_stock=rec['amount_in_stock'],
                        price=rec['price'],
                        measure=rec['measure'],
                        category=Category.objects.get(id=rec['category']))
            item.save()
        return HttpResponse("created")
    
    return HttpResponse("NOT CREATED")


