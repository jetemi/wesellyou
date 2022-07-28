from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404

# Create your views here.
from django.contrib import messages
from products.models import Product


def view_cart(request):
    """Show the items in the cart"""
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """
    Add item to the cart. Get quantity from posted form.
    Get cart from session, if not there then create cart empty dictionary.
    If item already in cart, check if total will be above max of 10, if yes
    then show error, else increase quantity.
    If item not already in cart then add it to the cart.
    Overwrite the session variable cart with new cart.
    Use 'redirect_url' hidden input in form to redirect user back to same page.
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    if item_id in list(cart.keys()):
        if cart[item_id] + quantity > 10:
            messages.error(
                request,
                'As producs are currently selling fast, we want everyone to partake of this goodness '
                'we only sell a max of 10 of each '
                f'at a time. You have {cart[item_id]} of "{product.name}" '
                f'in your shopping cart and adding another {quantity} will bring total '
                f'quantity for that item above 10. Thank you for your interest'
                ' but please reduce the quantity and try again. Thank you!'
                )
        else:
            cart[item_id] += quantity
            messages.success(
                request,
                f'Quantity for {product.name} updated to {cart[item_id]}',
                extra_tags='show_bag_in_toast'
                )
    else:
        cart[item_id] = quantity
        messages.success(
            request,
            f'{product.name} added to your bag',
            extra_tags='show_bag_in_toast'
            )
    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """
    Handles the form submitted from cart.html page to adjust quantity.
    If quantity greater than zero, set the new quantity, otherwise remove it.
    Overwrite cart session variable with new cart.
    Return user to cart page.
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    if quantity > 0:
        cart[item_id] = quantity
        messages.success(
            request,
            f'Quantity for {product.name} updated to {cart[item_id]}',
            extra_tags='show_bag_in_toast'
            )
    else:
        cart.pop(item_id)
        messages.success(
            request,
            f'{product.name} removed from your bag',
            extra_tags='show_bag_in_toast'
            )
    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """
    Handles the link from cart.html to remove an item (via javascript).
    Get cart from session, remove item, update cart session variable.
    Return success response. If error, raise server error.
    """
    try:
        product = get_object_or_404(Product, pk=item_id)
        cart = request.session.get('cart', {})
        cart.pop(item_id)
        request.session['cart'] = cart
        messages.success(
            request,
            f'{product.name} removed from your bag',
            extra_tags='show_bag_in_toast'
            )
        return HttpResponse(status=200)
    except Exception as error:
        messages.error(request, f'Error removing item: {error}')
        return HttpResponse(status=500)
