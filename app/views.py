from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Signuptable,Producttable, Chocolatetable, Caketable, Carttable, Billtable
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from django.core.mail import send_mail,BadHeaderError


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def gallery(request):
    return render(request, 'gallery.html')


def chocolate(request):
    a = Chocolatetable.objects.all()
    return render(request, 'chocolate.html', {'chocolatekey': a})


def cake(request):
    b = Caketable.objects.all()
    return render(request, 'cake.html', {'cakekey': b})


def chocolate_info(request, id):
    chocolate = get_object_or_404(Chocolatetable, id=id)
    return render(request, 'chocolate_info.html', {'chocolateinfokey': chocolate})


def cake_info(request, id):
    cake = get_object_or_404(Caketable, id=id)
    return render(request, 'cake_info.html', {'cakeinfokey': cake})


def signup(request):
    if request.method == 'POST':
        a = request.POST['name1']
        b = request.POST['name2']
        c = request.POST['name3']
        d = request.POST['name4']
        e = request.POST['name5']
        f = request.POST['name6']
        g = request.POST['name7']

        if User.objects.filter(username=f).exists():
            messages.error(request, "Username already exists.")
            return render(request, "signup.html")

        try:
            # Create the user
            user = User.objects.create_user(username=f, password=g)
            user.save()

            # Create the Signup entry
            e = Signuptable(first_name=a, last_name=b, mobile=c, email=d, place=e, username=f, password=g, user=user)
            e.save()

        except IntegrityError:
            messages.error(request, "An error occurred. Please try again.")

            return render(request, "signup.html")
        return redirect('signin')
    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        a = request.POST['name1']
        b = request.POST['name2']
        user = authenticate(username=a, password=b)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Invalid username or password')
    return render(request, "signin.html")


def lout(request):
    logout(request)
    return redirect('index')


def search(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        results = Producttable.objects.filter(product_name__icontains=query)
    return render(request, 'search.html', {'query': query, 'results': results})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Producttable, id=product_id)

    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity"))
            if quantity <= 0:
                return HttpResponseBadRequest("Quantity must be a positive integer.")

            unit_price = product.unit_price
            image = product.image
            total_price = quantity * unit_price

            # Save to Carttable
            cart_entry = Carttable(
                product_id=product.id,
                product_name=product.product_name,
                quantity=quantity,
                image=image,
                total_price=total_price,
                user_id=request.user.id
            )
            cart_entry.save()

            return redirect('cart')

        except ValueError:
            return HttpResponseBadRequest("Invalid quantity.")
        except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {e}")


@login_required
def cart(request):
    cart_items = Carttable.objects.filter(user_id=request.user.id)

    grand_total = sum(item.total_price for item in cart_items)

    return render(request, "cart.html", {"cartkey": cart_items,"grand_total": grand_total})


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Carttable, id=item_id)
    cart_item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    user_id = request.user.id
    cart_items = Carttable.objects.filter(user_id=user_id)  # Filter cart items by user_id

    # Calculate totals
    sub_total = sum(Decimal(item.total_price) * item.quantity for item in cart_items)
    tax = sub_total * Decimal('0.1')  # Assuming 10% tax rate
    shipping_cost = Decimal('50')  # Assuming a flat shipping rate
    grand_total = sub_total + tax + shipping_cost

    if cart_items.exists():  # Check if cart is not empty
        if request.method == 'POST':
            # Handle form data for checkout
            first_name = request.POST['firstName']
            last_name = request.POST['lastName']
            mobile = request.POST['mobile']
            email = request.POST['email']
            address = request.POST['address']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']

            if all([first_name, last_name, mobile, email, address, country, state, zip_code]):
                for item in cart_items:
                    Billtable.objects.create(
                        product_name=item.product_name,
                        first_name=first_name,
                        last_name=last_name,
                        mobile=mobile,
                        email=email,
                        quantity=item.quantity,
                        total_price=item.total_price * item.quantity,
                        user_id=request.user.id
                    )

                cart_items.delete()  # Clear cart after successful checkout

                return render(request, 'order_success.html')

        context = {
            'cart_items': cart_items,
            'sub_total': sub_total,
            'tax': tax,
            'shipping_cost': shipping_cost,
            'grand_total': grand_total,
        }

        return render(request, 'checkout.html', context)
    else:
        # Redirect or display an error message indicating the cart is empty
        return redirect('cart')  # Replace 'cart_view' with your actual cart view URL name


@login_required
def order_success(request):
    return render(request, 'order_success.html')


@login_required
def show_bill(request):
    bills = Billtable.objects.filter(user_id=request.user.id)
    return render(request, 'show_bills.html', {'bills': bills})


@login_required
def contact(request):
    user = request.user
    signuptable = Signuptable.objects.get(user=user)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject and message:  # Ensure subject and message are not empty
            full_message = f"From: {signuptable.first_name} {signuptable.last_name}\nEmail: {signuptable.email}\n\nMessage:\n{message}"
            try:
                send_mail(
                    subject,  # Subject
                    full_message,  # Message content
                    'naruto27031999@outlook.com',  # From email
                    ['naruto27031999@gmail.com'],  # To email
                    fail_silently=False,
                )
                return redirect('contact_success')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            except Exception as e:
                return HttpResponse(f'An error occurred: {e}')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')

    context = {
        'name': f"{signuptable.first_name} {signuptable.last_name}",
        'email': signuptable.email,
    }
    return render(request, 'contact.html', context)

def contact_success(request):
    return render(request, 'contact_success.html')
