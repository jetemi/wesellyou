"""context processor for cart items, totals and delivery charges"""
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    """
    Context processor - returns context dict for use by any template.
    Get cart from session, if not there then create cart empty dictionary.
    Iterate through items in cart dict, get product, set total and count,
    append dict of item_id, quantity, product object to cart_items list.
    Calculate delivery charge based on threshold in settings.py and amt
    of spend left to get free delivery
    """ 
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_spend_needed = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_spend_needed = 0

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_spend_needed': free_delivery_spend_needed,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
    return context
