from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem
from .forms import ProductForm 


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart', {})
        cart[str(id)] = cart.get(str(id), 0) + 1
        request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    items = []
    total = 0

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            items.append({
                'product': item.product,
                'quantity': item.quantity,
                'total': item.total,
            })
            total += item.total
    else:
        cart = request.session.get('cart', {})
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            item_total = product.price * quantity
            total += item_total
            items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
            })

    return render(request, 'store/cart.html', {'items': items, 'total': total})

def decrease_from_cart(request, product_id):
    if request.user.is_authenticated:
        try:
            item = CartItem.objects.get(user=request.user, product_id=product_id)
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
        except CartItem.DoesNotExist:
            pass
    else:
        cart = request.session.get('cart', {})
        key = str(product_id)
        if key in cart:
            if cart[key] > 1:
                cart[key] -= 1
            else:
                del cart[key]
            request.session['cart'] = cart
            request.session.modified = True
    return redirect('cart')


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    else:
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})